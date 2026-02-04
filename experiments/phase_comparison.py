#!/usr/bin/env python3
"""
Phase Comparison: Phase 1.0 vs 1.5 vs 3.0
Bank scenario (5 turns)
"""

import json
import os

def load_experimental_data():
    """Load experimental data from JSON file"""
    data_path = os.path.join(os.path.dirname(__file__), 'experimental_data.json')
    with open(data_path, 'r') as f:
        return json.load(f)

def compare_phases():
    """Compare token consumption across phases"""
    data = load_experimental_data()
    
    # Extract phase data
    phase_10 = data['phase_10_bank']
    phase_15 = data['phase_15_bank']
    phase_30 = data['phase_30_bank_explicit']
    
    print("="*60)
    print("Phase Comparison: Bank Scenario (5 turns)")
    print("="*60)
    print()
    
    # Phase 1.0
    tokens_10 = phase_10['total_tokens']
    print(f"Phase 1.0 (Naive):")
    print(f"  Total tokens: {tokens_10}")
    print(f"  Avg per turn: {phase_10['avg_per_turn']:.1f}")
    print()
    
    # Phase 1.5
    tokens_15 = phase_15['total_tokens']
    reduction_15 = (tokens_10 - tokens_15) / tokens_10 * 100
    print(f"Phase 1.5 (Operators):")
    print(f"  Total tokens: {tokens_15}")
    print(f"  Avg per turn: {phase_15['avg_per_turn']:.1f}")
    print(f"  Reduction: -{reduction_15:.1f}%")
    print()
    
    # Phase 3.0
    tokens_30 = phase_30['total_tokens']
    reduction_30 = (tokens_10 - tokens_30) / tokens_10 * 100
    print(f"Phase 3.0 (Zero-LLM Explicit):")
    print(f"  Total tokens: {tokens_30}")
    print(f"  Avg per turn: {phase_30['avg_per_turn']:.1f}")
    print(f"  Reduction: -{reduction_30:.1f}%")
    print()
    
    print("="*60)
    print("Summary")
    print("="*60)
    print(f"Phase 1.0 → 1.5: {reduction_15:.1f}% reduction")
    print(f"Phase 1.0 → 3.0: {reduction_30:.1f}% reduction")
    print()
    
    return {
        'phase_10': tokens_10,
        'phase_15': tokens_15,
        'phase_30': tokens_30,
        'reduction_15': reduction_15,
        'reduction_30': reduction_30
    }

if __name__ == '__main__':
    results = compare_phases()
