import train_ai

# Quick test - just 1 scenario with 2 games to make sure it works
trainer = train_ai.AITrainer()
scenarios = trainer.get_training_scenarios()
print(f"Found {len(scenarios)} scenarios")

if scenarios:
    print(f"Testing training on first scenario: ({scenarios[0].ball_x}, {scenarios[0].ball_y})")
    trainer.train_from_scenario(scenarios[0], num_games=2)  # Just 2 games for testing
    print("Training test successful!")
else:
    print("No valid scenarios found!")