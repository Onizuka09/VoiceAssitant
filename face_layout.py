import pygame
import time
import math


class Face:
    def __init__(self, screen =(400,400)):
        #pygame.init() 
        self.screen_lay = screen
        self.screen  = pygame.display.set_mode( self.screen_lay)
        self.clock = pygame.time.Clock()
        
        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Define eye parameters
        self.left_eye_center = (150, 200)
        self.right_eye_center = (250, 200)
        self.face_center = (200, 200)
        self.eye_radius = 50
        self.pupil_radius = 20
        self.face_radius = 150

        # Define mouth parameters
        self.mouth_rect = pygame.Rect(150, 270, 100, 50)
        self.mouth_width = 3
        self.mth= True

    
    def draw_smiling_mouth(self, open=False):
        if open:
            pygame.draw.arc(self.screen, self.BLACK, self.mouth_rect, math.radians(0), math.radians(180), self.mouth_width)
            pygame.draw.arc(self.screen, self.BLACK, self.mouth_rect, math.radians(180), math.radians(360),self.mouth_width)
        else:
            pygame.draw.arc(self.screen, self.BLACK, self.mouth_rect, math.radians(0), math.radians(180), self.mouth_width)

    def draw_mad_mouth(self, open=False):
        if open:
            pygame.draw.arc(self.screen, self.BLACK, self.mouth_rect, math.radians(180), math.radians(360), self.mouth_width)
            pygame.draw.arc(self.screen, self.BLACK, self.mouth_rect, math.radians(0), math.radians(180), self.mouth_width)
        else:
            pygame.draw.arc(self.screen, self.BLACK, self.mouth_rect, math.radians(180), math.radians(360), self.mouth_width)

    def draw_neutral_mouth(self, open=False):
        pygame.draw.line(self.screen, self.BLACK, self.mouth_rect.topleft, self.mouth_rect.topright, self.mouth_width)


     
    def draw_excited_mouth(self, open=False):
        pass
        """
        if open:
            pygame.draw.arc(self.screen, self.BLACK, self.mouth_rect, math.radians(0), math.radians(180), self.mouth_width)
            pygame.draw.arc(self.screen, self.BLACK, pygame.Rect(self.mouth_rect.left, self.mouth_rect.top, self.mouth_rect.width, mouth_rect.height * 2), math.radians(0), math.radians(180), mouth_width)
        else:
            pygame.draw.arc(screen, BLACK, mouth_rect, math.radians(0), math.radians(180), mouth_width)
        """
    
    def draw_eyebrows(self,expression="neutral"):
        if expression == "smiling":
            left_eyebrow_start = (110, 140)
            left_eyebrow_end = (190, 130)
            right_eyebrow_start = (210, 130)
            right_eyebrow_end = (290, 140)
        elif expression == "mad":
            left_eyebrow_start = (110, 130)
            left_eyebrow_end = (190, 140)
            right_eyebrow_start = (210, 140)
            right_eyebrow_end = (290, 130)
        elif expression == "excited":
            left_eyebrow_start = (110, 120)
            left_eyebrow_end = (190, 110)
            right_eyebrow_start = (210, 110)
            right_eyebrow_end = (290, 120)
        else:  # neutral
            left_eyebrow_start = (110, 140)
            left_eyebrow_end = (190, 140)
            right_eyebrow_start = (210, 140)
            right_eyebrow_end = (290, 140)
        
        pygame.draw.line(self.screen, self.BLACK, left_eyebrow_start, left_eyebrow_end, 5)
        pygame.draw.line(self.screen, self.BLACK, right_eyebrow_start, right_eyebrow_end, 5)

    def draw_eyes(self,open=True, look_direction="center"):
        if look_direction == "left":
            self.pupil_offset = (-25, 0)
        elif look_direction == "right":
            self.pupil_offset = (25, 0)
        else:  # center
            self.pupil_offset = (0, 0)
    
        if open:
        # Draw left eye open
            pygame.draw.circle(self.screen, self.BLACK, self.left_eye_center, self.eye_radius)
            pygame.draw.circle(self.screen, self.WHITE, self.left_eye_center, self.eye_radius - 5)
            pygame.draw.circle(self.screen, self.BLACK, (self.left_eye_center[0] + self.pupil_offset[0], self.left_eye_center[1] + self.pupil_offset[1]), self.pupil_radius)
        # Draw right eye open
            pygame.draw.circle(self.screen, self.BLACK, self.right_eye_center, self.eye_radius)
            pygame.draw.circle(self.screen, self.WHITE, self.right_eye_center, self.eye_radius - 5)
            pygame.draw.circle(self.screen, self.BLACK, (self.right_eye_center[0] + self.pupil_offset[0], self.right_eye_center[1] + self.pupil_offset[1]), self.pupil_radius)
        else:
        # Draw left eye closed
            pygame.draw.line(self.screen, self.BLACK, (self.left_eye_center[0] - self.eye_radius, self.left_eye_center[1]), (self.left_eye_center[0] + self.eye_radius, self.left_eye_center[1]),5 )
        # Draw right eye closed
            pygame.draw.line(self.screen, self.BLACK, (self.right_eye_center[0] - self.eye_radius, self.right_eye_center[1]), (self.right_eye_center[0] + self.eye_radius, self.right_eye_center[1]), 5)




    def draw_hat(self):
        hat_width = 140
        hat_height = 50
        hat_color = (255, 0, 0)  # Red color
        brim_height = 15
        hat_top_left = (self.face_center[0] - hat_width // 2, self.face_center[1] - self.face_radius - hat_height)
    
    # Draw the main part of the hat
        pygame.draw.rect(self.screen, hat_color, (hat_top_left[0], hat_top_left[1], hat_width, hat_height+12))
    
    # Draw the brim of the hat as an arc
        brim_top_left = (hat_top_left[0], hat_top_left[1] + hat_height)
        brim_rect = pygame.Rect(brim_top_left[0], brim_top_left[1], hat_width, brim_height * 2)  # Adjust height for better arc
    
    
        start_angle = 0  # 0 degrees (start from right)
        end_angle = math.pi  # 180 degrees (end at left)
    
        pygame.draw.arc(self.screen, hat_color, brim_rect, start_angle, end_angle, brim_height)
    def talk(self): 
        self.draw_smiling_mouth(True)
        time.sleep(0.3)
        self.draw_smiling_mouth(False) 
        time.sleep(0.3) 
        
    def draw_face(self,act ="talk",expression= "neutral", eyes_open=True, look_direction="center", mouth_open=False):
        self.screen.fill(self.WHITE)
    # draw the face layout 
        pygame.draw.circle(self.screen, self.BLACK, self.face_center, self.face_radius)
        pygame.draw.circle(self.screen, self.WHITE, self.face_center, self.face_radius - 5)
    # draw hat 
        self.draw_hat()

        self.draw_eyes(eyes_open, look_direction)
    
        self.draw_eyebrows(expression)
        if act == "talk":
        #talk()
            self.draw_smiling_mouth(mouth_open)
            #self.talk2()
        elif act == "neutral":
            self.draw_neutral_mouth(mouth_open)
        elif act  == "excited":
            self.draw_excited_mouth(mouth_open)
        else:  # neutral
            self.draw_neutral_mouth(mouth_open)
        pygame.display.flip()
    def talk2(self):
        self.draw_face(act="talk",expression="talk", eyes_open=True, look_direction="center",mouth_open=self.mth)
        self.mth = not self.mth
        time.sleep(0.3)
    def test(self) : 
        run = True
        while run : 
            for event in pygame.event.get():
                if event.type  == pygame.QUIT:
                    run= False
            self.draw_face(act="neutral",expression="talk", eyes_open=True, look_direction="center",mouth_open=True)
        pygame.quit()
    def test2(self):
        run = True
        is_talking = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    print('t')
                    if event.key == pygame.K_t:
                        is_talking = not is_talking  # Toggle talking on/off with 't' key

            if is_talking:
                self.talk2() 
               #self.clock.tick(0.3)
            else :
                self.draw_face(act="neutral",expression="talk", eyes_open=True, look_direction="center",mouth_open=True)




if __name__ == '__main__':
    f= Face((400,400))
    f.test2()
    
