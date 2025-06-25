import math

# Exact copy of your physics without pygame drawing
WINDOWX, WINDOWY = 800, 600
GRAVITY = -9.8

# Ball class (physics only)
class Ball:
    ball_dimensions = 16
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.fire_state = False
        self.rolling_state = False

    def ball_projectile(self, time, start_x, start_y, start_x_vel, start_y_vel):
        # SUVAT equations (exact copy)
        new_y_vel = int(start_y_vel + GRAVITY * time)
        y = int(start_y - (start_y_vel * time + (GRAVITY / 2 * (time) ** 2)))
        x = int(start_x_vel * time + start_x)
        return (x, y, int(start_x_vel), new_y_vel)

    def roll(self, surface, time, start_x, start_v):
        # Exact copy of your rolling physics
        acceleration = surface.coeff_of_friction * GRAVITY
        if start_v > 0:
            x = (start_v * time + (time ** 2) * acceleration / 2) + start_x
            new_v_sqred = (start_v) ** 2 + 2 * acceleration * (abs(x - start_x))
            if new_v_sqred < 0:
                new_v_sqred = 0
            new_v = math.sqrt(new_v_sqred)
        elif start_v < 0:
            x = (start_v * time - (time ** 2) * acceleration / 2) + start_x
            new_v_sqred = (start_v) ** 2 + 2 * acceleration * (abs(x - start_x))
            if new_v_sqred < 0:
                new_v_sqred = 0
            new_v = -math.sqrt(new_v_sqred)
        else:
            x = start_x
            new_v = start_v
        return (int(x), int(new_v))

# Vector functions (exact copy)
def scalar_product(v1, v2):
    x_comp = v1[0] * v2[0]
    y_comp = v1[1] * v2[1]
    scalar_product = x_comp + y_comp
    return (scalar_product)

def get_magnitude(v):
    magnitude = math.sqrt((v[0]) ** 2 + (v[1]) ** 2)
    return magnitude

def get_unit_v(vector):
    magnitude = get_magnitude(vector)
    if magnitude != 0:
        x = vector[0] / magnitude
        y = vector[1] / magnitude
    else:
        x = 0
        y = 0
    return (x, y)

# Surface class (exact copy)
class Surface:
    def __init__(self, start_x, start_y, end_x, end_y, restitution, para_v, perp_v, cof):
        self.restitution = restitution
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.para_vector = para_v
        self.perp_vector = perp_v
        self.coeff_of_friction = cof

    def is_collided(self, x, y):
        # Exact copy of collision detection
        if x in range(self.start_x, self.end_x):
            if y in range(self.start_y, self.end_y):
                return True
        return False

    def bounce(self, ball):
        # Exact copy of bounce physics
        ball_vector = (ball.x_vel, ball.y_vel)
        para_projection = scalar_product(ball_vector, self.para_vector)
        perp_projection = scalar_product(ball_vector, self.perp_vector)
        v1_x = para_projection * self.para_vector[0]
        v1_y = para_projection * self.para_vector[1]
        v2_x = -self.restitution * perp_projection * self.perp_vector[0]
        v2_y = -self.restitution * perp_projection * self.perp_vector[1]
        x_vel = v1_x + v2_x
        y_vel = v1_y + v2_y
        return (x_vel, y_vel)

    def add_after_collision(self, ball, difference):
        # Exact copy of collision position correction
        amount_to_add = abs(difference)
        ball_vector = (ball.x_vel, ball.y_vel)
        perp_projection = scalar_product(ball_vector, self.perp_vector)
        v_x = -perp_projection * self.perp_vector[0]
        v_y = -perp_projection * self.perp_vector[1]
        ball_vector = get_unit_v((v_x, v_y))
        x_addition = amount_to_add * ball_vector[0] + ball_vector[0]
        y_addition = amount_to_add * ball_vector[1] + ball_vector[1]
        return (x_addition, y_addition)

# Obstacle positions (exact copy from your game)
x1, y1, height1, width1 = 200, 400, 200, 10
x2, y2, height2, width2 = 0, 500, 10, 100
x3, y3, height3, width3 = 300, 300, 10, 250
x4, y4, height4, width4 = 600, 500, 100, 15
x5, y5, height5, width5 = 670, 500, 100, 15

flag_dimensions = 128
flag_centre = WINDOWX - (flag_dimensions - 46)
sand_dimensions = 64

# Surface objects (exact copy from your game)
bottom_edge = Surface(0, WINDOWY - Ball.ball_dimensions + 1, WINDOWX, WINDOWY * 10, 0.6, (1, 0), (0, 1), 0.7)
left_edge = Surface(0 - WINDOWX * 10, -WINDOWY * 10, 0, WINDOWY * 10, 0.9, (0, 1), (1, 0), 0)
right_edge = Surface(WINDOWX, 0, WINDOWX * 10 + Ball.ball_dimensions, WINDOWY * 10, 0.9, (0, 1), (-1, 0), 0)
top_edge = Surface(0, 0, WINDOWX, 20, 0.9, (1, 0), (0, -1), 0)
sand_edge = Surface(WINDOWX - flag_dimensions - sand_dimensions + 7, WINDOWY - sand_dimensions + 5, WINDOWX - flag_dimensions, WINDOWY, 0, (1, 0), (0, 1), 10)

