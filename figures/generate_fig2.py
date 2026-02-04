#!/usr/bin/env python3
"""
Generate Figure 2: Scaling Validation Chart
"""

import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import os

def load_experimental_data():
    """Load experimental data from JSON file"""
    exp_path = os.path.join(os.path.dirname(__file__), '..', 'experiments', 'experimental_data.json')
    with open(exp_path, 'r') as f:
        return json.load(f)

def generate_figure2():
    """Generate Scaling validation chart"""
    data = load_experimental_data()
    
    # Extract data
    scenarios = ['Bank\n(5 turns)', 'Spring\n(10 turns)', 'Court\n(12 turns)']
    scenario_tokens = [
        data['phase_15_bank']['total_tokens'],
        data['phase_15_spring']['total_tokens'],
        data['phase_15_court']['total_tokens']
    ]
    avg_per_turn = [
        data['phase_15_bank']['avg_per_turn'],
        data['phase_15_spring']['avg_per_turn'],
        data['phase_15_court']['avg_per_turn']
    ]
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    x = np.arange(len(scenarios))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, scenario_tokens, width, label='Total Tokens', 
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2 = ax.twinx()
    line = ax2.plot(x, avg_per_turn, 'o-', color='#e74c3c', linewidth=3, 
                    markersize=12, label='Avg per Turn', markeredgecolor='black', 
                    markeredgewidth=1.5)
    
    # Add value labels
    for i, (bar, token, avg) in enumerate(zip(bars1, scenario_tokens, avg_per_turn)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 30,
                f'{token}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
        ax2.text(i, avg + 2, f'{avg:.1f}', ha='center', va='bottom', 
                 fontsize=11, fontweight='bold', color='#c0392b')
    
    ax.set_xlabel('Scenario', fontsize=14, fontweight='bold')
    ax.set_ylabel('Total Tokens', fontsize=14, fontweight='bold', color='#3498db')
    ax2.set_ylabel('Avg Tokens per Turn', fontsize=14, fontweight='bold', color='#e74c3c')
    ax.set_title('Phase 1.5 Scaling Validation: Consistent Efficiency Across Scenarios', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.tick_params(axis='y', labelcolor='#3498db')
    ax2.tick_params(axis='y', labelcolor='#e74c3c')
    ax.set_ylim(0, 1200)
    ax2.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)
    
    plt.tight_layout()
    
    # Save figure
    output_path = os.path.join(os.path.dirname(__file__), 'figure2_scaling_validation.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Figure 2 saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    generate_figure2()
