import pygame
import sys

# Initialize Pygame
pygame.init()

# Set frames per second
FPS = 600

# Set surface dimensions
surface_width = 512
surface_height = 512
surface_size = (surface_width, surface_height)

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create fullscreen window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Set display dimensions
screen_width = screen.get_width()  # Adjust according to your screen resolution
screen_height = screen.get_height()  # Adjust according to your screen resolution
screen_size = (screen_width, screen_height)

# Create surface
box = pygame.Surface(surface_size)
box.fill(WHITE)

# Center surface on the screen
surface_rect = box.get_rect(center=screen.get_rect().center)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main loop
running = True
mouse_pos = ()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                box.fill(WHITE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If mouse button is down, set mouse_pos relative to the center of the surface
            mouse_pos = pygame.mouse.get_pos()
            # Adjust mouse_pos relative to the center of the surface
            mouse_pos = (mouse_pos[0] - (surface_rect.center[0] - surface_rect.left),
                         mouse_pos[1] - (surface_rect.center[1] - surface_rect.top))
        elif event.type == pygame.MOUSEBUTTONUP:
            # If mouse button is up, reset mouse_pos
            mouse_pos = ()
        elif event.type == pygame.MOUSEMOTION:
            # Update mouse_pos while dragging the mouse
            if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
                mouse_pos = pygame.mouse.get_pos()
                # Adjust mouse_pos relative to the center of the surface
                mouse_pos = (mouse_pos[0] - (surface_rect.center[0] - surface_rect.left),
                             mouse_pos[1] - (surface_rect.center[1] - surface_rect.top))

    if mouse_pos:
        pygame.draw.circle(box, BLACK, mouse_pos, 3)

    # Fill screen with black
    screen.fill(BLACK)

    # Blit the surface onto the screen
    screen.blit(box, surface_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
