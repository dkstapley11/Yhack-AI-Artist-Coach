import pygame, math
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

padding = 20
# Center surface on the screen
surface_rect = (padding * 2 + 512, screen_height // 2 - 512 // 2, 512, 512)
img_rect = (padding, screen_height // 2 - 512 // 2, 512, 512)
screen_rect = pygame.Rect((0, 0), (screen_width, screen_height))

# Set the dimensions and psosition of the exit button
square_size = 25
square_rect = pygame.Rect(screen_width - square_size - 3, 3, square_size, square_size)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main loop
running = True
mouse_pos = ()
prev_pos = ()

imgs = []

for i in range(14):
    path = "ui_images/"
    j = str(i)
    if len(j) == 1:
        j = "0" + j
    path += j + ".png"
    imgs.append(pygame.image.load(path))

smallImgs = []
sizek = 90

for img in imgs:
    smallImgs.append(pygame.transform.scale(img, (sizek, sizek)))

smallPadding = 10
megaPadding = 50

basey = screen_height // 2 - (sizek * 7 + smallPadding * 6) // 2

ys = [basey + (smallPadding + sizek) * y for y in range(7)]
xs = screen_width - megaPadding - smallPadding - sizek * 2
xs = [xs, xs + smallPadding + sizek]

slots = [[(x, y) for x in xs] for y in ys]
flattened = []
rects = []

for slot in slots:
    flattened += slot

for flat in flattened:
    rects.append((flat[0], flat[1], sizek, sizek))

imgindex = 0

def draw_smooth_line(surface, prev_pos, actual_pos):
    # Calculate the distance between previous and actual positions
    distance = math.sqrt((actual_pos[0] - prev_pos[0]) ** 2 + (actual_pos[1] - prev_pos[1]) ** 2)
    
    # If the distance is less than or equal to 6, just draw a circle at the actual position
    k = 3.5
    if distance <= 6 // k:
        pygame.draw.circle(surface, (0, 0, 0), actual_pos, 3)
    else:
        # Calculate the number of points needed to fill the line smoothly
        num_points = math.ceil(k * (distance / 6))
        
        # Draw circles at intermediate points
        for i in range(1, num_points):
            # Calculate intermediate positions
            x = prev_pos[0] + (actual_pos[0] - prev_pos[0]) * i / num_points
            y = prev_pos[1] + (actual_pos[1] - prev_pos[1]) * i / num_points
            pygame.draw.circle(surface, (0, 0, 0), (int(x), int(y)), 3)
    
    # Draw a circle at the actual position
    pygame.draw.circle(surface, (0, 0, 0), actual_pos, 3)

def modRect(rect, x):
    return rect[0] + x, rect[1] + x, rect[2] - x * 2, rect[3] - x * 2

def inRect(rect, coord):
    x, y = coord
    return rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]

ssr = modRect(square_rect, 3)
ssr = ssr[0], ssr[1], ssr[2] - 1, ssr[3] - 1
xLines = ((ssr[0], ssr[1]), (ssr[0] + ssr[2], ssr[1] + ssr[3])), ((ssr[0] + ssr[2], ssr[1]), (ssr[0], ssr[1] + ssr[3]))
font14px = pygame.font.Font("freesansbold.ttf", 14)
font24px = pygame.font.Font("freesansbold.ttf", 24)



class Button:
    def __init__(self, rect, inColor, outColor, text, w=4):
        self.rect = rect
        self.inColor = inColor
        self.outColor = outColor
        self.text = font24px.render(text, True, outColor)
        self.w = w
        self.action = None
    
    def update(self):
        pygame.draw.rect(screen, self.inColor, self.rect)
        offset = (self.rect[2] - self.text.get_width()) // 2, (self.rect[3] - self.text.get_height()) // 2
        screen.blit(self.text, (self.rect[0] + offset[0], self.rect[1] + offset[1]))
        pygame.draw.rect(screen, self.outColor, self.rect, self.w)
    
    def set_action(self, action):
        self.action = action
    
    def do(self):
        self.action()
    
    def get_pressed(self, pos):
        return inRect(self.rect, pos)

resetRect = (surface_rect[0], surface_rect[1] + surface_rect[3] + padding, 100, 40)
reset = Button(resetRect, (120, 120, 255), (50, 50, 255), "RESET")
w = 100
runRect = (surface_rect[0] + surface_rect[2] - w, surface_rect[1] + surface_rect[3] + padding, 100, 40)
run = Button(runRect, (255, 120, 120), (255, 45, 45), "RUN")

import subprocess

def runProgram():
    pygame.image.save(box,'output.png')
    subprocess.call(["python", "Grade_Image.py"])

def clearImg():
    box.fill(WHITE)

reset.set_action(clearImg)
run.set_action(runProgram)

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
            elif event.key == pygame.K_r:
                pygame.image.save(box,'output.png')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # If mouse button is down, set mouse_pos relative to the center of the surface
                mouse_pos = pygame.mouse.get_pos()
                # Check if the mouse click occurs within the boundaries of the red square
                if screen_width - square_size <= mouse_pos[0] <= screen_width and 0 <= mouse_pos[1] <= square_size:
                    running = False  # Exit the program
                    pygame.quit()
                    sys.exit()
                else:
                    i = 0
                    for rect in rects:
                        if inRect(rect, mouse_pos):
                            imgindex = int(i)
                        i += 1
                
                    if run.get_pressed(mouse_pos):
                        run.do()
                    elif reset.get_pressed(mouse_pos):
                        reset.do()

        elif event.type == pygame.MOUSEWHEEL:
            imgindex -= event.y
            if imgindex < 0:
                while imgindex < 0:
                    imgindex += 14
            elif imgindex > 13:
                while imgindex > 13: 
                    imgindex -= 14
        elif event.type == pygame.MOUSEBUTTONUP:
            # If mouse button is up, reset mouse_pos
            mouse_pos = ()
            prev_pos = ()
        elif event.type == pygame.MOUSEMOTION:
            # Update mouse_pos while dragging the mouse
            if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
                mouse_pos = pygame.mouse.get_pos()


    # Fill screen with black
    screen.fill(BLACK)

    # Draw the small red square
    pygame.draw.rect(screen, RED, square_rect)
    for line in xLines:
        pygame.draw.line(screen, BLACK, line[0], line[1], 4)
    

    if mouse_pos:
        relPos = surface_rect[0], surface_rect[1]
        actPos = mouse_pos[0] - relPos[0], mouse_pos[1] - relPos[1]
        # pygame.draw.circle(box, BLACK, actPos, 3)
        if not prev_pos:
            prev_pos = tuple(actPos)

        draw_smooth_line(box, prev_pos, actPos)

        prev_pos = tuple(actPos)

    # Blit the surface onto the screen
    screen.blit(box, surface_rect)
    screen.blit(imgs[imgindex], img_rect)

    i = 0
    for img in smallImgs:
        screen.blit(img, rects[i])
        if i == imgindex:
            pygame.draw.rect(screen, (0, 255, 0), modRect(rects[i], -6), 3)
        i += 1
    
    reset.update()
    run.update()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

