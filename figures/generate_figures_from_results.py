#!/usr/bin/env python3
import json
import statistics
import collections
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "results" / "universal_3trial_results.json"
OUT2 = ROOT / "figures" / "paper5_fig2_all_domains.png"
OUT4 = ROOT / "figures" / "paper5_fig4_operator_heatmap.png"

scenario_order = [
    "bank","spring","court",
    "rag_support","rag_trouble",
    "agent_tasks",
    "planning_demo","planning_security","planning_resource","planning_priority",
    "multiagent_security","multiagent_ux","multiagent_market","multiagent_debt",
    "multimodal_brand","multimodal_audience","multimodal_competitive","multimodal_abtest",
]

name_map = {
    "bank":"IME\n(bank)", "spring":"IME\n(spring)", "court":"IME\n(court)",
    "rag_support":"RAG\n(support)","rag_trouble":"RAG\n(trouble)",
    "agent_tasks":"Agent\n(tasks)",
    "planning_demo":"Planning\n(demo)","planning_security":"Planning\n(security)","planning_resource":"Planning\n(resource)","planning_priority":"Planning\n(priority)",
    "multiagent_security":"Multi-agent\n(security)","multiagent_ux":"Multi-agent\n(ux)","multiagent_market":"Multi-agent\n(market)","multiagent_debt":"Multi-agent\n(debt)",
    "multimodal_brand":"Multimodal\n(brand)","multimodal_audience":"Multimodal\n(audience)","multimodal_competitive":"Multimodal\n(competitive)","multimodal_abtest":"Multimodal\n(abtest)",
}

with open(RESULTS, encoding="utf-8") as f:
    data = json.load(f)
records = data["records"]

sc_domain = {}
for rec in records:
    sc_domain[rec["scenario"]] = rec["result"]["domain"]
color_map = {
    "IME":"#5A9ECF", "RAG":"#63BC69", "Agent":"#DE77AE",
    "Planning":"#5A9ECF", "Multi-agent":"#63BC69", "Multimodal":"#DE77AE"
}

vals = collections.defaultdict(list)
for rec in records:
    if float(rec["temperature"]) == 0.3:
        vals[rec["scenario"]].append(rec["result"]["avg_per_turn"])
means = [statistics.mean(vals[s]) for s in scenario_order]
overall = statistics.mean(means)

plt.figure(figsize=(16,5.8))
x = np.arange(len(scenario_order))
plt.bar(x, means, color=[color_map[sc_domain[s]] for s in scenario_order], edgecolor="black", linewidth=1.2)
plt.axhline(overall, color="red", linestyle="--", linewidth=2.2, label=f"Average ({overall:.1f})")
for i,v in enumerate(means):
    plt.text(i, v+1.2, f"{v:.1f}", ha="center", va="bottom", fontsize=8)
plt.title("Token Consumption Across All Domains (Phase 1.5, T=0.3, 3 models x 3 trials)", fontsize=17, weight="bold")
plt.ylabel("Tokens per Turn", fontsize=14, weight="bold")
plt.xlabel("Domain & Scenario", fontsize=14, weight="bold")
plt.xticks(x, [name_map[s] for s in scenario_order], fontsize=9)
plt.ylim(0, max(means)+18)
plt.grid(axis="y", alpha=0.3)
plt.legend(loc="upper right", framealpha=0.9)
plt.tight_layout()
plt.savefig(OUT2, dpi=220)
plt.close()

sigma = collections.Counter(); delta = collections.Counter(); count = collections.Counter()
for rec in records:
    sc = rec["scenario"]
    for t in rec["result"]["turns"]:
        op = t.get("operator")
        if op == "sigma": sigma[sc] += 1
        elif op == "delta": delta[sc] += 1
        count[sc] += 1
sigma_pct = [100.0 * sigma[s] / count[s] if count[s] else 0.0 for s in scenario_order]
delta_pct = [100.0 * delta[s] / count[s] if count[s] else 0.0 for s in scenario_order]

plt.figure(figsize=(14,10.8))
y = np.arange(len(scenario_order))
plt.barh(y, sigma_pct, color="#5A9ECF", edgecolor="black", label="σ (strengthen)")
plt.barh(y, delta_pct, left=sigma_pct, color="#E45B4E", edgecolor="black", label="δ (dampen)")
for i,(sp,dp) in enumerate(zip(sigma_pct, delta_pct)):
    if sp > 8: plt.text(sp/2, i, f"{sp:.0f}%", ha="center", va="center", color="white", fontsize=9, weight="bold")
    if dp > 8: plt.text(sp+dp/2, i, f"{dp:.0f}%", ha="center", va="center", color="white", fontsize=9, weight="bold")
plt.yticks(y, [name_map[s].replace("\n"," ") for s in scenario_order], fontsize=10)
plt.xlabel("Operator Usage (%)", fontsize=15, weight="bold")
plt.title("Operator Selection Patterns Across 18 Scenarios\n(All 324 runs: 3 models x 2 temperatures x 3 trials)", fontsize=18, weight="bold")
plt.xlim(0,100)
plt.grid(axis="x", alpha=0.25)
plt.legend(loc="lower right", fontsize=11, framealpha=0.95)
plt.tight_layout()
plt.savefig(OUT4, dpi=220)
plt.close()

print("saved", OUT2)
print("saved", OUT4)
