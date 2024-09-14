import pygame
import math
import random
from operator import itemgetter

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
tile_size = 40  # Size of each tile
screen = pygame.display.set_mode((screen_width, screen_height))

# Calculate the number of tiles based on screen size and tile size
map_width = screen_width // tile_size
map_height = screen_height // tile_size

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create an empty map (0 for open space, 1 for walls)
map_data = [[0 if (x > 0 and x < map_width - 1 and y > 0 and y < map_height - 1) else 1
             for x in range(map_width)] for y in range(map_height)]

# Number of boxes to place randomly
num_boxes = 30  # Adjust this to control how many boxes to place

# Randomly place boxes (represented by 1) in open space
for _ in range(num_boxes):
    while True:
        rand_x = random.randint(1, map_width - 2)  # Avoid placing at the edges
        rand_y = random.randint(1, map_height - 2)
        
        # Only place a box if it's currently an open space
        if map_data[rand_y][rand_x] == 0:
            map_data[rand_y][rand_x] = 1  # Place a box
            break  # Break the loop once a box is placed

# Player (Camera) class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Player's direction (in degrees)
        self.speed = 2

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Convert to map grid coordinates to check for collisions
        grid_x = int(new_x // tile_size)
        grid_y = int(new_y // tile_size)
        # Check if new position is within bounds and not hitting a wall
        if 0 <= grid_x < map_width and 0 <= grid_y < map_height:
            if map_data[grid_y][grid_x] == 0:  # Only move if it's an open space
                self.x = new_x
                self.y = new_y

    def rotate(self, da):
        self.angle += da

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 10)

    # Raycasting logic to simulate vision
    def raycast(self, screen, map_data):
        vision = []
        for ray in range(-30, 30):  # Number of rays for FOV
            ray_angle = math.radians(self.angle + ray)
            max_depth = 0
            for depth in range(100):  # Ray length (vision depth)
                target_x = int(self.x + math.cos(ray_angle) * depth)
                target_y = int(self.y + math.sin(ray_angle) * depth)

                # Convert to map grid coordinates
                grid_x = target_x // tile_size
                grid_y = target_y // tile_size
                
                if depth > max_depth:
                    max_depth = depth + 1 

                # Check if the ray is out of bounds
                if not (0 <= grid_x < map_width and 0 <= grid_y < map_height):
                    break  # Stop if the ray goes out of bounds
                
                # Stop ray if it hits a wall
                if map_data[grid_y][grid_x] == 1:  # Wall detected
                    break
                pygame.draw.line(screen, WHITE, (self.x, self.y), (target_x, target_y), 1)
            vision.append((max_depth, ray_angle))
        vision.append((self.x, self.y))
        vision.append(self.angle)
        return vision

# Shooter class
class Shooter:
    def __init__(self, distance, rotation, x, y):
        self.distance = distance
        self.rotation = rotation
        self.x = x
        self.y = y
    
    def update_position(self, x, y):
        self.x = x
        self.y = y

    def update_rotation(self, rotation):
        self.rotation = rotation

    def update_distance(self, distance):
        self.distance = distance
    
    def draw(self, screen, color):
        # Calculate endpoint of the paint shot
        x2 = self.x + self.distance * math.cos(self.rotation)
        y2 = self.y + self.distance * math.sin(self.rotation)
        
        # Draw the shooter (a simple circle)
        pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), 5)
        
        # Draw the paint shot (line)
        if self.distance != 100:
            pygame.draw.circle(screen, color, (x2, y2), 3)

# Draw the 2D grid map
def draw_map(screen, map_data):
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            tile_color = GREY if map_data[row][col] == 1 else BLACK
            pygame.draw.rect(screen, tile_color, pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size))

# Main game loop
def game_loop():
    player = Player(screen_width // 2, screen_height // 2)
    
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement (example: arrow keys)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rotate(-2)
        if keys[pygame.K_RIGHT]:
            player.rotate(2)
        if keys[pygame.K_UP]:
            player.move(math.cos(math.radians(player.angle)), math.sin(math.radians(player.angle)))
        if keys[pygame.K_DOWN]:
            player.move(-math.cos(math.radians(player.angle)), -math.sin(math.radians(player.angle)))

        # Drawing and game updates
        screen.fill(BLACK)
        draw_map(screen, map_data)
        player.draw(screen)
        slam_data = player.raycast(screen, map_data)
        file.write(str(slam_data) + '\n')

        pygame.display.flip()
        clock.tick(60)

    # Close file and quit Pygame
    file.close()
    pygame.quit()

# Shooter data management
def manage_shooter_data():
    with open('SLAM_data.txt') as f:
        lines = f.read().splitlines()
        shooter_data = [eval(i) for i in lines]

    final_data = []
    for x in range(60):
        final_data.append([])
        shooter = list(map(itemgetter(x), shooter_data))
        distances = []
        angles = []
        for y in shooter:
            distances.append(y[0])
            angles.append(y[1])
        final_data[x].append(distances)
        final_data[x].append(angles)

    for x in final_data:
        x.append(shooter_data[-2])
    
    return final_data

# Create shooters from data
def create_shooters(data):
    shooters = []
    for shooter_data in data:
        shooters.append(Shooter(shooter_data[0], shooter_data[1], shooter_data[2][0], shooter_data[2][1]))
    return shooters

# Update shooters from data
def update_shooters(shooters, data):
    for i, shooter in enumerate(data):
        # Get the latest position (last in the list) for each shooter
        latest_data = shooter[-3:]
        distance = latest_data[0][0]
        rotation = latest_data[0][1]
        x, y = latest_data[1]
        shooters[i].update_distance(distance)
        shooters[i].update_rotation(rotation)
        shooters[i].update_position(x, y)

# Shooter simulation loop
def shooter_simulation_loop():
    shooter_data = manage_shooter_data()
    shooters = create_shooters(shooter_data)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update shooters based on latest data
        update_shooters(shooters, shooter_data)

        # Fill background (to clear previous frame)
        screen.fill(WHITE)
        
        # Draw each shooter
        for shooter in shooters:
            shooter.draw(screen, RED)
        
        # Update the display
        pygame.display.flip()

# Open SLAM data file for writing
file = open("SLAM_data.txt", "a")
file.seek(0)
file.truncate()

# Run game loop first, then shooter simulation loop
game_loop()
shooter_simulation_loop()
