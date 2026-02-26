#!/usr/bin/env python3
"""Generate Figure 1: Operator Selection Patterns Heatmap"""
import json, matplotlib.pyplot as plt, matplotlib, numpy as np, os
matplotlib.use('Agg')

exp_path = os.path.join(os.path.dirname(__file__), '..', 'experiments', 'experimental_data.json')
with open(exp_path, 'r') as f:
    data = json.load(f)

scenarios_data = []
for key, scenario_data in data.items():
    if 'phase_15' in key:
        scenario_name = scenario_data.get('scenario', key.replace('phase_15_', ''))
        domain = scenario_data.get('domain', 'Unknown')
        turns = scenario_data.get('turns', [])
        sigma = scenario_data.get('sigma_count', 0)
        delta = scenario_data.get('delta_count', 0)
        total = len(turns)
        scenarios_data.append({
            'name': scenario_name, 'domain': domain, 'turns': total, 'sigma': sigma, 'delta': delta,
            'sigma_pct': (sigma / total * 100) if total > 0 else 0,
            'delta_pct': (delta / total * 100) if total > 0 else 0
        })

domain_order = ['IME', 'RAG', 'Agent', 'Planning', 'Multi-agent', 'Multimodal']
scenarios_data.sort(key=lambda x: (domain_order.index(x['domain']) if x['domain'] in domain_order else 999, x['name']))

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
scenario_names = [s['name'].replace('_', ' ').title() for s in scenarios_data]
sigma_values = [s['sigma_pct'] for s in scenarios_data]
delta_values = [s['delta_pct'] for s in scenarios_data]
y_pos = np.arange(len(scenario_names))

ax.barh(y_pos, sigma_values, color='#3498db', alpha=0.9, edgecolor='black', linewidth=1, label='σ (strengthen)')
ax.barh(y_pos, delta_values, left=sigma_values, color='#e74c3c', alpha=0.9, edgecolor='black', linewidth=1, label='δ (dampen)')

for i, (s_val, d_val) in enumerate(zip(sigma_values, delta_values)):
    if s_val > 5:
        ax.text(s_val/2, i, f'{s_val:.0f}%', ha='center', va='center', fontweight='bold', fontsize=9, color='white')
    if d_val > 5:
        ax.text(s_val + d_val/2, i, f'{d_val:.0f}%', ha='center', va='center', fontweight='bold', fontsize=9, color='white')

current_domain, domain_positions = None, []
for i, s in enumerate(scenarios_data):
    if s['domain'] != current_domain:
        if current_domain is not None:
            ax.axhline(y=i-0.5, color='black', linewidth=2, linestyle='-')
        current_domain = s['domain']
        domain_positions.append((i, current_domain))

ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.set_yticks([pos for pos, _ in domain_positions])
ax2.set_yticklabels([domain for _, domain in domain_positions], fontweight='bold', fontsize=11)

ax.set_yticks(y_pos)
ax.set_yticklabels(scenario_names, fontsize=9)
ax.set_xlabel('Operator Usage (%)', fontsize=14, fontweight='bold')
ax.set_title('Operator Selection Patterns Across 18 Scenarios\n(0%–100% Variation Demonstrates True Generality)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlim(0, 100)
ax.legend(loc='lower right', fontsize=12, framealpha=0.9)
ax.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()

output_path = os.path.join(os.path.dirname(__file__), 'figure1_operator_heatmap.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Figure 1 saved to {output_path}")
plt.close()
