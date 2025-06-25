import exact_physics

print("=== Debugging Scoring Detection ===")

# Test from position very close to hole
hole_x = exact_physics.flag_centre - exact_physics.Ball.ball_dimensions/2
hole_y = exact_physics.WINDOWY - exact_physics.Ball.ball_dimensions

print(f"Hole position: ({hole_x}, {hole_y})")
print(f"Flag centre: {exact_physics.flag_centre}")

# Test 1: Ball right at hole with no velocity
test_ball = exact_physics.Ball(hole_x, hole_y)
test_ball.x_vel = 0
test_ball.y_vel = 0
print(f"Test 1 - Ball at hole: {exact_physics.is_score(test_ball)}")

# Test 2: Ball near hole with low velocity  
test_ball2 = exact_physics.Ball(hole_x + 5, hole_y)
test_ball2.x_vel = 10
test_ball2.y_vel = 10
print(f"Test 2 - Ball near hole: {exact_physics.is_score(test_ball2)}")

# Test 3: Try some actual shots toward hole
print("\nTesting shots toward hole:")
positions_to_test = [(650, 584), (700, 584), (710, 584)]

for start_x, start_y in positions_to_test:
    print(f"\nFrom ({start_x}, {start_y}):")
    
    # Try straight shot toward hole
    angle = 0  # Straight right
    power = 50
    
    scored, time, final_x, final_y = exact_physics.simulate_complete_shot(start_x, start_y, angle, power)
    print(f"  Shot 0°, power 50: scored={scored}, final=({final_x:.0f}, {final_y:.0f})")
    
    # Try angled shot
    import math
    dx = hole_x - start_x
    dy = hole_y - start_y
    angle_to_hole = math.atan2(dy, dx)
    
    scored, time, final_x, final_y = exact_physics.simulate_complete_shot(start_x, start_y, angle_to_hole, 30)
    print(f"  Shot toward hole, power 30: scored={scored}, final=({final_x:.0f}, {final_y:.0f})")

print("\nIf all shots show scored=False, the physics extraction has issues!")