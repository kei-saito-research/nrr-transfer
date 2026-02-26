#!/usr/bin/env python3
"""
Universal (Paper 5) rebuild experiment runner.

Design:
- Main line (IME-aligned): temp=0.3, 3 trials, 3 models
- Robustness line: temp=0.0, 3 trials, 3 models

Scenarios are loaded from an existing notebook that defines SCENARIOS[...] dicts.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


UNIVERSAL_SCENARIOS = [
    "bank",
    "spring",
    "court",
    "rag_support",
    "rag_trouble",
    "agent_tasks",
    "planning_demo",
    "planning_security",
    "planning_resource",
    "planning_priority",
    "multiagent_security",
    "multiagent_ux",
    "multiagent_market",
    "multiagent_debt",
    "multimodal_brand",
    "multimodal_audience",
    "multimodal_competitive",
    "multimodal_abtest",
]

MODEL_IDS = {
    "claude": "claude-sonnet-4-20250514",
    "gpt": "gpt-4o-mini-2024-07-18",
    "gemini": "gemini-2.0-flash",
}


@dataclass
class RunConfig:
    notebook_path: Optional[str]
    scenarios_json: Optional[str]
    out_json: str
    trials: int
    temperatures: List[float]
    models: List[str]
    max_tokens: int
    alpha: float
    seed: int
    sleep_sec: float
    retry: int


class StateManager:
    """Deterministic state transitions used in previous unified experiments."""

    def __init__(self) -> None:
        self.states: Dict[str, Dict[str, Dict[str, float]]] = {}
        self.counter = 0

    def create_state(self, items: Dict[str, float]) -> str:
        state_id = f"S{self.counter:04d}"
        total = sum(items.values())
        if total <= 0:
            raise ValueError("State total must be > 0")
        self.states[state_id] = {"items": {k: v / total for k, v in items.items()}}
        self.counter += 1
        return state_id

    def get_state(self, state_id: str) -> Dict[str, Dict[str, float]]:
        return self.states[state_id]

    def apply_operator(
        self, state_id: str, operator: str, target: str, strength: float = 0.4
    ) -> str:
        old = self.get_state(state_id)
        items = old["items"].copy()
        if target not in items:
            return state_id

        if operator in ("σ", "sigma"):
            items[target] = min(0.95, items[target] + strength)
        elif operator in ("δ", "delta"):
            items[target] = max(0.05, items[target] - strength)
        else:
            return state_id

        remaining = 1.0 - items[target]
        other_sum = sum(v for k, v in items.items() if k != target)
        if other_sum > 0:
            for k in items:
                if k != target:
                    items[k] = (items[k] / other_sum) * remaining

        return self.create_state(items)


def load_scenarios_from_notebook(path: str) -> Dict[str, Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    blocks: List[str] = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        if "SCENARIOS['" in src and "Phase 3.0 Detail" not in src:
            blocks.append(src)

    if not blocks:
        raise ValueError("Could not find SCENARIOS definitions in notebook.")

    env: Dict[str, Any] = {}
    for block in blocks:
        exec(block, {}, env)

    if "SCENARIOS" not in env:
        raise ValueError("SCENARIOS not found after executing notebook blocks.")
    return env["SCENARIOS"]


def extract_operator(response_text: str, valid_targets: List[str]) -> Tuple[Optional[str], Optional[str]]:
    text = response_text.lower()
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = text.replace('"', "").replace("'", "")

    operator: Optional[str] = None
    if "sigma" in text or "σ" in text:
        operator = "sigma"
    elif "delta" in text or "δ" in text:
        operator = "delta"

    target: Optional[str] = None
    for t in valid_targets:
        if t.lower() in text:
            target = t
            break
    return operator, target


def make_prompt(domain: str, items: List[str], turn_text: str) -> str:
    items_str = ", ".join(items)
    if domain == "IME":
        return f"""State has: [{items_str}]
New: "{turn_text}"

Choose operator and target:
- sigma: strengthen matching interpretation
- delta: weaken non-matching interpretation

Output ONLY:
operator: <sigma or delta>
target: <one of the items>"""
    if domain == "RAG":
        return f"""Documents: [{items_str}]
User query: "{turn_text}"

Which document is most relevant?

Output ONLY:
operator: <sigma or delta>
target: <document key>

sigma = increase relevance, delta = decrease relevance"""
    if domain == "Agent":
        return f"""Tasks: [{items_str}]
Situation: "{turn_text}"

Which task should be prioritized or deprioritized?

Output ONLY:
operator: <sigma or delta>
target: <task key>"""
    if domain == "Planning":
        return f"""Project tasks: [{items_str}]
New information: "{turn_text}"

Which task should be adjusted?

Output ONLY:
operator: <sigma or delta>
target: <task key>"""
    if domain == "Multi-agent":
        return f"""Expert perspectives: [{items_str}]
New information: "{turn_text}"

Which expert is most relevant?

Output ONLY:
operator: <sigma or delta>
target: <expert key>"""
    if domain == "Multimodal":
        return f"""Design candidates: [{items_str}]
