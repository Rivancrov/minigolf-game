import json
import math
import random
import time
from collections import defaultdict
import exact_physics

class ExactMCTS:
    def __init__(self, simulations=50):
        self.simulations = simulations
    
    def get_best_action(self, x, y):
        """Find best action using exact physics MCTS"""
        action_scores = {}
        
        # Comprehensive action space
        angles = [i * math.pi / 18 for i in range(36)]  # Every 10 degrees
        powers = [30, 50, 70, 90, 110, 130, 150]  # 7 power levels
        
        print(f"  Testing {len(angles)} angles × {len(powers)} powers × {self.simulations} sims = {len(angles) * len(powers) * self.simulations:,} total simulations")
        
        best_score = 0
        best_action = None
        
        for i, angle in enumerate(angles):
            if i % 9 == 0:  # Progress every 90 degrees
                print(f"    Angle {i+1}/{len(angles)} ({math.degrees(angle):.0f}°)")
            
            for power in powers:
                wins = 0
                total_time = 0
                
                # Run simulations for this action
                for _ in range(self.simulations):
                    scored, shot_time, final_x, final_y = exact_physics.simulate_complete_shot(x, y, angle, power)
                    if scored:
                        wins += 1
                        total_time += shot_time
                
                if wins > 0:
                    win_rate = wins / self.simulations
                    avg_time = total_time / wins
                    # Score: win rate with time bonus (faster is better)
                    score = win_rate * (5.0 / (1 + avg_time))  # Prefer quick scores
                    action_scores[(angle, power)] = score
                    
                    if score > best_score:
                        best_score = score
                        best_action = (angle, power)
        
        return best_action, best_score, action_scores

def real_overnight_training():
    print("🚀 REAL OVERNIGHT MCTS TRAINING - EXACT PHYSICS 🚀")
    print("Using your exact game physics - obstacles, bouncing, rolling!")
    print()
    
    mcts = ExactMCTS(simulations=25)  # 25 sims per action for speed
    policy_table = {}
    
    # Realistic training positions where ball can actually rest
    positions = []
    
    # Main ground - every 30 pixels
    for x in range(50, 750, 30):
        positions.append((x, 584))
    
    # Platform 1 (block_2 top) - y=484
    for x in range(10, 90, 20):
        positions.append((x, 484))
    
    # Platform 2 (block_3 top) - y=284  
    for x in range(310, 540, 30):
        positions.append((x, 284))
    
    # Dense coverage near hole
    for x in range(650, 710, 15):
        positions.append((x, 584))
    
    print(f"Training positions: {len(positions)}")
    print(f"Per position: 36 angles × 7 powers × 25 sims = 6,300 tests")
    print(f"TOTAL SIMULATIONS: {len(positions) * 36 * 7 * 25:,}")
    print(f"Estimated time: 3-8 hours (depends on computer speed)")
    print()
    
    start_time = time.time()
    
    for i, (x, y) in enumerate(positions):
        pos_start = time.time()
        print(f"Position {i+1}/{len(positions)}: ({x}, {y})")
        
        best_action, best_score, all_scores = mcts.get_best_action(x, y)
        
        if best_action:
            angle, power = best_action
            
            # Find top 3 actions for variety
            sorted_actions = sorted(all_scores.items(), key=lambda item: item[1], reverse=True)
            top_actions = []
            
            for (a, p), score in sorted_actions[:3]:
                top_actions.append({
                    'angle': a,
                    'power': p, 
                    'win_rate': score
                })
            
            # Store in policy table
            x_bucket = int(x // 40)
            y_bucket = int(y // 30)
            x_bucket = max(0, min(19, x_bucket))
            y_bucket = max(0, min(19, y_bucket))
            state_key = f"{x_bucket}_{y_bucket}"
            
            policy_table[state_key] = top_actions
            
            pos_time = time.time() - pos_start
            elapsed = time.time() - start_time
            remaining = (elapsed / (i + 1)) * (len(positions) - i - 1)
            
            print(f"  ✅ Best: {math.degrees(angle):.0f}° power {power} (score: {best_score:.3f})")
            print(f"  ⏱️  {pos_time/60:.1f} min (ETA: {remaining/3600:.1f}h)\n")
            
            # Save progress every 5 positions
            if (i + 1) % 5 == 0:
                with open('ai_policy_progress.json', 'w') as f:
                    json.dump(policy_table, f)
                print(f"  💾 Progress saved: {len(policy_table)} strategies learned\n")
        else:
            print(f"  ❌ No successful actions found\n")
    
    # Save final policy
    with open('ai_policy.json', 'w') as f:
        json.dump(policy_table, f, indent=2)
    
    total_time = time.time() - start_time
    print("🎉🎉🎉 REAL TRAINING COMPLETE! 🎉🎉🎉")
    print(f"Time: {total_time/3600:.1f} hours")
    print(f"Positions trained: {len(positions)}")
    print(f"Strategies learned: {len(policy_table)}")
    print(f"Total simulations: {len(positions) * 36 * 7 * 25:,}")
    print("AI should now be MUCH smarter with exact physics!")

if __name__ == "__main__":
    real_overnight_training()