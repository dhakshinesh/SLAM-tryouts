import pygame
import math
import random

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
                    print("detected", depth)
                    break
                pygame.draw.line(screen, WHITE, (self.x, self.y), (target_x, target_y), 1)
            vision.append((max_depth, ray_angle))
        vision.append((self.x, self.y))
        vision.append(self.angle)
        return vision

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
        file.write(str(player.raycast(screen, map_data))+'\n')

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
file = open("SLAM_data.txt", "a")
file.seek(0)
file.truncate()
game_loop()
