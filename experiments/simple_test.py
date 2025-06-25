print("=== Starting simple test ===")

try:
    print("Step 1: Importing train_ai...")
    import train_ai
    print("✓ train_ai imported successfully")
    
    print("Step 2: Importing mcts_ai...")
    import mcts_ai
    print("✓ mcts_ai imported successfully")
    
    print("Step 3: Creating trainer...")
    trainer = train_ai.AITrainer()
    print("✓ Trainer created successfully")
    
    print("Step 4: Getting scenarios...")
    scenarios = trainer.get_training_scenarios()
    print(f"✓ Found {len(scenarios)} scenarios")
    
    if scenarios:
        print(f"First scenario: ball at ({scenarios[0].ball_x:.1f}, {scenarios[0].ball_y:.1f})")
    
    print("=== Simple test completed successfully ===")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()