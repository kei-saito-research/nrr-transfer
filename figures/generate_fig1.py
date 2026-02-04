#!/usr/bin/env python3
"""
Generate Figure 1: Phase Comparison Chart
"""

import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

def load_experimental_data():
    """Load experimental data from JSON file"""
    exp_path = os.path.join(os.path.dirname(__file__), '..', 'experiments', 'experimental_data.json')
    with open(exp_path, 'r') as f:
        return json.load(f)

def generate_figure1():
    """Generate Phase comparison chart"""
    data = load_experimental_data()
    
    # Extract data
    phase_10 = data['phase_10_bank']['total_tokens']
    phase_15 = data['phase_15_bank']['total_tokens']
    phase_30 = data['phase_30_bank_explicit']['total_tokens']
    
    # Calculate reductions
    reduction_15 = (phase_10 - phase_15) / phase_10 * 100
    reduction_30 = (phase_10 - phase_30) / phase_10 * 100
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    phases = ['Phase 1.0\n(Naive)', 'Phase 1.5\n(Operators)', 'Phase 3.0\n(Zero-LLM\nExplicit)']
    tokens = [phase_10, phase_15, phase_30]
    colors = ['#e74c3c', '#3498db', '#2ecc71']
    
    bars = ax.bar(phases, tokens, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for bar, token in zip(bars, tokens):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 30,
                f'{token}\ntokens',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Add reduction labels
    ax.text(0.5, phase_10 * 0.6, f'−{reduction_15:.1f}%', ha='center', fontsize=14, 
            fontweight='bold', color='white', 
            bbox=dict(boxstyle='round', facecolor='#3498db', alpha=0.8))
    
    ax.text(1.5, phase_10 * 0.3, f'−{reduction_30:.1f}%', ha='center', fontsize=14, 
            fontweight='bold', color='white',
            bbox=dict(boxstyle='round', facecolor='#2ecc71', alpha=0.8))
    
    ax.set_ylabel('Total Tokens (5 turns)', fontsize=14, fontweight='bold')
    ax.set_title('IME Token Consumption: Phase Comparison (Bank Scenario)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 1400)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    # Save figure
    output_path = os.path.join(os.path.dirname(__file__), 'figure1_phase_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Figure 1 saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    generate_figure1()
