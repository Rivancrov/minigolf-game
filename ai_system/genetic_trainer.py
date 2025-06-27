import json
import math
import random
import time
import sys
from collections import namedtuple

# Add path to core_game
sys.path.append('../')
from core_game import exact_physics

# --- Genetic Algorithm Configuration ---
POPULATION_SIZE = 1000
GENERATIONS = 150
MUTATION_RATE = 0.3 # Increased mutation rate for more exploration
CROSSOVER_RATE = 0.7
TOURNAMENT_SIZE = 3 # Reduced selection pressure

# --- Data Structures ---
Individual = namedtuple('Individual', ['angle', 'power'])
Strategy = namedtuple('Strategy', ['angle', 'power', 'win_rate', 'strategy_type'])

class GeneticAITrainer:
    def __init__(self, positions_to_train):
        self.positions = positions_to_train
        self.policy_table = {}

    def train(self):
        """Main training loop to evolve strategies for all positions"""
        start_time = time.time()
        print(f"🧬 Starting genetic evolution for {len(self.positions)} positions...")
        print(f"   Generations per position: {GENERATIONS}")
        print(f"   Population size: {POPULATION_SIZE}")

        for i, (x, y) in enumerate(self.positions):
            pos_start_time = time.time()
            print(f"\nPosition {i+1}/{len(self.positions)}: ({x}, {y})")

            # Evolve the best strategy for this position
            best_strategy = self.evolve_for_position(x, y)

            if best_strategy:
                # Store the best evolved strategy
                state_key = self.discretize_state(x, y)
                if state_key not in self.policy_table:
                    self.policy_table[state_key] = []
                
                self.policy_table[state_key].append(best_strategy._asdict())
                
                pos_time = time.time() - pos_start_time
                print(f"  ✅ Evolution complete in {pos_time:.1f}s. Best win rate: {best_strategy.win_rate:.2f}")
            else:
                print("  ❌ No successful strategy evolved.")

            # Save progress periodically
            if (i + 1) % 5 == 0:
                self.save_policy('ai_policy_progress.json')
                print(f"  💾 Progress saved. {len(self.policy_table)} strategies learned.")

        total_time = time.time() - start_time
        print(f"\n🎉🎉🎉 EVOLUTION COMPLETE! 🎉🎉🎉")
        print(f"   Total time: {total_time / 3600:.2f} hours")
        self.save_policy('ai_policy.json')
        print(f"   Final policy with {len(self.policy_table)} strategies saved to ai_policy.json")

    def evolve_for_position(self, x, y):
        """Run the genetic algorithm for a single position"""
        population = self.create_initial_population()
        best_fitness_so_far = 0

        for gen in range(GENERATIONS):
            # Evaluate fitness of the entire population
            fitness_scores = [self.calculate_fitness(ind, x, y) for ind in population]

            # Create the next generation
            new_population = []
            # Elitism: carry over the best individual
            best_index = fitness_scores.index(max(fitness_scores))
            new_population.append(population[best_index])

            while len(new_population) < POPULATION_SIZE:
                # Selection
                parent1 = self.tournament_selection(population, fitness_scores)
                parent2 = self.tournament_selection(population, fitness_scores)

                # Crossover
                if random.random() < CROSSOVER_RATE:
                    child1, child2 = self.simulated_binary_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2

                # Mutation
                child1 = self.mutate(child1, x, y, max(fitness_scores))
                child2 = self.mutate(child2, x, y, max(fitness_scores))

                new_population.extend([child1, child2])
            
            population = new_population[:POPULATION_SIZE]
            
            current_best_fitness = max(fitness_scores)
            if current_best_fitness > best_fitness_so_far:
                best_fitness_so_far = current_best_fitness
                print(f"    Gen {gen+1}/{GENERATIONS}: New best fitness = {best_fitness_so_far:.3f}")


        # Return the best individual from the final population
        final_fitness = [self.calculate_fitness(ind, x, y) for ind in population]
        best_individual = population[final_fitness.index(max(final_fitness))]
        
        # Determine strategy type
        strategy_type = self.analyze_strategy_type(best_individual, x, y)
        
        return Strategy(
            angle=best_individual.angle,
            power=best_individual.power,
            win_rate=max(final_fitness),
            strategy_type=strategy_type
        )

    def create_initial_population(self):
        """Create a random population of individuals"""
        population = []
        for _ in range(POPULATION_SIZE):
            angle = random.uniform(0, 2 * math.pi)
            power = random.uniform(30, 200)
            population.append(Individual(angle, power))
        return population

    def calculate_fitness(self, individual, x, y):
        """Calculate the fitness of an individual shot"""
        scored, time, final_x, final_y = exact_physics.simulate_complete_shot(x, y, individual.angle, individual.power)

        hole_x = exact_physics.flag_centre - exact_physics.Ball.ball_dimensions / 2
        hole_y = exact_physics.WINDOWY - exact_physics.Ball.ball_dimensions
        
        start_dist = math.sqrt((x - hole_x)**2 + (y - hole_y)**2)

        # If starting exactly at the hole, it's a perfect score
        if start_dist < 1.0: # Use a small epsilon to account for floating point inaccuracies
            return 1.0

        if scored:
            # High fitness for scoring, bonus for faster shots
            return 1.0 - (time / 20.0)

        # If not scored, fitness is based on distance to the hole
        final_dist = math.sqrt((final_x - hole_x)**2 + (final_y - hole_y)**2)

        # Normalize fitness: 0 (no improvement) to 1 (at the hole)
        fitness = 1.0 - (final_dist / start_dist)
        return max(0, fitness) # Ensure fitness is not negative

    def tournament_selection(self, population, fitness_scores):
        """Select the best individual from a random tournament"""
        tournament = random.sample(list(zip(population, fitness_scores)), TOURNAMENT_SIZE)
        tournament.sort(key=lambda item: item[1], reverse=True)
        return tournament[0][0]

    def simulated_binary_crossover(self, parent1, parent2, eta=2.0):
        """More advanced crossover to create more diverse offspring."""
        p1_angle, p1_power = parent1.angle, parent1.power
        p2_angle, p2_power = parent2.angle, parent2.power

        # Angle Crossover
        u = random.random()
        if u <= 0.5:
            beta = (2 * u)**(1 / (eta + 1))
        else:
            beta = (1 / (2 * (1 - u)))**(1 / (eta + 1))
        
        c1_angle = 0.5 * ((1 + beta) * p1_angle + (1 - beta) * p2_angle)
        c2_angle = 0.5 * ((1 - beta) * p1_angle + (1 + beta) * p2_angle)

        # Power Crossover
        u = random.random()
        if u <= 0.5:
            beta = (2 * u)**(1 / (eta + 1))
        else:
            beta = (1 / (2 * (1 - u)))**(1 / (eta + 1))

        c1_power = 0.5 * ((1 + beta) * p1_power + (1 - beta) * p2_power)
        c2_power = 0.5 * ((1 - beta) * p1_power + (1 + beta) * p2_power)

        return Individual(c1_angle, c1_power), Individual(c2_angle, c2_power)


    def mutate(self, individual, x, y, best_fitness):
        """
        Perform physics-aware and adaptive mutation.
        """
        if random.random() > MUTATION_RATE:
            return individual

        # Adaptive mutation: if fitness is high, do fine-tuning. If low, explore.
        if best_fitness > 0.7 and random.random() < 0.5:
            # Fine-tuning mutation
            new_angle = individual.angle + random.uniform(-math.pi / 32, math.pi / 32)
            new_power = individual.power + random.uniform(-10, 10)
        else:
            # Exploratory mutation
            mutation_type = random.choice(['angle', 'power', 'both', 'physics'])
            if mutation_type == 'angle':
                new_angle = individual.angle + random.uniform(-math.pi / 4, math.pi / 4)
                new_power = individual.power
            elif mutation_type == 'power':
                new_angle = individual.angle
                new_power = individual.power + random.uniform(-50, 50)
            elif mutation_type == 'physics':
                 hole_x = exact_physics.flag_centre - exact_physics.Ball.ball_dimensions / 2
                 hole_y = exact_physics.WINDOWY - exact_physics.Ball.ball_dimensions
                 angle_to_hole = math.atan2(hole_y - y, hole_x - x)
                 new_angle = angle_to_hole + random.uniform(-0.1, 0.1)
                 new_power = math.sqrt((hole_x - x)**2 + (hole_y - y)**2) * random.uniform(1.5, 2.5)
            else: # both
                new_angle = random.uniform(0, 2 * math.pi)
                new_power = random.uniform(30, 250)

        # Clamp power to reasonable limits
        new_power = max(20, min(300, new_power))
        
        return Individual(new_angle, new_power)

    def analyze_strategy_type(self, individual, x, y):
        """Analyze the trajectory to classify the strategy"""
        # This is a simplified analysis. A more detailed one would trace the ball's path.
        if exact_physics.is_roll_angle(individual.angle):
            return "safe" # Low-angle shots are usually safe rolls

        # Check for bounces
        # (A more complex implementation would simulate and check for collisions)
        if individual.power > 180:
            return "bounce" # High power shots are likely to bounce

        return "direct"

    def discretize_state(self, x, y):
        """Convert continuous state to discrete buckets for lookup"""
        x_bucket = int(x // 40)
        y_bucket = int(y // 30)
        x_bucket = max(0, min(19, x_bucket))
        y_bucket = max(0, min(19, y_bucket))
        return f"{x_bucket}_{y_bucket}"

    def save_policy(self, filename):
        """Save the learned policy table to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.policy_table, f, indent=2)

def get_training_positions():
    """Generate a list of valid training positions"""
    positions = []
    
    # Ground positions
    for x in range(50, 750, 40):
        positions.append((x, 584))
    
    # Platform positions
    for x in range(10, 90, 25):
        positions.append((x, 484))
    for x in range(310, 540, 40):
        positions.append((x, 284))
    
    # Near hole
    for x in range(650, 720, 20):
        positions.append((x, 584))
        
    # Filter out any positions that start inside an obstacle
    valid_positions = []
    for x, y in positions:
        collision = False
        for surface in exact_physics.edges:
            if surface.is_collided(x, y):
                collision = True
                break
        if not collision:
            valid_positions.append((x, y))
            
    return valid_positions

if __name__ == "__main__":
    training_positions = get_training_positions()
    trainer = GeneticAITrainer(training_positions)
    trainer.train()
