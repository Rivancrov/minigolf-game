
#!/usr/bin/env python3

"""
🧬🚀 GENETIC AI TRAINING LAUNCHER 🚀🧬

Use this script to start the AI evolution process.
"""

import sys
import os

# Add paths for imports
sys.path.insert(0, 'ai_system')

def launch_training():
    """Launch the main genetic algorithm trainer"""
    try:
        from genetic_trainer import GeneticAITrainer, get_training_positions
        
        print("🚀 Launching the Genetic AI Trainer...")
        print("   This will run for several hours to evolve the best strategies.")
        print("   You can monitor the progress in the console.")
        print("   A progress file 'ai_policy_progress.json' will be saved periodically.")
        print()

        training_positions = get_training_positions()
        trainer = GeneticAITrainer(training_positions)
        trainer.train()

    except ImportError as e:
        print(f"❌ Error importing trainer: {e}")
        print("   Please ensure you are in the project root directory.")
    except Exception as e:
        print(f"❌ An error occurred during training: {e}")

if __name__ == "__main__":
    launch_training()
