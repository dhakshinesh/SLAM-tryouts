import pygame
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
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 10)
        
        # Draw the paint shot (line)
        pygame.draw.line(screen, color, (self.x, self.y), (x2, y2), 3)

def create_shooters(data):
    shooters = []
    for shooter_data in data:
        distance, rotation = shooter_data[0]
        x, y = shooter_data[1]
        shooters.append(Shooter(distance, rotation, x, y))
    return shooters

def update_shooters(shooters, data):
    for i, shooter_data in enumerate(data):
        # Get the latest position (last in the list) for each shooter
        latest_data = shooter_data[-2:]
        distance, rotation = latest_data[0]
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

# Nested data with distinct positions
data = [
    [   # Shooter 1
        (100, math.radians(45)), (100, 100),  # Initial position
        (120, math.radians(60)), (200, 150),  # Updated position
        (140, math.radians(75)), (250, 200)   # Further updated position
    ],
    [   # Shooter 2
        (50, math.radians(90)), (300, 400),   # Initial position
        (70, math.radians(120)), (400, 450)    # Updated position
    ],
    [   # Shooter 3
        (80, math.radians(30)), (500, 300),   # Initial position
        (90, math.radians(45)), (600, 350)    # Updated position
    ]
]

# Create shooters from initial data
shooters = create_shooters(data)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update shooters based on latest data
    update_shooters(shooters, data)

    # Fill background (to clear previous frame)
    screen.fill(WHITE)
    
    # Draw each shooter
    for shooter in shooters:
        shooter.draw(screen, RED)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
