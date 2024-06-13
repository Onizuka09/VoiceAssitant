import pygame
import numpy as np 
import pygame.camera 
import cv2 as cv
import time

# Face Haar cascade path
FACE_HAAR_PATH = "haarcascade_frontalface_default.xml"
FACE_HAAR = cv.CascadeClassifier(FACE_HAAR_PATH ) #cv.data.haarcascades + FACE_HAAR_PATH)
print (cv.data.haarcascades)# Screen settings
SCREEN = [300, 300]  # Adjust screen size for better visibility

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
def main():
    pygame.init()  # Initialize pygame
    pygame.camera.init()
    camera_list = pygame.camera.list_cameras()
    
    if not camera_list:
        raise ValueError("No cameras found.")

    # Set game screen
    screen = pygame.display.set_mode(SCREEN)
    
    # Initialize and start the camera
    cam = pygame.camera.Camera(camera_list[0], SCREEN)
    cam.start()
    
    while True:  # Main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cam.stop()
                pygame.quit()
                quit()

        image = cam.get_image()  # Get current webcam image

        cv_image = pygame_to_cvimage(image)  # Convert Pygame image to OpenCV image

        faces = detect_faces(cv_image)  # Detect faces

        cv_image = draw_from_points(cv_image, faces)  # Draw rectangles on faces

        pygame_image = pygame.image.frombuffer(cv_image.tobytes(), cv_image.shape[1::-1], 'BGR')  # Convert back to Pygame image

        screen.blit(pygame_image, (0, 0))  # Display the image on screen

        pygame.display.update()  # Update Pygame display

        #time.sleep(1 / 60)  # Limit to 30 frames per second

import threading 
if __name__ == '__main__':
    
    camera_thread = threading.Thread(target = main ) 
    camera_thread.start()
    while True:
        time.sleep(10) 
        print( "runninhg") 
    camera_thread.join()



