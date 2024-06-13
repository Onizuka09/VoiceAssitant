import pygame
import pygame.camera
import cv2 as cv
import numpy as np
import threading
from face_layout import Face

class FaceDetection:
    def __init__(self, inn_screen, inn_scr_size ):
        self.SCREEN = [800, 800]
        self.INNER_SCREEN_SIZE = inn_scr_size
        self.FACE_HAAR_PATH = "haarcascade_frontalface_default.xml"
        self.FACE_HAAR = cv.CascadeClassifier(self.FACE_HAAR_PATH)
        #self.screen_width, self.screen_height = self.SCREEN
        self.inner_screen = inn_screen # pygame.Surface(self.INNER_SCREEN_SIZE)
        self.lock = threading.Lock()
        self.is_talking = False
        self.running = True
        #self.init_pygame()
        #self.face = Face(self.screen, False)
        self.inner_screen_thread = threading.Thread(target=self.update_inner_screen, args=(self.inner_screen, self.lock), daemon=True)
        
    def surface_to_string(self, surface):
        return pygame.image.tostring(surface, 'RGB')
    
    def pygame_to_cvimage(self, surface):
        image_string = self.surface_to_string(surface)
        np_image = np.frombuffer(image_string, dtype=np.uint8)
        np_image = np_image.reshape((surface.get_height(), surface.get_width(), 3))
        cv_image = cv.cvtColor(np_image, cv.COLOR_RGB2BGR)
        return cv_image
    
    def detect_faces(self, cv_image):
        grayscale = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
        faces = self.FACE_HAAR.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces
    
    def draw_from_points(self, cv_image, points):
        for (x, y, w, h) in points:
            cv.rectangle(cv_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return cv_image
    
    def update_inner_screen(self, inner_screen, lock):
        pygame.camera.init()
        camera_list = pygame.camera.list_cameras()
        
        if not camera_list:
            raise ValueError("No cameras found.")
        
        cam = pygame.camera.Camera(camera_list[0], self.INNER_SCREEN_SIZE)
        cam.start()
        
        try:
            while True:
                image = cam.get_image()
                cv_image = self.pygame_to_cvimage(image)
                faces = self.detect_faces(cv_image)
                cv_image = self.draw_from_points(cv_image, faces)
                pygame_image = pygame.image.frombuffer(cv_image.tobytes(), cv_image.shape[1::-1], 'BGR')
                
                with lock:
                    inner_screen.blit(pygame_image, (0, 0))
                
                pygame.time.wait(30)
        finally:
            cam.stop()
    

if __name__ == "__main__":
    pygame.init()
    w,h = [800,800] 
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Screen in Screen Example")      
    inn_scr = pygame.Surface([200,200])
    d= FaceDetection(inn_scr, [200,200]) 
    face = Face(screen, False)
    is_talking = False  
    d.inner_screen_thread.start()
    run = True   
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        face.screen.fill((255, 255, 255))
            
        if is_talking:
               face.talk2()
        else:
               face.draw_face(act="neutral", expression="talk", eyes_open=True, look_direction="center", mouth_open=True)
            
        with d.lock:
                face.screen.blit(inn_scr, (600, 0))
            
        pygame.display.flip()
        
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
