
import pygame
import pygame.camera
import cv2 as cv
import numpy as np
import threading
import time
from face_layout import Face 
# Constants
SCREEN = [800, 800]  # Main screen size
INNER_SCREEN_SIZE = [300, 300]  # Inner screen size

# Haar Cascade for face detection
FACE_HAAR_PATH = "haarcascade_frontalface_default.xml"
FACE_HAAR = cv.CascadeClassifier( FACE_HAAR_PATH)

def surface_to_string(surface):
    """Convert a pygame surface into string"""
    return pygame.image.tostring(surface, 'RGB')

def pygame_to_cvimage(surface):
    """Convert a pygame surface into a cv image"""
    image_string = surface_to_string(surface)
    np_image = np.frombuffer(image_string, dtype=np.uint8)
    np_image = np_image.reshape((surface.get_height(), surface.get_width(), 3))
    cv_image = cv.cvtColor(np_image, cv.COLOR_RGB2BGR)
    return cv_image

def detect_faces(cv_image):
    """Detects faces based on Haar cascades. Returns points."""
    grayscale = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
    faces = FACE_HAAR.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def draw_from_points(cv_image, points):
    """Draws rectangles around detected faces"""
    for (x, y, w, h) in points:
        cv.rectangle(cv_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return cv_image

def update_inner_screen(inner_screen, lock):
    pygame.camera.init()
    camera_list = pygame.camera.list_cameras()
    
    if not camera_list:
        raise ValueError("No cameras found.")

    cam = pygame.camera.Camera(camera_list[0], INNER_SCREEN_SIZE)
    cam.start()
    
    try:
        while True:
            image = cam.get_image()  # Get current webcam image

            cv_image = pygame_to_cvimage(image)  # Convert Pygame image to OpenCV image

            faces = detect_faces(cv_image)  # Detect faces

            cv_image = draw_from_points(cv_image, faces)  # Draw rectangles on faces

            pygame_image = pygame.image.frombuffer(cv_image.tobytes(), cv_image.shape[1::-1], 'BGR')  # Convert back to Pygame image

            with lock:
                inner_screen.blit(pygame_image, (0, 0))

            pygame.time.wait(30)  # Simulate some delay for FPS control
    finally:
        cam.stop()

# Initialize Pygame
screen_width, screen_height = SCREEN
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

face = Face(screen, False) 
# Set up the main screen

pygame.display.set_caption("Screen in Screen Example")

# Set up the inner screen
inner_screen = pygame.Surface(INNER_SCREEN_SIZE)

# Lock for thread synchronization
lock = threading.Lock()

# Create and start the worker thread
inner_screen_thread = threading.Thread(target=update_inner_screen, args=(inner_screen, lock), daemon=True)
inner_screen_thread.start()
is_talking = False 
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #print('t')
            if event.key == pygame.K_t:
               is_talking = not is_talking

    # Fill the main screen with a color
    face.screen.fill((255, 255, 255))  # Bl. background
    
    if is_talking:
         face.talk2() 
               #self.clock.tick(0.3)
    else :
       face.draw_face(act="neutral",expression="talk", eyes_open=True, look_direction="center",mouth_open=True)

    with lock:
        face.screen.blit(inner_screen, (500, 0))

    
    
    # Blit the inner screen onto the main screen at position (200, 150)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()


"""
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the main screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Screen in Screen Example")

# Set up the inner screen
inner_width, inner_height = 300, 300
inner_screen = pygame.Surface((inner_width, inner_height))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the main screen with a color
    screen.fill((0, 0, 0))  # Black background

    # Fill the inner screen with a different color
    inner_screen.fill((0, 128, 255))  # Blue background

    # Draw something on the inner screen
    pygame.draw.circle(inner_screen, (255, 0, 0), (inner_width // 2, inner_height // 2), 50)  # Red circle

    # Blit the inner screen onto the main screen at position (200, 150)
    screen.blit(inner_screen, (500, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
"""
