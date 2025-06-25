import exact_physics
import math

print("=== Deep Debug of Position 4: (140, 584) ===")

# Test a single shot in detail
x, y = 140, 584
print(f"Starting position: ({x}, {y})")
print(f"Hole position: ({exact_physics.flag_centre - exact_physics.Ball.ball_dimensions/2}, {exact_physics.WINDOWY - exact_physics.Ball.ball_dimensions})")
print()

# Test 1: Simple shot toward hole
hole_x = exact_physics.flag_centre - exact_physics.Ball.ball_dimensions/2
hole_y = exact_physics.WINDOWY - exact_physics.Ball.ball_dimensions
dx = hole_x - x
dy = hole_y - y
angle_to_hole = math.atan2(dy, dx)

print(f"Distance to hole: {math.sqrt(dx*dx + dy*dy):.1f}")
print(f"Angle to hole: {math.degrees(angle_to_hole):.1f}°")
print()

# Try the shot with detailed step-by-step tracking
print("Testing shot: angle={:.2f} rad ({:.1f}°), power=60".format(angle_to_hole, math.degrees(angle_to_hole)))

# Create ball and set initial state
ball = exact_physics.Ball(x, y)
power = 60

# Determine initial velocity
if exact_physics.is_roll_angle(angle_to_hole):
    print("Shot will ROLL")
    ball.rolling_state = True
    ball.fire_state = False
    if math.cos(angle_to_hole) >= 0:
        ball.x_vel = power / 2
    else:
        ball.x_vel = -power / 2
    ball.y_vel = 0
else:
    print("Shot will FLY")
    ball.fire_state = True
    ball.rolling_state = False
    ball.x_vel = math.cos(angle_to_hole) * power / 3
    ball.y_vel = math.sin(angle_to_hole) * power / 3

print(f"Initial velocity: ({ball.x_vel:.1f}, {ball.y_vel:.1f})")
print()

# Simulate step by step
time = 0
max_steps = 20
step = 0

print("Step-by-step simulation:")
while step < max_steps and time < 5.0:
    step += 1
    old_x, old_y = ball.x, ball.y
    old_vx, old_vy = ball.x_vel, ball.y_vel
    
    print(f"Step {step}: pos=({ball.x:.1f}, {ball.y:.1f}), vel=({ball.x_vel:.1f}, {ball.y_vel:.1f}), fire={ball.fire_state}, roll={ball.rolling_state}")
    
    # Check if scored before moving
    if exact_physics.is_score(ball):
        print(f"  🎯 SCORED!")
        break
    
    # Check if stopped
    if not ball.fire_state and not ball.rolling_state and abs(ball.x_vel) < 2 and abs(ball.y_vel) < 2:
        print(f"  ⏹️  Ball stopped")
        break
    
    # Simulate one step
    if ball.fire_state:
        time += 0.15
        try:
            stats = exact_physics.shoot_ball(ball, time, old_x, old_y, old_vx, old_vy)
            time = stats[0]
            print(f"  Flying: new_time={time:.2f}")
        except Exception as e:
            print(f"  ❌ Error in shoot_ball: {e}")
            break
            
    elif ball.rolling_state:
        time += 0.15
        edge = exact_physics.bottom_edge  # Assume rolling on ground
        try:
            stats = exact_physics.roll_ball(edge, ball, time, old_x, old_vx)
            time = stats[0]
            print(f"  Rolling: new_time={time:.2f}")
            
            if abs(ball.x_vel) < 2:
                ball.x_vel = 0
                ball.rolling_state = False
                print(f"  Rolling stopped")
        except Exception as e:
            print(f"  ❌ Error in roll_ball: {e}")
            break
    else:
        print(f"  Ball in unknown state")
        break
    
    # Check for infinite position
    if ball.x == old_x and ball.y == old_y and ball.x_vel == old_vx and ball.y_vel == old_vy:
        print(f"  ⚠️  Ball stuck - no movement")
        break

print(f"\nFinal: pos=({ball.x:.1f}, {ball.y:.1f}), scored={exact_physics.is_score(ball)}")

# Test scoring detection specifically
print(f"\nScoring test:")
print(f"Distance to hole: {math.sqrt((ball.x - hole_x)**2 + (ball.y - hole_y)**2):.1f}")
print(f"Ball speed: {math.sqrt(ball.x_vel**2 + ball.y_vel**2):.1f}")
print(f"Scoring threshold: distance < 15 and speed < 80")
print(f"Should score: {exact_physics.is_score(ball)}")