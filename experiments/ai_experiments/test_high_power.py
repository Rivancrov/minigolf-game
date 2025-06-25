import exact_physics
import math

print("=== Testing High Power Shots ===")

x, y = 140, 584
hole_x = exact_physics.flag_centre - exact_physics.Ball.ball_dimensions/2
hole_y = exact_physics.WINDOWY - exact_physics.Ball.ball_dimensions

print(f"Position: ({x}, {y}) → Hole: ({hole_x}, {hole_y})")
print(f"Distance: {math.sqrt((hole_x-x)**2 + (hole_y-y)**2):.0f} pixels")
print()

# Test different power levels
test_powers = [200, 300, 400, 500]
angle = 0.1  # Slight upward angle for flying shot

for power in test_powers:
    print(f"Testing power {power}...")
    scored, time, final_x, final_y = exact_physics.simulate_complete_shot(x, y, angle, power, max_time=8.0)
    distance_to_hole = math.sqrt((final_x - hole_x)**2 + (final_y - hole_y)**2)
    
    print(f"  Result: scored={scored}, final=({final_x:.0f}, {final_y:.0f}), distance_to_hole={distance_to_hole:.0f}")
    
    if scored:
        print(f"  🎯 SUCCESS! Found working shot: angle={math.degrees(angle):.1f}°, power={power}")
        break

print()
print("If any shot scored=True, then physics works and we just need higher power in training!")