# Wooden blocks
block_1 = Surface(x1 - Ball.ball_dimensions, y1, x1 + Ball.ball_dimensions, y1 + height1, 0.6, (0, 1), (-1, 0), 0)
block_2 = Surface(x2, y2 - Ball.ball_dimensions, x2 + width2, y2 + Ball.ball_dimensions, 0.6, (1, 0), (0, 1), 0.7)
block_3 = Surface(x3, y3 - Ball.ball_dimensions, x3 + width3, y3 + Ball.ball_dimensions, 0.6, (1, 0), (0, 1), 0.7)
block_4 = Surface(x4 - Ball.ball_dimensions, y4, x4 + width4, y4 + height4, 0.8, (0, 1), (-1, 0), 0)
block_5 = Surface(x5, y5, x5 + width4, y5 + height5, 0.8, (0, 1), (-1, 0), 0)

edges = [left_edge, right_edge, top_edge, bottom_edge, block_1, block_2, block_3, block_4, block_5, sand_edge]
roll_edges = [bottom_edge, block_2, block_3, sand_edge]

# Exact copy of your utility functions
def is_roll_angle(angle):
    if angle >= 0 and angle < math.pi * 1 / 36:
        return True
    if angle > math.pi * 71 / 36 and angle <= math.pi * 2:
        return True
    if angle > math.pi * 35 / 36 and angle < math.pi * 37 / 36:
        return True
    return False

def is_score(ball):
    x_change = ball.x - (flag_centre - Ball.ball_dimensions / 2)
    y_change = ball.y - (WINDOWY - Ball.ball_dimensions)
    distance = get_magnitude((x_change, y_change))
    speed = get_magnitude((ball.x_vel, ball.y_vel))
    if distance < 15 and speed < 80:
        return True
    return False

def find_difference(ball, edge):
    # Exact copy of your difference calculation
    if edge == bottom_edge:
        difference = ball.y - (bottom_edge.start_y)
    elif edge == left_edge:
        difference = ball.x - left_edge.end_x
    elif edge == right_edge:
        difference = ball.x - right_edge.start_x
    elif edge == top_edge:
        difference = ball.y - top_edge.end_y
    elif edge == sand_edge:
        difference = ball.y - (sand_edge.start_y)
    elif edge == block_1:
        if ball.x_vel > 0:
            difference = ball.x - block_1.start_x
        else:
            difference = ball.x - block_1.end_x
    elif edge == block_2:
        if ball.y_vel > 0:
            difference = ball.y - block_2.end_y
        else:
            difference = ball.y - block_2.start_y
    elif edge == block_3:
        if ball.y_vel > 0:
            difference = ball.y - block_3.end_y
        else:
            difference = ball.y - block_3.start_y
    elif edge == block_4:
        if ball.x_vel > 0:
            difference = ball.x - block_4.start_x
        else:
            difference = ball.x - block_4.end_x
    elif edge == block_5:
        if ball.x_vel > 0:
            difference = ball.x - block_5.start_x
        else:
            difference = ball.x - block_5.end_x
    else:
        difference = 0
    return difference

# Exact copy of your physics simulation functions
def shoot_ball(ball, time, start_x, start_y, start_x_vel, start_y_vel):
    hit = False
    edge = None
    
    # Check for collision
    for surface in edges:
        if surface.is_collided(int(ball.x), int(ball.y)):
            hit = True
            edge = surface
            break
    
    # No collision - call projectile
    if not hit:
        stats = ball.ball_projectile(time, start_x, start_y, start_x_vel, start_y_vel)
        ball.x = stats[0]
        ball.y = stats[1] 
        ball.x_vel = stats[2]
        ball.y_vel = stats[3]
    # Collision and bouncing conditions
    elif abs(ball.y_vel) > 10 or (edge not in roll_edges):
        difference = find_difference(ball, edge)
        sum_vals = edge.add_after_collision(ball, difference)
        ball.x = ball.x + sum_vals[0]
        ball.y = ball.y - sum_vals[1]
        stats = edge.bounce(ball)
        ball.x_vel = stats[0]
        ball.y_vel = stats[1]
        start_x_vel = ball.x_vel
        start_y_vel = ball.y_vel
        start_x = ball.x
        start_y = ball.y
        time = 0
    # Collision but start rolling
    else:
        ball.fire_state = False
        ball.rolling_state = True
        difference = find_difference(ball, edge)
        sum_vals = edge.add_after_collision(ball, difference)
        ball.y = ball.y - sum_vals[1]
        ball.x = ball.x + sum_vals[0]
        ball.y_vel = 0
        start_x = ball.x
        start_y = ball.y
        start_x_vel = ball.x_vel
        start_y_vel = ball.y_vel
        time = 0
    
    return (time, start_x, start_y, edge, start_x_vel, start_y_vel)

