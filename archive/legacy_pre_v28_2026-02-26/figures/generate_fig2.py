#!/usr/bin/env python3
"""Generate Figure 2: Domain Summary Charts"""
import json, matplotlib.pyplot as plt, matplotlib, numpy as np, os
matplotlib.use('Agg')

exp_path = os.path.join(os.path.dirname(__file__), '..', 'experiments', 'experimental_data.json')
with open(exp_path, 'r') as f:
    data = json.load(f)

scenarios_data = []
for key, scenario_data in data.items():
    if 'phase_15' in key:
        scenarios_data.append({
            'name': scenario_data.get('scenario', key), 'domain': scenario_data.get('domain', 'Unknown'),
            'turns': len(scenario_data.get('turns', [])), 'sigma': scenario_data.get('sigma_count', 0),
            'delta': scenario_data.get('delta_count', 0)
        })

domain_order = ['IME', 'RAG', 'Agent', 'Planning', 'Multi-agent', 'Multimodal']
scenarios_data.sort(key=lambda x: (domain_order.index(x['domain']) if x['domain'] in domain_order else 999, x['name']))

domain_stats = {}
for s in scenarios_data:
    domain = s['domain']
    if domain not in domain_stats:
        domain_stats[domain] = {'sigma': 0, 'delta': 0, 'total': 0}
    domain_stats[domain]['sigma'] += s['sigma']
    domain_stats[domain]['delta'] += s['delta']
    domain_stats[domain]['total'] += s['turns']

domains = list(domain_stats.keys())
sigma_counts = [domain_stats[d]['sigma'] for d in domains]
delta_counts = [domain_stats[d]['delta'] for d in domains]
total_turns = [domain_stats[d]['total'] for d in domains]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
x, width = np.arange(len(domains)), 0.6

bars1 = ax1.bar(x, sigma_counts, width, label='σ (strengthen)', color='#3498db', alpha=0.9, edgecolor='black', linewidth=1.5)
bars2 = ax1.bar(x, delta_counts, width, bottom=sigma_counts, label='δ (dampen)', color='#e74c3c', alpha=0.9, edgecolor='black', linewidth=1.5)

for i, (s_count, d_count, total) in enumerate(zip(sigma_counts, delta_counts, total_turns)):
    s_pct, d_pct = (s_count / total * 100) if total > 0 else 0, (d_count / total * 100) if total > 0 else 0
    if s_count > 0:
        ax1.text(i, s_count/2, f'{s_count}\n({s_pct:.0f}%)', ha='center', va='center', fontweight='bold', fontsize=10, color='white')
    if d_count > 0:
        ax1.text(i, s_count + d_count/2, f'{d_count}\n({d_pct:.0f}%)', ha='center', va='center', fontweight='bold', fontsize=10, color='white')

ax1.set_ylabel('Operator Count', fontsize=13, fontweight='bold')
ax1.set_xlabel('Domain', fontsize=13, fontweight='bold')
ax1.set_title('Operator Distribution by Domain', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(domains, rotation=15, ha='right')
ax1.legend(loc='upper left', fontsize=11)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

avg_tokens = []
for domain in domains:
    domain_scenarios = [s for s in scenarios_data if s['domain'] == domain]
    total_tokens, total_turns_domain = 0, 0
    for ds in domain_scenarios:
        for key, scenario_data in data.items():
            if scenario_data.get('scenario') == ds['name'] and 'phase_15' in key:
                total_tokens += scenario_data.get('total_tokens', 0)
                total_turns_domain += len(scenario_data.get('turns', []))
    avg = total_tokens / total_turns_domain if total_turns_domain > 0 else 0
    avg_tokens.append(avg)

bars = ax2.bar(x, avg_tokens, width, color='#2ecc71', alpha=0.9, edgecolor='black', linewidth=1.5)

for bar, avg in zip(bars, avg_tokens):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 1, f'{avg:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

overall_avg = 75.8
ax2.axhline(y=overall_avg, color='red', linestyle='--', linewidth=2, label=f'Overall Avg: {overall_avg:.1f}')

ax2.set_ylabel('Avg Tokens per Turn', fontsize=13, fontweight='bold')
ax2.set_xlabel('Domain', fontsize=13, fontweight='bold')
ax2.set_title('Token Efficiency by Domain', fontsize=14, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(domains, rotation=15, ha='right')
ax2.set_ylim(0, 100)
ax2.legend(loc='upper right', fontsize=11)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), 'figure2_domain_summary.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Figure 2 saved to {output_path}")
plt.close()