New information: "{turn_text}"

Which design should be adjusted?

Output ONLY:
operator: <sigma or delta>
target: <design key>"""
    raise ValueError(f"Unknown domain: {domain}")


class LLMClients:
    def __init__(self) -> None:
        self._claude = None
        self._openai = None
        self._gemini = None

    def _ensure_clients(self) -> None:
        if self._claude is None:
            import anthropic

            self._claude = anthropic.Anthropic()
        if self._openai is None:
            from openai import OpenAI

            self._openai = OpenAI()
        if self._gemini is None:
            import google.generativeai as genai

            key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not key:
                raise RuntimeError("Missing GEMINI_API_KEY (or GOOGLE_API_KEY).")
            genai.configure(api_key=key)
            self._gemini = genai

    def call(
        self,
        model: str,
        model_id: str,
        prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> Tuple[str, int, int, int]:
        self._ensure_clients()

        if model == "claude":
            msg = self._claude.messages.create(
                model=model_id,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            text = msg.content[0].text
            inp = msg.usage.input_tokens
            out = msg.usage.output_tokens
            return text, inp + out, inp, out

        if model == "gpt":
            res = self._openai.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            text = res.choices[0].message.content or ""
            inp = res.usage.prompt_tokens
            out = res.usage.completion_tokens
            return text, inp + out, inp, out

        if model == "gemini":
            gm = self._gemini.GenerativeModel(
                model_name=model_id,
                generation_config={"max_output_tokens": max_tokens, "temperature": temperature},
            )
            res = gm.generate_content(prompt)
            text = res.text
            usage = getattr(res, "usage_metadata", None)
            if usage:
                inp = int(getattr(usage, "prompt_token_count", 0) or 0)
                out = int(getattr(usage, "candidates_token_count", 0) or 0)
            else:
                inp, out = 0, 0
            return text, inp + out, inp, out

        raise ValueError(f"Unknown model: {model}")


def parse_turn_text(turn: Dict[str, Any]) -> str:
    return turn.get("text", turn.get("query", turn.get("situation", "")))


def run_one_scenario(
    clients: LLMClients,
    scenario_key: str,
    scenario: Dict[str, Any],
    model: str,
    temperature: float,
    max_tokens: int,
    alpha: float,
    retry: int,
    sleep_sec: float,
) -> Dict[str, Any]:
    mgr = StateManager()
    state_id = mgr.create_state(scenario["initial_state"])
    domain = scenario["domain"]

    result: Dict[str, Any] = {
        "scenario": scenario_key,
        "domain": domain,
        "phase": "1.5",
        "model": model,
        "model_id": MODEL_IDS[model],
        "temperature": temperature,
        "turns": [],
        "total_tokens": 0,
        "sigma_count": 0,
        "delta_count": 0,
    }

    for turn_idx, turn in enumerate(scenario["turns"], start=1):
        text = parse_turn_text(turn)
        items = list(mgr.get_state(state_id)["items"].keys())
        prompt = make_prompt(domain, items, text)

        last_err = None
        response_text = ""
        total = inp = out = 0
        for _ in range(retry):
            try:
                response_text, total, inp, out = clients.call(
                    model=model,
                    model_id=MODEL_IDS[model],
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                last_err = None
                break
            except Exception as e:  # API/network/limits
                last_err = str(e)
                time.sleep(1.5)

        if last_err is not None:
            result["turns"].append({"turn": turn_idx, "error": last_err, "success": False})
            continue

        op, target = extract_operator(response_text, items)
        success = op is not None and target is not None
        if success:
            state_id = mgr.apply_operator(state_id, op, target, strength=alpha)
            if op == "sigma":
                result["sigma_count"] += 1
            elif op == "delta":
                result["delta_count"] += 1

        result["turns"].append(
            {
                "turn": turn_idx,
                "text": text,
                "total_tokens": total,
                "input_tokens": inp,
                "output_tokens": out,
                "operator": op,
                "target": target,
                "success": success,
                "response": response_text,
            }
        )
        result["total_tokens"] += total
        time.sleep(sleep_sec)

    n_turns = len(scenario["turns"])
    result["avg_per_turn"] = result["total_tokens"] / n_turns if n_turns else 0
    result["success_rate"] = (
        sum(1 for t in result["turns"] if t.get("success")) / n_turns if n_turns else 0
    )
    return result


def _safe_std(values: List[float]) -> float:
    if len(values) <= 1:
        return 0.0
    return statistics.pstdev(values)


def aggregate(results: Dict[str, Any]) -> Dict[str, Any]:
    buckets: Dict[Tuple[str, str, float], List[Dict[str, Any]]] = {}
    for rec in results["records"]:
        key = (rec["scenario"], rec["model"], float(rec["temperature"]))
        buckets.setdefault(key, []).append(rec["result"])

    by_condition: List[Dict[str, Any]] = []
    for (scenario, model, temperature), trials in sorted(
        buckets.items(), key=lambda x: (x[0][2], x[0][1], x[0][0])
    ):
        avg_tokens = [t["avg_per_turn"] for t in trials]
        success_rates = [t["success_rate"] for t in trials]
        n_turns = len(trials[0]["turns"]) if trials else 0

        complete_consistency_turns = 0
        if len(trials) >= 2 and n_turns > 0:
            for i in range(n_turns):
                pairs = {(t["turns"][i].get("operator"), t["turns"][i].get("target")) for t in trials}
                if len(pairs) == 1:
                    complete_consistency_turns += 1

        by_condition.append(
            {
                "scenario": scenario,
                "model": model,
                "temperature": temperature,
                "n_trials": len(trials),
                "avg_tokens_per_turn_mean": round(statistics.mean(avg_tokens), 4),
                "avg_tokens_per_turn_std": round(_safe_std(avg_tokens), 4),
                "success_rate_mean": round(statistics.mean(success_rates), 4),
                "success_rate_std": round(_safe_std(success_rates), 4),
                "trial_turn_consistency": (
                    round(complete_consistency_turns / n_turns, 4) if n_turns else 0.0
                ),
            }
        )

    return {"by_condition": by_condition}


def save_json(path: str, payload: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser(description="Run Universal 3-trial rebuild experiments.")
    parser.add_argument("--notebook", help="Path to nrr_unified_experiments_final.ipynb")
    parser.add_argument("--scenarios-json", help="Path to scenarios JSON (preferred for standalone runs)")
    parser.add_argument(
        "--out",
        default=f"universal_3trial_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        help="Output json path",
    )
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--temperatures", default="0.3,0.0")
    parser.add_argument("--models", default="claude,gpt,gemini")
    parser.add_argument("--max-tokens", type=int, default=200)
    parser.add_argument("--alpha", type=float, default=0.4)
    parser.add_argument("--seed", type=int, default=20260208)
    parser.add_argument("--sleep-sec", type=float, default=0.3)
    parser.add_argument("--retry", type=int, default=5)

    a = parser.parse_args()
    temperatures = [float(x.strip()) for x in a.temperatures.split(",") if x.strip()]
    models = [x.strip() for x in a.models.split(",") if x.strip()]
    for m in models:
        if m not in MODEL_IDS:
            raise ValueError(f"Unknown model: {m}")
    return RunConfig(
        notebook_path=a.notebook,
        scenarios_json=a.scenarios_json,
        out_json=a.out,
        trials=a.trials,
        temperatures=temperatures,
        models=models,
        max_tokens=a.max_tokens,
        alpha=a.alpha,
        seed=a.seed,
        sleep_sec=a.sleep_sec,
        retry=a.retry,
    )


def main() -> None:
    cfg = parse_args()
    random.seed(cfg.seed)
    if cfg.scenarios_json:
        with open(cfg.scenarios_json, "r", encoding="utf-8") as f:
            scenarios = json.load(f)
    elif cfg.notebook_path:
        scenarios = load_scenarios_from_notebook(cfg.notebook_path)
    else:
        raise ValueError("Provide either --scenarios-json or --notebook.")
    missing = [k for k in UNIVERSAL_SCENARIOS if k not in scenarios]
    if missing:
        raise ValueError(f"Missing scenarios in notebook: {missing}")

    tasks = []
    for model in cfg.models:
        for temp in cfg.temperatures:
            for trial in range(1, cfg.trials + 1):
                for scenario_key in UNIVERSAL_SCENARIOS:
                    tasks.append(
                        {
                            "model": model,
                            "temperature": temp,
                            "trial": trial,
                            "scenario_key": scenario_key,
                        }
                    )
    random.shuffle(tasks)

    payload: Dict[str, Any] = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "script": "universal_rebuild_3trial.py",
            "models": {m: MODEL_IDS[m] for m in cfg.models},
            "trials": cfg.trials,
            "temperatures": cfg.temperatures,
            "max_tokens": cfg.max_tokens,
            "alpha": cfg.alpha,
            "seed": cfg.seed,
            "task_count": len(tasks),
        },
        "records": [],
        "aggregation": {},
    }

    clients = LLMClients()
    for idx, t in enumerate(tasks, start=1):
        key = f"{t['model']}|temp={t['temperature']}|trial={t['trial']}|{t['scenario_key']}"
        print(f"[{idx}/{len(tasks)}] {key}")
        result = run_one_scenario(
            clients=clients,
            scenario_key=t["scenario_key"],
            scenario=scenarios[t["scenario_key"]],
            model=t["model"],
            temperature=t["temperature"],
            max_tokens=cfg.max_tokens,
            alpha=cfg.alpha,
            retry=cfg.retry,
            sleep_sec=cfg.sleep_sec,
        )
        payload["records"].append(
            {
                "model": t["model"],
                "temperature": t["temperature"],
                "trial": t["trial"],
                "scenario": t["scenario_key"],
                "result": result,
            }
        )
        payload["aggregation"] = aggregate(payload)
        save_json(cfg.out_json, payload)

    print(f"\nDone. Saved: {cfg.out_json}")


if __name__ == "__main__":
    main()
