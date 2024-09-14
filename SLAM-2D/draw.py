import pygame
from operator import itemgetter
import math

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
        pygame.draw.circle(screen, (0,0,255), (int(self.x), int(self.y)), 5)
        
        # Draw the paint shot (line)
        if self.distance != 100:
            pygame.draw.circle(screen, color,(x2, y2), 3)


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


def create_shooters(data):
    shooters = []
    for shooter_data in data:
        shooters.append(Shooter(shooter_data[0], shooter_data[1], shooter_data[2][0], shooter_data[2][1]))
    return shooters


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

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Shooter Simulation")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create shooters from initial data
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

# Quit Pygame
pygame.quit()
