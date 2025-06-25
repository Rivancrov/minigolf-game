#!/usr/bin/env python3

# Simple test to see what the AI is doing
import json

def test_ai_logic():
    print("🤖 Testing AI Strategy Selection Logic")
    
    # Load strategies
    with open('ai_policy.json', 'r') as f:
        strategies = json.load(f)
    
    print(f"Loaded {len(strategies)} strategy sets")
    
    # Test position conversion
    test_positions = [
        (100, 584, "Starting position"),
        (720, 584, "Near hole"),
        (750, 550, "In sand area")
    ]
    
    for x, y, desc in test_positions:
        # Convert to bucket like the AI does
        x_bucket = int(x // 40)
        y_bucket = int(y // 30)
        x_bucket = max(0, min(19, x_bucket))
        y_bucket = max(0, min(19, y_bucket))
        state_key = f"{x_bucket}_{y_bucket}"
        
        print(f"\n📍 {desc}: ({x}, {y}) -> bucket {state_key}")
        
        if state_key in strategies:
            position_strategies = strategies[state_key]
            print(f"   Found {len(position_strategies)} strategies!")
            
            # Show best strategies
            sorted_strats = sorted(position_strategies, key=lambda s: s['win_rate'], reverse=True)
            for i, strat in enumerate(sorted_strats[:3]):
                print(f"   {i+1}. {strat['strategy_type']:8s} win_rate={strat['win_rate']:.3f}")
            
            # Check for hole-in-ones
            hole_in_ones = [s for s in position_strategies if s['win_rate'] > 0.9]
            if hole_in_ones:
                print(f"   🎯 {len(hole_in_ones)} HOLE-IN-ONE strategies available!")
        else:
            print(f"   ❌ No strategies found for this position")
            
            # Check nearby positions
            nearby_found = False
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nearby_key = f"{x_bucket + dx}_{y_bucket + dy}"
                    if nearby_key in strategies:
                        print(f"   📍 Nearby position {nearby_key} has strategies")
                        nearby_found = True
                        break
                if nearby_found:
                    break
    
    print(f"\n📊 Strategy Summary:")
    total_strategies = sum(len(strats) for strats in strategies.values())
    hole_in_ones = sum(1 for strats in strategies.values() 
                      for strat in strats if strat['win_rate'] > 0.9)
    print(f"   Total strategies: {total_strategies}")
    print(f"   Hole-in-one strategies: {hole_in_ones}")
    print(f"   Coverage: {len(strategies)} positions out of 400 possible (20x20 grid)")

if __name__ == "__main__":
    test_ai_logic()