def roll_ball(roll_surface, ball, time, start_x, start_v):
    hit = False
    edge = None
    
    for surface in edges:
        if surface.is_collided(int(ball.x), int(ball.y)):
            hit = True
            edge = surface
            break
    
    # Roll ball if hasn't collided and on top of something
    if not hit and roll_surface.is_collided(int(ball.x), int(ball.y) + 10):
        stats = ball.roll(roll_surface, time, start_x, start_v)
        ball.x = stats[0]
        ball.x_vel = stats[1]
    # Call fire state if hasn't collided and nothing below
    elif not hit and not roll_surface.is_collided(int(ball.x), int(ball.y) + 10):
        ball.rolling_state = False
        ball.fire_state = True
        time = 0
        start_v = ball.x_vel
        start_x = ball.x
    # Has collided - modify position and velocity
    else:
        difference = find_difference(ball, edge)
        sum_vals = edge.add_after_collision(ball, difference)
        ball.x = int(ball.x + sum_vals[0])
        ball.y = int(ball.y - sum_vals[1])
        stats = edge.bounce(ball)
        ball.x_vel = stats[0]
        ball.y_vel = stats[1]
        start_x = ball.x
        start_v = ball.x_vel
        time = 0
    
    return (time, start_x, start_v)

def simulate_complete_shot(start_x, start_y, angle, power, max_time=10.0):
    """Simulate a complete shot using your exact physics with safety checks"""
    import time as time_module
    simulation_start = time_module.time()
    
    ball = Ball(start_x, start_y)
    
    # Set initial state based on angle
    if is_roll_angle(angle):
        ball.rolling_state = True
        ball.fire_state = False
        if math.cos(angle) >= 0:
            ball.x_vel = power / 2
        else:
            ball.x_vel = -power / 2
        ball.y_vel = 0
        # Find initial roll surface
        edge = bottom_edge
        for surface in edges:
            if surface.is_collided(ball.x, ball.y + 5):
                edge = surface
                break
    else:
        ball.fire_state = True
        ball.rolling_state = False
        ball.x_vel = math.cos(angle) * power / 3
        ball.y_vel = math.sin(angle) * power / 3
        edge = None
    
    time = 0
    start_x_val = ball.x
    start_y_val = ball.y
    start_x_vel = ball.x_vel
    start_y_vel = ball.y_vel
    
    # Simulate until ball stops or scores with real-time timeout
    iterations = 0
    max_iterations = 1000  # Prevent infinite loops
    
    while time < max_time and iterations < max_iterations:
        iterations += 1
        
        # Real-time timeout check (every 100 iterations)
        if iterations % 100 == 0:
            elapsed = time_module.time() - simulation_start
            if elapsed > 3.0:  # 3 second real-time limit
                break
        
        if ball.fire_state:
            time += 0.15
            stats = shoot_ball(ball, time, start_x_val, start_y_val, start_x_vel, start_y_vel)
            time = stats[0]
            start_x_val = stats[1]
            start_y_val = stats[2]
            start_x_vel = stats[4]
            start_y_vel = stats[5]
            edge = stats[3]
            
        elif ball.rolling_state:
            time += 0.15
            stats = roll_ball(edge, ball, time, start_x_val, start_x_vel)
            time = stats[0]
            start_x_val = stats[1]
            start_x_vel = stats[2]
            start_y_vel = 0
            start_y_val = ball.y
            
            if abs(ball.x_vel) < 2:
                ball.x_vel = 0
                ball.rolling_state = False
                break
        else:
            break
        
        # Check if scored
        if is_score(ball):
            return True, time, ball.x, ball.y
        
        # Safety check - if ball out of bounds or stuck
        if (ball.x < -200 or ball.x > WINDOWX + 200 or 
            ball.y < -200 or ball.y > WINDOWY + 200):
            break
            
        # Check if ball is stuck (same position for too long)
        if iterations > 500:  # After many iterations
            speed = get_magnitude((ball.x_vel, ball.y_vel))
            if speed < 0.1:  # Ball barely moving
                break
    
    return False, time, ball.x, ball.y

# Test the exact physics
if __name__ == "__main__":
    print("Testing exact physics simulation...")
    
    # Test shot from starting position
    scored, time, final_x, final_y = simulate_complete_shot(100, 584, 0.5, 100)
    print(f"Shot 1: scored={scored}, time={time:.2f}s, final=({final_x:.1f}, {final_y:.1f})")
    
    # Test shot that should hit obstacle
    scored, time, final_x, final_y = simulate_complete_shot(100, 584, 0, 150)
    print(f"Shot 2: scored={scored}, time={time:.2f}s, final=({final_x:.1f}, {final_y:.1f})")
    
    print("Exact physics working!")