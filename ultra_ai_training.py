#!/usr/bin/env python3

"""
🧬🚀 ULTRA AI TRAINING - NEXT LEVEL INTELLIGENCE 🚀🧬

Streamlined AI training that filters glitch strategies and improves legitimacy
"""

import json
import sys
import os

def quick_ultra_boost():
    """Quick version for immediate improvement - filters glitch strategies"""
    print("⚡ QUICK ULTRA BOOST ⚡")
    print("Fast upgrade to next-level AI intelligence")
    
    ai_policy_path = 'ai_system/ai_policy.json'
    
    # Load existing strategies
    try:
        with open(ai_policy_path, 'r') as f:
            strategies = json.load(f)
    except FileNotFoundError:
        print("❌ No AI policy found. Please train the AI first.")
        return {}
    
    # Filter out obvious glitch strategies
    clean_strategies = {}
    improved_count = 0
    total_strategies_before = sum(len(strats) for strats in strategies.values())
    
    for position, strats in strategies.items():
        clean_strats = []
        for strat in strats:
            # Keep strategies that seem legitimate
            win_rate = strat.get('win_rate', 0)
            strategy_type = strat.get('strategy_type', 'unknown')
            
            # Filter out suspiciously perfect strategies or obvious glitches
            is_legitimate = (
                win_rate < 0.95 or  # Not suspiciously perfect
                strategy_type in ['platform', 'safe'] or  # Conservative types
                (strategy_type == 'bounce' and win_rate < 0.98)  # Reasonable bounces
            )
            
            if is_legitimate:
                clean_strats.append(strat)
            
        if clean_strats:
            clean_strategies[position] = clean_strats
            if len(clean_strats) < len(strats):
                improved_count += 1
    
    total_strategies_after = sum(len(strats) for strats in clean_strategies.values())
    
    # Save cleaned strategies
    with open(ai_policy_path, 'w') as f:
        json.dump(clean_strategies, f, indent=2)
    
    print(f"✅ Cleaned {improved_count} positions of glitch strategies")
    print(f"📊 Strategies: {total_strategies_before} → {total_strategies_after}")
    print(f"🎯 AI now has {len(clean_strategies)} legitimate strategy sets")
    
    return clean_strategies

def analyze_ai_strategies():
    """Analyze the current AI strategies and show quality breakdown"""
    print("📊 AI STRATEGY ANALYSIS 📊")
    
    try:
        with open('ai_system/ai_policy.json', 'r') as f:
            strategies = json.load(f)
    except FileNotFoundError:
        print("❌ No AI policy found.")
        return
    
    strategy_types = {}
    win_rate_ranges = {"Low (0-0.2)": 0, "Medium (0.2-0.5)": 0, "High (0.5-0.8)": 0, "Very High (0.8+)": 0}
    
    total_strategies = 0
    for position, strats in strategies.items():
        for strat in strats:
            total_strategies += 1
            
            # Count strategy types
            strategy_type = strat.get('strategy_type', 'unknown')
            strategy_types[strategy_type] = strategy_types.get(strategy_type, 0) + 1
            
            # Count win rate ranges
            win_rate = strat.get('win_rate', 0)
            if win_rate < 0.2:
                win_rate_ranges["Low (0-0.2)"] += 1
            elif win_rate < 0.5:
                win_rate_ranges["Medium (0.2-0.5)"] += 1
            elif win_rate < 0.8:
                win_rate_ranges["High (0.5-0.8)"] += 1
            else:
                win_rate_ranges["Very High (0.8+)"] += 1
    
    print(f"📍 Total positions: {len(strategies)}")
    print(f"🎯 Total strategies: {total_strategies}")
    print(f"📈 Average strategies per position: {total_strategies/len(strategies):.1f}")
    
    print("\n🎲 Strategy Types:")
    for strategy_type, count in sorted(strategy_types.items()):
        percentage = (count / total_strategies) * 100
        print(f"  {strategy_type}: {count} ({percentage:.1f}%)")
    
    print("\n📊 Win Rate Distribution:")
    for range_name, count in win_rate_ranges.items():
        percentage = (count / total_strategies) * 100
        print(f"  {range_name}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    print("🚀 ULTRA AI TRAINING 🚀")
    print("Streamlined AI optimization system")
    print()
    print("1. Quick Ultra Boost - Clean glitch strategies")
    print("2. Analyze current AI strategies") 
    print()
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        quick_ultra_boost()
        print("\n🎮 Test the improved AI with: python main.py")
    elif choice == "2":
        analyze_ai_strategies()
    else:
        print("Running quick boost by default...")
        quick_ultra_boost()
        print("\n🎮 Test the improved AI with: python main.py")