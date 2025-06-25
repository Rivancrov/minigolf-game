#!/usr/bin/env python3

"""
🏌️‍♂️ MINIGOLF AI PROJECT 🏌️‍♂️
Main launcher for the intelligent minigolf game

Features:
- Physics-accurate minigolf simulation
- AI vs Human gameplay  
- Mega-evolved AI strategies
- Comprehensive training system
"""

import sys
import os

# Add paths for imports
sys.path.insert(0, 'core_game')
sys.path.insert(0, 'ai_system')

try:
    import menu
    print("🏌️‍♂️ Starting Minigolf AI Game...")
    print("   Single Player: Play alone")
    print("   VS AI: Challenge the mega-evolved AI!")
    print()
    menu.main()
except ImportError as e:
    print(f"❌ Error importing game: {e}")
    print("Make sure you're in the project root directory")
except Exception as e:
    print(f"❌ Game error: {e}")
