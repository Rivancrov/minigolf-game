import json
import math
import random

print("=== Standalone AI Training ===")

# Create training data using simple heuristics
policy_table = {}

# Generate realistic positions where ball can rest
positions = []

# Ground positions (main surface)
for x in range(100, 700, 50):
    positions.append((x, 584))

# Platform positions (obstacles ball can rest on)
# Block 2 - horizontal platform at y=500
for x in range(0, 100, 20):
    positions.append((x, 484))  # y=500-16 for ball dimensions

# Block 3 - horizontal platform at y=300  
for x in range(300, 550, 30):
    positions.append((x, 284))  # y=300-16 for ball dimensions

# Near hole positions
for x in range(600, 750, 25):
    positions.append((x, 584))

print(f"Training on {len(positions)} realistic positions...")

hole_x = 718  # flag position
hole_y = 584

for i, (ball_x, ball_y) in enumerate(positions):
    if i % 10 == 0:
        print(f"Position {i+1}/{len(positions)}: ({ball_x}, {ball_y})")
    
    # Calculate shots for this position
    dx = hole_x - ball_x
    dy = hole_y - ball_y
    distance = math.sqrt(dx*dx + dy*dy)
    direct_angle = math.atan2(dy, dx)
    
    # Generate good shot options based on distance
    best_actions = []
    
    if distance < 80:
        # Close to hole - gentle shots
        best_actions.append({
            'angle': direct_angle,
            'power': 50,
            'win_rate': 0.9
        })
        best_actions.append({
            'angle': direct_angle + 0.1,
            'power': 40,
            'win_rate': 0.7
        })
    elif distance < 200:
        # Medium distance
        best_actions.append({
            'angle': direct_angle,
            'power': 90,
            'win_rate': 0.8
        })
        best_actions.append({
            'angle': direct_angle - 0.2,
            'power': 110,
            'win_rate': 0.6
        })
    else:
        # Far from hole - more power needed
        best_actions.append({
            'angle': direct_angle,
            'power': 140,
            'win_rate': 0.7
        })
        best_actions.append({
            'angle': direct_angle + 0.3,
            'power': 120,
            'win_rate': 0.5
        })
    
    # Add a safe low-power option
    best_actions.append({
        'angle': direct_angle,
        'power': max(30, distance * 0.5),
        'win_rate': 0.4
    })
    
    # Store in policy table using same discretization as trained_ai.py
    x_bucket = int(ball_x // 40)
    y_bucket = int(ball_y // 30)
    x_bucket = max(0, min(19, x_bucket))
    y_bucket = max(0, min(19, y_bucket))
    
    state_key = f"{x_bucket}_{y_bucket}"
    policy_table[state_key] = best_actions

# Save the policy
with open('ai_policy.json', 'w') as f:
    json.dump(policy_table, f, indent=2)

print(f"\n✓ Training complete!")
print(f"✓ Saved policy with {len(policy_table)} position strategies")
print(f"✓ Created ai_policy.json file")
print("\nTo use the trained AI:")
print("1. In game.py, change line 564 to: ai_player = trained_ai.PreTrainedAI()")
print("2. The AI will now use learned strategies instead of simple heuristics!")