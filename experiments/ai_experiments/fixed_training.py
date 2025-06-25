import json
import math
import random
import time
from collections import defaultdict
import exact_physics

def get_valid_positions():
    """Get training positions that don't collide with obstacles"""
    positions = []
    
    # Test all potential positions
    candidates = []
    
    # Main ground - every 30 pixels
    for x in range(50, 750, 30):
        candidates.append((x, 584))
    
    # Platform positions
    for x in range(10, 90, 20):
        candidates.append((x, 484))
    for x in range(310, 540, 30):  
        candidates.append((x, 284))
    
    # Near hole positions
    for x in range(650, 710, 15):
        candidates.append((x, 584))
    
    # Filter out positions that collide
    for x, y in candidates:
        collision = False
        for surface in exact_physics.edges:
            if surface.is_collided(x, y):
                collision = True
                break
        
        if not collision:
            positions.append((x, y))
        else:
            print(f"Skipping collision position: ({x}, {y})")
    
    return positions

class ExactMCTS:
    def __init__(self, simulations=25):
        self.simulations = simulations
    
    def get_best_action(self, x, y):
        """Find best action using exact physics MCTS"""
        action_scores = {}
        
        # Smaller action space for faster testing
        angles = [i * math.pi / 12 for i in range(24)]  # Every 15 degrees
        powers = [40, 60, 80, 100, 120, 140]  # 6 power levels
        
        print(f"  Testing {len(angles)} angles × {len(powers)} powers × {self.simulations} sims")
        
        successful_actions = 0
        
        for angle in angles:
            for power in powers:
                wins = 0
                total_time = 0
                
                # Run simulations for this action
                for _ in range(self.simulations):
                    try:
                        scored, shot_time, final_x, final_y = exact_physics.simulate_complete_shot(x, y, angle, power, max_time=5.0)
                        if scored:
                            wins += 1
                            total_time += shot_time
                    except:
                        # Skip if simulation fails
                        continue
                
                if wins > 0:
                    successful_actions += 1
                    win_rate = wins / self.simulations
                    avg_time = total_time / wins
                    score = win_rate * (3.0 / (1 + avg_time))
                    action_scores[(angle, power)] = score
        
        print(f"  Found {successful_actions}/{len(angles) * len(powers)} working actions")
        
        if action_scores:
            best_action = max(action_scores.items(), key=lambda x: x[1])
            return best_action[0], best_action[1], action_scores
        
        return None, 0, {}

def fixed_training():
    print("🔧 FIXED MCTS TRAINING - No Collision Positions 🔧")
    print("Filtering out positions that collide with obstacles...")
    
    positions = get_valid_positions()
    print(f"Valid training positions: {len(positions)}")
    
    if len(positions) == 0:
        print("❌ No valid positions found! Check collision detection.")
        return
    
    mcts = ExactMCTS(simulations=15)  # Fewer sims for faster testing
    policy_table = {}
    
    start_time = time.time()
    
    for i, (x, y) in enumerate(positions[:5]):  # Test just first 5 positions
        pos_start = time.time()
        print(f"\nPosition {i+1}/5: ({x}, {y})")
        
        best_action, best_score, all_scores = mcts.get_best_action(x, y)
        
        if best_action:
            angle, power = best_action
            
            # Store best action
            x_bucket = int(x // 40)
            y_bucket = int(y // 30)
            x_bucket = max(0, min(19, x_bucket))
            y_bucket = max(0, min(19, y_bucket))
            state_key = f"{x_bucket}_{y_bucket}"
            
            policy_table[state_key] = [{
                'angle': angle,
                'power': power,
                'win_rate': best_score
            }]
            
            pos_time = time.time() - pos_start
            print(f"  ✅ Best: {math.degrees(angle):.0f}° power {power} (score: {best_score:.3f})")
            print(f"  ⏱️  {pos_time:.1f}s")
        else:
            print(f"  ❌ No successful actions found")
    
    # Save results
    if policy_table:
        with open('ai_policy.json', 'w') as f:
            json.dump(policy_table, f, indent=2)
        
        print(f"\n✅ Fixed training complete!")
        print(f"Learned {len(policy_table)} strategies")
        print("Try the game now - AI should use these strategies!")
    else:
        print("\n❌ No strategies learned - physics still has issues")

if __name__ == "__main__":
    fixed_training()