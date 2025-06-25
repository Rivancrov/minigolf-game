import math

# Headless version of your physics - no pygame needed!
class HeadlessPhysics:
    def __init__(self):
        # Copy constants from game.py
        self.WINDOWX = 800
        self.WINDOWY = 600
        self.GRAVITY = -9.8
        self.ball_dimensions = 16
        self.flag_centre = self.WINDOWX - (128 - 46)
        
        # Obstacle positions (from game.py)
        self.x1, self.y1, self.height1, self.width1 = 200, 400, 200, 10
        self.x2, self.y2, self.height2, self.width2 = 0, 500, 10, 100  
        self.x3, self.y3, self.height3, self.width3 = 300, 300, 10, 250
        self.x4, self.y4, self.height4, self.width4 = 600, 500, 100, 15
        self.x5, self.y5, self.height5, self.width5 = 670, 500, 100, 15
    
    def is_roll_angle(self, angle):
        """Check if angle is small enough for rolling"""
        return (angle >= 0 and angle < math.pi/36) or \
               (angle > math.pi*71/36 and angle <= math.pi*2) or \
               (angle > math.pi*35/36 and angle < math.pi*37/36)
    
    def is_collision(self, x, y):
        """Check if ball collides with any obstacle"""
        # Check all obstacles
        obstacles = [
            (self.x1, self.y1, self.width1, self.height1),
            (self.x2, self.y2, self.width2, self.height2), 
            (self.x3, self.y3, self.width3, self.height3),
            (self.x4, self.y4, self.width4, self.height4),
            (self.x5, self.y5, self.width5, self.height5)
        ]
        
        for ox, oy, ow, oh in obstacles:
            if (ox <= x <= ox + ow) and (oy <= y <= oy + oh):
                return True
        
        # Check boundaries
        if x < 0 or x > self.WINDOWX or y < 0 or y > self.WINDOWY:
            return True
            
        return False
    
    def is_scored(self, x, y, vx, vy):
        """Check if ball scored"""
        hole_x = self.flag_centre - self.ball_dimensions/2
        hole_y = self.WINDOWY - self.ball_dimensions
        
        distance = math.sqrt((x - hole_x)**2 + (y - hole_y)**2)
        speed = math.sqrt(vx**2 + vy**2)
        
        return distance < 15 and speed < 80
    
    def simulate_shot(self, start_x, start_y, angle, power, max_time=5.0):
        """Simulate a complete shot without graphics"""
        x, y = start_x, start_y
        
        # Determine initial velocity based on angle and rolling
        if self.is_roll_angle(angle):
            # Rolling shot
            if math.cos(angle) >= 0:
                vx = power / 2
            else:
                vx = -power / 2
            vy = 0
            rolling = True
        else:
            # Flying shot  
            vx = math.cos(angle) * power / 3
            vy = math.sin(angle) * power / 3
            rolling = False
        
        time = 0
        dt = 0.05  # Small time step
        
        while time < max_time:
            # Update position
            if rolling:
                # Simple rolling physics with friction
                friction = 0.7
                acceleration = friction * self.GRAVITY
                
                if abs(vx) < 2:
                    break  # Ball stopped
                    
                x += vx * dt
                if vx > 0:
                    vx = max(0, vx + acceleration * dt)
                else:
                    vx = min(0, vx - acceleration * dt)
                    
            else:
                # Projectile motion
                x += vx * dt
                y += vy * dt
                vy += self.GRAVITY * dt
                
                # Check if ball lands (simplified)
                if y >= self.WINDOWY - self.ball_dimensions:
                    y = self.WINDOWY - self.ball_dimensions
                    vy = 0
                    rolling = True
                    # Energy loss on landing
                    vx *= 0.8
            
            # Check collisions (simplified)
            if self.is_collision(x, y):
                # Simple bounce - reverse velocity with energy loss
                vx *= -0.6
                vy *= -0.6
                # Move out of collision
                x = max(0, min(self.WINDOWX, x))
                y = max(0, min(self.WINDOWY, y))
            
            # Check scoring
            if self.is_scored(x, y, vx, vy):
                return True, time, x, y
            
            time += dt
        
        return False, time, x, y

# Test the headless physics
if __name__ == "__main__":
    physics = HeadlessPhysics()
    
    # Test a shot
    scored, time, final_x, final_y = physics.simulate_shot(100, 584, 0.5, 100)
    print(f"Shot result: scored={scored}, time={time:.2f}s, final_pos=({final_x:.1f}, {final_y:.1f})")