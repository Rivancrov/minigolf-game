import json
import math
import random
import time
from collections import defaultdict
from headless_physics import HeadlessPhysics

class HeadlessMCTS:
    def __init__(self, physics, simulations=200):
        self.physics = physics
        self.simulations = simulations
    
    def get_best_action(self, x, y):
        """Find best action using MCTS without graphics"""
        action_scores = defaultdict(list)
        
        # Try different angle/power combinations
        angles = [i * math.pi / 12 for i in range(24)]  # 24 directions
        powers = [40, 60, 80, 100, 120, 140]  # 6 power levels
        
        for angle in angles:
            for power in powers:
                # Run multiple simulations for this action
                wins = 0
                total_time = 0
                
                for _ in range(self.simulations):
                    scored, shot_time, _, _ = self.physics.simulate_shot(x, y, angle, power)
                    if scored:
                        wins += 1
                        total_time += shot_time
                
                if wins > 0:
                    win_rate = wins / self.simulations
                    avg_time = total_time / wins if wins > 0 else 10
                    # Score considers both win rate and speed
                    score = win_rate * (1.0 / (1 + avg_time))
                    action_scores[(angle, power)] = score
        
        if action_scores:
            best_action = max(action_scores.items(), key=lambda x: x[1])
            return best_action[0], best_action[1]  # (angle, power), score
        
        return None, 0

def overnight_training():
    print("=== OVERNIGHT MCTS TRAINING (No Graphics!) ===")
    print("This will run for hours - perfect for overnight training")
    
    physics = HeadlessPhysics()
    mcts = HeadlessMCTS(physics, simulations=100)  # 100 sims per action
    policy_table = {}
    
    # Generate realistic training positions
    positions = []
    
    # Ground positions
    for x in range(50, 750, 25):
        positions.append((x, 584))
    
    # Platform positions
    for x in range(0, 100, 15):
        positions.append((x, 484))
    for x in range(300, 550, 20):  
        positions.append((x, 284))
    
    # Near hole positions
    for x in range(600, 750, 10):
        positions.append((x, 584))
    
    print(f"Training on {len(positions)} positions...")
    print(f"Each position: 24 angles × 6 powers × 100 simulations = 14,400 shot tests")
    print(f"Total simulations: {len(positions) * 24 * 6 * 100:,}")
    print("This will take 2-6 hours depending on your computer")
    print()
    
    start_time = time.time()
    
    for i, (x, y) in enumerate(positions):
        pos_start = time.time()
        print(f"Position {i+1}/{len(positions)}: ({x}, {y})", end=" ... ")
        
        # Train MCTS on this position
        best_action, score = mcts.get_best_action(x, y)
        
        if best_action:
            angle, power = best_action
            
            # Store top strategies
            x_bucket = int(x // 40)
            y_bucket = int(y // 30)
            x_bucket = max(0, min(19, x_bucket))
            y_bucket = max(0, min(19, y_bucket))
            state_key = f"{x_bucket}_{y_bucket}"
            
            # Save the learned strategy
            policy_table[state_key] = [{
                'angle': angle,
                'power': power,
                'win_rate': score
            }]
            
            pos_time = time.time() - pos_start
            elapsed = time.time() - start_time
            remaining = (elapsed / (i + 1)) * (len(positions) - i - 1)
            
            print(f"✓ {pos_time:.1f}s (ETA: {remaining/3600:.1f}h)")
            
            # Save progress every 10 positions
            if (i + 1) % 10 == 0:
                with open('ai_policy_progress.json', 'w') as f:
                    json.dump(policy_table, f)
                print(f"  → Saved progress: {len(policy_table)} strategies learned")
        else:
            print("✗ No good actions found")
    
    # Save final policy
    with open('ai_policy.json', 'w') as f:
        json.dump(policy_table, f, indent=2)
    
    total_time = time.time() - start_time
    print(f"\n🎉 TRAINING COMPLETE! 🎉")
    print(f"Time taken: {total_time/3600:.1f} hours")
    print(f"Strategies learned: {len(policy_table)}")
    print(f"Total simulations run: {len(positions) * 24 * 6 * 100:,}")
    print(f"Saved to: ai_policy.json")
    print("\nYour AI should now be MUCH smarter!")

if __name__ == "__main__":
    overnight_training()