import train_ai
import mcts_ai

print("=== AI Training Validation Test ===")

# Test one specific position with intensive training
trainer = train_ai.AITrainer()

# Pick a challenging position - middle of the course
test_position = mcts_ai.GameState(400, 500, 0, 0, 0)
print(f"Testing training on position: ({test_position.ball_x}, {test_position.ball_y})")

# Before training - test AI performance
print("\n--- BEFORE TRAINING ---")
untrained_ai = mcts_ai.MCTSPlayer(simulation_count=100)
print("Testing 5 shots with untrained AI...")
for i in range(5):
    action = untrained_ai.get_best_action(test_position)
    if action:
        print(f"Shot {i+1}: angle={action.angle:.2f} rad ({(action.angle*180/3.14159):.1f}°), power={action.power}")
    else:
        print(f"Shot {i+1}: No action")

# Train intensively on this position
print(f"\n--- TRAINING (this will take a few minutes) ---")
trainer.train_from_scenario(test_position, num_games=100)

# Check what was learned
state_key = trainer.discretize_state(test_position)
learned_actions = trainer.policy_table.get(state_key, [])
print(f"\n--- AFTER TRAINING ---")
print(f"Learned {len(learned_actions)} actions for this position:")
for i, (action, win_rate) in enumerate(learned_actions):
    print(f"Action {i+1}: angle={action.angle:.2f} rad ({(action.angle*180/3.14159):.1f}°), power={action.power}, win_rate={win_rate:.2f}")

# Test if actions are different/better
if learned_actions:
    best_action = learned_actions[0][0]
    print(f"\nBest learned action: {(best_action.angle*180/3.14159):.1f}° at power {best_action.power}")
    print("Training appears to be working!")
else:
    print("\nNo actions learned - training may need adjustment")

print("\nValidation complete!")