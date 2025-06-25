import json
import math

def analyze_evolved_strategies():
    """Analyze what the SuperAI learned"""
    print("🧠 SUPER AI STRATEGY ANALYSIS 🧠")
    print()
    
    with open('ai_policy.json', 'r') as f:
        strategies = json.load(f)
    
    print(f"📊 Total strategy sets: {len(strategies)}")
    
    # Analyze by strategy type
    type_stats = {'bounce': [], 'direct': [], 'platform': [], 'safe': []}
    win_rate_stats = []
    
    for position, position_strategies in strategies.items():
        print(f"\n📍 Position {position}:")
        
        for strategy in position_strategies:
            strategy_type = strategy['strategy_type']
            win_rate = strategy['win_rate']
            angle_deg = math.degrees(strategy['angle']) % 360
            power = strategy['power']
            
            type_stats[strategy_type].append(win_rate)
            win_rate_stats.append(win_rate)
            
            print(f"   {strategy_type:8s}: {angle_deg:6.1f}° {power:6.1f}pwr (win:{win_rate:.2f})")
    
    print(f"\n📈 STRATEGY TYPE ANALYSIS:")
    for strategy_type, win_rates in type_stats.items():
        if win_rates:
            avg_win_rate = sum(win_rates) / len(win_rates)
            max_win_rate = max(win_rates)
            count = len(win_rates)
            print(f"   {strategy_type:8s}: {count:2d} strategies, avg:{avg_win_rate:.3f}, max:{max_win_rate:.3f}")
    
    print(f"\n🎯 OVERALL PERFORMANCE:")
    print(f"   Total strategies: {len(win_rate_stats)}")
    print(f"   Average win rate: {sum(win_rate_stats)/len(win_rate_stats):.3f}")
    print(f"   Best win rate: {max(win_rate_stats):.3f}")
    print(f"   Strategies > 0.8 win rate: {len([w for w in win_rate_stats if w > 0.8])}")
    print(f"   Strategies > 0.5 win rate: {len([w for w in win_rate_stats if w > 0.5])}")

if __name__ == "__main__":
    analyze_evolved_strategies()