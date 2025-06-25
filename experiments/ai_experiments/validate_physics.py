import exact_physics

print("=== Physics Validation Test ===")
print("Testing if extracted physics matches your game behavior")
print()

# Test 1: Basic shot that should work
print("Test 1: Basic shot towards hole")
scored, time, final_x, final_y = exact_physics.simulate_complete_shot(100, 584, 0.5, 80)
print(f"Result: scored={scored}, time={time:.1f}s, final_pos=({final_x:.0f}, {final_y:.0f})")
print(f"Expected: Ball should move towards hole, may or may not score")
print()

# Test 2: Shot directly at obstacle (should bounce/stop)
print("Test 2: Shot directly at wooden block")
scored, time, final_x, final_y = exact_physics.simulate_complete_shot(100, 584, 0, 120)  # Straight right
print(f"Result: scored={scored}, time={time:.1f}s, final_pos=({final_x:.0f}, {final_y:.0f})")
print(f"Expected: Ball should hit obstacle around x=200, bounce back or stop")
print()

# Test 3: Rolling shot (low angle)
print("Test 3: Rolling shot (low angle)")
scored, time, final_x, final_y = exact_physics.simulate_complete_shot(100, 584, 0.05, 60)  # Very low angle
print(f"Result: scored={scored}, time={time:.1f}s, final_pos=({final_x:.0f}, {final_y:.0f})")
print(f"Expected: Ball should roll along ground")
print()

# Test 4: Check if surfaces are loaded correctly
print("Test 4: Surface configuration check")
print(f"Number of edges: {len(exact_physics.edges)}")
print(f"Number of roll edges: {len(exact_physics.roll_edges)}")
print(f"Hole position: ({exact_physics.flag_centre:.0f}, {exact_physics.WINDOWY - exact_physics.Ball.ball_dimensions})")
print()

# Test 5: Scoring detection
print("Test 5: Shot very close to hole")
hole_x = exact_physics.flag_centre - exact_physics.Ball.ball_dimensions/2
hole_y = exact_physics.WINDOWY - exact_physics.Ball.ball_dimensions
scored, time, final_x, final_y = exact_physics.simulate_complete_shot(hole_x - 20, hole_y, 0, 30)
print(f"Result: scored={scored}, time={time:.1f}s, final_pos=({final_x:.0f}, {final_y:.0f})")
print(f"Expected: Should score or get very close to hole at ({hole_x:.0f}, {hole_y})")
print()

print("=== Validation Complete ===")
print("If these results look reasonable, the physics extraction worked!")
print("Look for:")
print("- Obstacle bounces/stops around x=200")
print("- Ball movement makes sense")
print("- Close shots near hole should score")
print("- No crashes or infinite loops")