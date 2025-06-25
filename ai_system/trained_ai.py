import json
import math
import random
from typing import Optional
import sys
sys.path.append('../core_game')

class Action:
    def __init__(self, angle, power):
        self.angle = angle
        self.power = power

class GameState:
    def __init__(self, x, y, x_vel, y_vel, stroke_count):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.stroke_count = stroke_count
        self.is_terminal = False
    
    def is_ball_stationary(self):
        """Check if ball is stationary (not moving)"""
        speed = math.sqrt(self.x_vel**2 + self.y_vel**2)
        return speed < 2.0

class PreTrainedAI:
    def __init__(self, policy_file='ai_policy.json'):
        self.policy_table = {}
        self.load_policy(policy_file)
        
    def load_policy(self, policy_file):
        """Load pre-trained policy from file"""
        try:
            with open(policy_file, 'r') as f:
                policy_dict = json.load(f)
            
            # Convert back to usable format with strategy types
            for state_key_str, actions_data in policy_dict.items():
                x_bucket, y_bucket = map(int, state_key_str.split('_'))
                state_key = (x_bucket, y_bucket)
                
                actions = []
                for action_data in actions_data:
                    action = Action(action_data['angle'], action_data['power'])
                    win_rate = action_data['win_rate']
                    strategy_type = action_data.get('strategy_type', 'unknown')
                    actions.append((action, win_rate, strategy_type))
                
                # Sort by win rate (best first)
                actions.sort(key=lambda x: x[1], reverse=True)
                self.policy_table[state_key] = actions
            
            print(f"Loaded AI policy with {len(self.policy_table)} states")
            
        except FileNotFoundError:
            print("No pre-trained policy found. Using random AI.")
            self.policy_table = {}
    
    def discretize_state(self, state):
        """Convert continuous state to discrete buckets for lookup"""
        x_bucket = int(state.x // 40)
        y_bucket = int(state.y // 30)
        
        x_bucket = max(0, min(19, x_bucket))
        y_bucket = max(0, min(19, y_bucket))
        
        return (x_bucket, y_bucket)
    
    def get_best_action(self, game_state) -> Optional[Action]:
        """Get best action from mega-evolved policy with intelligent selection"""
        if not game_state.is_ball_stationary() or game_state.is_terminal:
            return None
        
        state_key = self.discretize_state(game_state)
        
        # Try to find exact match
        if state_key in self.policy_table:
            actions = self.policy_table[state_key]
            if actions:
                # Intelligent strategy selection based on game state
                return self.select_smart_strategy(actions, game_state)
        
        # Try nearest neighbor approach - find closest trained position
        closest_key = self.find_nearest_trained_position(state_key, game_state)
        if closest_key and closest_key in self.policy_table:
            actions = self.policy_table[closest_key]
            if actions:
                print(f"  📍 Using nearest neighbor position {closest_key}")
                return self.select_smart_strategy(actions, game_state)
        
        # Fallback: simple heuristic towards hole
        return self.get_heuristic_action(game_state)
    
    def get_heuristic_action(self, game_state):
        """Fallback heuristic action when no policy available"""
        # Calculate angle towards hole
        hole_x = 800 - 128 + 46  # flag_centre
        hole_y = 600 - 16
        
        dx = hole_x - game_state.x
        dy = hole_y - game_state.y
        
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
    
    def select_smart_strategy(self, actions, game_state):
        """Intelligently select strategy based on game situation"""
        stroke_count = game_state.stroke_count
        
        # Extract actions with strategy types
        strategy_actions = []
        for item in actions:
            if len(item) == 3:  # New format with strategy type
                action, win_rate, strategy_type = item
                strategy_actions.append((action, win_rate, strategy_type))
            else:  # Old format without strategy type
                action, win_rate = item
                strategy_actions.append((action, win_rate, 'unknown'))
        
        # Sort by win rate (already sorted but just in case)
        strategy_actions.sort(key=lambda x: x[1], reverse=True)
        
        # Debug output
        best_action, best_win_rate, best_strategy = strategy_actions[0]
        print(f"  🤖 AI analyzing {len(strategy_actions)} strategies, best: {best_strategy} (win_rate: {best_win_rate:.2f})")
        
        if stroke_count == 0:
            # First shot - prefer high win rate strategies
            hole_in_one_shots = [a for a in strategy_actions if a[1] > 0.9]
            if hole_in_one_shots:
                chosen = random.choice(hole_in_one_shots[:2])
                print(f"  🎯 Going for hole-in-one with {chosen[2]} strategy!")
                return chosen[0]
            
            high_win_actions = [a for a in strategy_actions if a[1] > 0.8]
            if high_win_actions:
                chosen = random.choice(high_win_actions[:2])
                print(f"  ⚡ Aggressive {chosen[2]} strategy (win_rate: {chosen[1]:.2f})")
                return chosen[0]
            
            print(f"  🎮 Using best available: {best_strategy}")
            return best_action
        
        elif stroke_count == 1:
            # Second shot - balance risk/reward  
            good_actions = [a for a in strategy_actions if a[1] > 0.5]
            if good_actions:
                chosen = random.choice(good_actions)
                print(f"  ⚖️ Balanced {chosen[2]} strategy (win_rate: {chosen[1]:.2f})")
                return chosen[0]
            
            print(f"  🎯 Fallback to best: {best_strategy}")
            return best_action
        
        else:
            # Later shots - prefer safer strategies
            safe_strategies = [a for a in strategy_actions if a[2] == 'safe']
            if safe_strategies and random.random() < 0.6:
                chosen = safe_strategies[0]
                print(f"  🛡️ Playing it safe with {chosen[2]} strategy")
                return chosen[0]
            
            # Otherwise use best available
            chosen = strategy_actions[0] if random.random() < 0.7 else random.choice(strategy_actions[:3])
            print(f"  🎲 Using {chosen[2]} strategy (win_rate: {chosen[1]:.2f})")
            return chosen[0]
    
    def find_nearest_trained_position(self, current_key, game_state):
        """Find the nearest trained position using actual distance"""
        if not self.policy_table:
            return None
        
        current_x = current_key[0] * 40 + 20  # Convert bucket back to actual position
        current_y = current_key[1] * 30 + 15
        
        closest_key = None
        min_distance = float('inf')
        
        for trained_key in self.policy_table.keys():
            trained_x = trained_key[0] * 40 + 20
            trained_y = trained_key[1] * 30 + 15
            
            # Calculate actual distance
            distance = ((current_x - trained_x) ** 2 + (current_y - trained_y) ** 2) ** 0.5
            
            if distance < min_distance:
                min_distance = distance
                closest_key = trained_key
        
        print(f"  🎯 Nearest trained position: {closest_key} (distance: {min_distance:.1f})")
        return closest_key

class FastAI:
    """Even simpler AI that just aims towards hole with basic power calculation"""
    
    def get_best_action(self, game_state) -> Optional[Action]:
        if not game_state.is_ball_stationary() or game_state.is_terminal:
            return None
        
        # Calculate angle towards hole
        hole_x = 800 - 128 + 46
        hole_y = 600 - 16
        
        dx = hole_x - game_state.x
        dy = hole_y - game_state.y
        
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