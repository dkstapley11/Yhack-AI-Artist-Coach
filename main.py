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
RED = (255, 0, 0)

# Create fullscreen window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()

# Create surface
box = pygame.Surface(surface_size)
box.fill(WHITE)

# Center surface on the screen
surface_rect = box.get_rect(center=screen.get_rect().center)
screen_rect = pygame.Rect((0, 0), (screen_width, screen_height))

# Set the dimensions and psosition of the exit button
square_size = 25
square_rect = pygame.Rect(screen_width - square_size, 0, square_size, square_size)

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
            # Check if the mouse click occurs within the boundaries of the red square
            if screen_width - square_size <= mouse_pos[0] <= screen_width and 0 <= mouse_pos[1] <= square_size:
                running = False  # Exit the program
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            # If mouse button is up, reset mouse_pos
            mouse_pos = ()
        elif event.type == pygame.MOUSEMOTION:
            # Update mouse_pos while dragging the mouse
            if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
                mouse_pos = pygame.mouse.get_pos()


    # Fill screen with black
    screen.fill(BLACK)

    # Draw the small red square
    pygame.draw.rect(screen, RED, square_rect)

    if mouse_pos:
        relPos = surface_rect[0], surface_rect[1]
        actPos = mouse_pos[0] - relPos[0], mouse_pos[1] - relPos[1]
        pygame.draw.circle(box, BLACK, actPos, 3)

    # Blit the surface onto the screen
    screen.blit(box, surface_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
