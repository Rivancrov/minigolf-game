import exact_physics

print("=== Debugging Training Positions ===")

# Check if training positions are inside obstacles
positions = []

# Recreate the training positions
for x in range(50, 750, 30):
    positions.append((x, 584))

print(f"Checking {len(positions)} ground positions...")
print(f"Ground level y = 584")
print()

# Check each obstacle boundary
print("Obstacle boundaries:")
print(f"Block 1: x={exact_physics.x1}-{exact_physics.x1+exact_physics.width1}, y={exact_physics.y1}-{exact_physics.y1+exact_physics.height1}")
print(f"Block 2: x={exact_physics.x2}-{exact_physics.x2+exact_physics.width2}, y={exact_physics.y2}-{exact_physics.y2+exact_physics.height2}") 
print(f"Block 3: x={exact_physics.x3}-{exact_physics.x3+exact_physics.width3}, y={exact_physics.y3}-{exact_physics.y3+exact_physics.height3}")
print(f"Block 4: x={exact_physics.x4}-{exact_physics.x4+exact_physics.width4}, y={exact_physics.y4}-{exact_physics.y4+exact_physics.height4}")
print(f"Block 5: x={exact_physics.x5}-{exact_physics.x5+exact_physics.width5}, y={exact_physics.y5}-{exact_physics.y5+exact_physics.height5}")
print()

# Test collision detection for each position
problematic_positions = []

for x, y in positions[:10]:  # Just test first 10
    print(f"Position ({x}, {y}):", end=" ")
    
    # Check collision with each surface
    collisions = []
    for i, surface in enumerate(exact_physics.edges):
        if surface.is_collided(x, y):
            collisions.append(f"surface_{i}")
    
    if collisions:
        print(f"❌ COLLIDING with {collisions}")
        problematic_positions.append((x, y))
    else:
        print("✅ Clear")

print()
if problematic_positions:
    print(f"Found {len(problematic_positions)} bad positions!")
    print("This explains why no shots work - ball starts inside obstacles!")
else:
    print("All positions seem clear - issue is elsewhere...")
    
# Also test the collision detection itself
print("\nTesting collision detection logic:")
test_ball = exact_physics.Ball(exact_physics.x1 + 5, exact_physics.y1 + 5)  # Should be inside block 1
print(f"Ball at ({test_ball.x}, {test_ball.y}) inside block 1:")
for i, surface in enumerate(exact_physics.edges):
    if surface.is_collided(test_ball.x, test_ball.y):
        print(f"  Detected collision with surface {i}")
        break
else:
    print("  No collision detected - collision logic broken!")