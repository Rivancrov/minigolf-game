import json
import math
import random
from typing import Optional
import mcts_ai

class PreTrainedAI:
    def __init__(self, policy_file='ai_policy.json'):
        self.policy_table = {}
        self.load_policy(policy_file)
        
    def load_policy(self, policy_file):
        """Load pre-trained policy from file"""
        try:
            with open(policy_file, 'r') as f:
                policy_dict = json.load(f)
            
            # Convert back to usable format
            for state_key_str, actions_data in policy_dict.items():
                x_bucket, y_bucket = map(int, state_key_str.split('_'))
                state_key = (x_bucket, y_bucket)
                
                actions = []
                for action_data in actions_data:
                    action = mcts_ai.Action(action_data['angle'], action_data['power'])
                    win_rate = action_data['win_rate']
                    actions.append((action, win_rate))
                
                self.policy_table[state_key] = actions
            
            print(f"Loaded AI policy with {len(self.policy_table)} states")
            
        except FileNotFoundError:
            print("No pre-trained policy found. Using random AI.")
            self.policy_table = {}
    
    def discretize_state(self, state):
        """Convert continuous state to discrete buckets for lookup"""
        x_bucket = int(state.ball_x // 40)
        y_bucket = int(state.ball_y // 30)
        
        x_bucket = max(0, min(19, x_bucket))
        y_bucket = max(0, min(19, y_bucket))
        
        return (x_bucket, y_bucket)
    
    def get_best_action(self, game_state) -> Optional[mcts_ai.Action]:
        """Get best action from pre-trained policy"""
        if not game_state.is_ball_stationary() or game_state.is_terminal:
            return None
        
        state_key = self.discretize_state(game_state)
        
        # Try to find exact match
        if state_key in self.policy_table:
            actions = self.policy_table[state_key]
            if actions:
                # Use best action with some randomness
                if random.random() < 0.8:  # 80% time use best action
                    return actions[0][0]  # Best action
                else:
                    # Sometimes use second best for variety
                    if len(actions) > 1:
                        return actions[1][0]
                    return actions[0][0]
        
        # Try nearby states if exact match not found
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nearby_key = (state_key[0] + dx, state_key[1] + dy)
                if nearby_key in self.policy_table:
                    actions = self.policy_table[nearby_key]
                    if actions:
                        return actions[0][0]
        
        # Fallback: simple heuristic towards hole
        return self.get_heuristic_action(game_state)
    
    def get_heuristic_action(self, game_state):
        """Fallback heuristic action when no policy available"""
        # Calculate angle towards hole
        hole_x = 800 - 128 + 46  # flag_centre
        hole_y = 600 - 16
        
        dx = hole_x - game_state.ball_x
        dy = hole_y - game_state.ball_y
        
        angle = math.atan2(dy, dx)
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Adjust power based on distance
        if distance < 100:
            power = 40  # Gentle shot when close
        elif distance < 200:
            power = 80
        else:
            power = 120  # More power for long shots
        
        return mcts_ai.Action(angle, power)

class FastAI:
    """Even simpler AI that just aims towards hole with basic power calculation"""
    
    def get_best_action(self, game_state) -> Optional[mcts_ai.Action]:
        if not game_state.is_ball_stationary() or game_state.is_terminal:
            return None
        
        # Calculate angle towards hole
        hole_x = 800 - 128 + 46
        hole_y = 600 - 16
        
        dx = hole_x - game_state.ball_x
        dy = hole_y - game_state.ball_y
        
        angle = math.atan2(dy, dx)
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Smart power calculation
        if distance < 50:
            power = 30
        elif distance < 150:
            power = 60
        elif distance < 300:
            power = 100
        else:
            power = 140
        
        # Add some randomness to avoid being too predictable
        angle += random.uniform(-0.2, 0.2)
        power += random.uniform(-10, 10)
        power = max(20, min(160, power))
        
        return mcts_ai.Action(angle, power)