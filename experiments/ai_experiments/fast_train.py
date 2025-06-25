import json
import math
import random
import mcts_ai

print("=== Fast AI Training (No MCTS) ===")

# Create training data using simple heuristics instead of MCTS
policy_table = {}

# Generate realistic positions
positions = []
# Ground positions
for x in range(100, 700, 50):
    positions.append((x, 584))

# Platform positions  
for x in range(0, 100, 20):
    positions.append((x, 500))
for x in range(300, 550, 30):
    positions.append((x, 300))

print(f"Training on {len(positions)} positions...")

for i, (ball_x, ball_y) in enumerate(positions):
    print(f"Position {i+1}/{len(positions)}: ({ball_x}, {ball_y})")
    
    # Calculate optimal shots for this position
    hole_x = 718
    hole_y = 584
    
    dx = hole_x - ball_x
    dy = hole_y - ball_y
    distance = math.sqrt(dx*dx + dy*dy)
    
    # Generate multiple good shot options
    best_actions = []
    
    # Direct shot
    direct_angle = math.atan2(dy, dx)
    if distance < 100:
        direct_power = 60
    elif distance < 200:
        direct_power = 100
    else:
        direct_power = 140
    
    best_actions.append({
        'angle': direct_angle,
        'power': direct_power,
        'win_rate': 0.8
    })
    
    # High arc shot
    arc_angle = direct_angle + 0.3
    arc_power = direct_power + 20
    best_actions.append({
        'angle': arc_angle,
        'power': arc_power,
        'win_rate': 0.6
    })
    
    # Low power shot
    low_angle = direct_angle - 0.2
    low_power = max(40, direct_power - 30)
    best_actions.append({
        'angle': low_angle,
        'power': low_power,
        'win_rate': 0.5
    })
    
    # Store in policy table
    x_bucket = int(ball_x // 40)
    y_bucket = int(ball_y // 30)
    state_key = f"{x_bucket}_{y_bucket}"
    
    policy_table[state_key] = best_actions

# Save policy
with open('ai_policy.json', 'w') as f:
    json.dump(policy_table, f, indent=2)

print(f"Saved policy with {len(policy_table)} positions")
print("Training complete! AI can now use trained policy.")
print("To use: change game.py to use trained_ai.PreTrainedAI() instead of FastAI()")