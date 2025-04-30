'''
FYP Project 2022
Name: Garab
'''

import mediapipe as mp
import cv2
import numpy as np
from datetime import date
import pygame
from sys import exit
import random
import uuid
import string
import time
from FingerVariables import *
from DataRecord import Record, RecordReal, plot, boxplot

def get_label(index, hand, results):
    output = None
    for item in results.multi_handedness:
        if item.classification[0].index == index:
            label, score = item.classification[0].label, item.classification[0].score
            text = '{} {}'.format(label, round(score, 2))

            # Coordinates
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                [640, 480]).astype(int))

            output = text, coords

    return output

#renamed as draw angles
def draw_finger_angles(image, results, joint_list):
    # Loop through hands
    counter_for_index_finger = 0
    angle_list = [ ]

    for hand in results.multi_hand_landmarks:

        # Loop through joint sets
        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])  # First coord
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])  # Second coord
            c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y])  # Third coord

            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)

            if angle > 180.0:
                angle = 360 - angle
            if angle < 85.0:
                angle = 85

            cv2.putText(image, str(round(angle, 1)), tuple(np.multiply(b, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    return image

'''have to get back here'''

def maxlist(maxangle, Anglelist, First,Second,third,hand,set):

    a = np.array([hand.landmark[First].x, hand.landmark[First].y])  # First coord
    b = np.array([hand.landmark[Second].x, hand.landmark[Second].y])  # Second coord
    c = np.array([hand.landmark[third].x, hand.landmark[third].y])  # Third coord

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    angle = round(angle,1)
    if angle > 180.0:
        angle = 360 - angle

    if angle < 85.0:
        angle = 85
    set.append(angle)
    maxangle.append(angle)
    maxangle.sort(reverse=True)

    x = maxangle[0]

    if len(maxangle) > 10:
        Anglelist.append(x)
        maxangle.clear()
        Anglelist.sort(reverse=True)

    return Anglelist[0]

def minlist(minangle, anglelist,First,Second,Thrid,hand):
    name = None
    a = np.array([hand.landmark[First].x, hand.landmark[First].y])  # First coord
    b = np.array([hand.landmark[Second].x, hand.landmark[Second].y])  # Second coord
    c = np.array([hand.landmark[Thrid].x, hand.landmark[Thrid].y])  # Third coord

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    if angle < 85.0:
        angle = 85

    minangle.append(angle)
    minangle.sort()

    x = minangle[0]

    if len(minangle) > 10:
        anglelist.append(x)
        minangle.clear()
        anglelist.sort()

    return anglelist[0]

#pipe creation with coordinates
def create_pipe():

    random_pipe_position = random.choice(pipe_height)
    new_pipe_top, new_pipe_bottom = pipes.get_rect(center= (1300,random_pipe_position)), pipes.get_rect(midbottom= (1300,random_pipe_position - 500))
    return new_pipe_top, new_pipe_bottom

#pipe motion
def putting_pipes(pipes_list):

    for pipe in pipes_list:
        pipe.centerx -= 10

    visible_pipes = [x for x in pipes_list if x.right > -50]
    return visible_pipes

'''does this even need a function'''
def draw_pipes(pipes_list):
    for x in pipes_list:
        screen.blit(pipes,x)

#renamed draw_on_screen()
def Draw_floor():

    screen.blit(background,(background_x,0))
    screen.blit(background, (background_x + WIDTH, 0))
    screen.blit(floor, (floor_x, 630))
    screen.blit(floor, (floor_x + WIDTH, 630))

def checkcollision(pipes_list):
    for pipe in pipes_list:

        if bird_rect.colliderect(pipe):
            return False

        if bird_rect.top <=-20 or bird_rect.bottom >= 680:
            return False

    return True

#renamed bird_or_box_rotate
def fun_rotate(bird):

    new = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new

#renamed animation
def bird_animation():
    new = bird_frame[bird_index]
    new_rect = new.get_rect(center = (100,bird_rect.centery))
    return new, new_rect

def display_score(game_state):

    score_surface = game_font.render("Score: "+str(int(score)),True,(255,0,255)) #the text, then antialiasing, and colour
    score_rect = score_surface.get_rect(center = (800,20))
    screen.blit(score_surface,score_rect)

    if game_state == "game_over":
        high_score_surface = game_font.render("Hi Score: " + str(int(high_score)), True,(255, 255, 255))  # the text, then antialiasing, and colour
        high_score_rect = high_score_surface.get_rect(center=(1000,20))
        screen.blit(high_score_surface, high_score_rect)

start = time.time()

#id is named filename_id
id = str(uuid.uuid1())

id = [i for i in id if i in string.ascii_letters]

id = "".join(id)

#prepath is named file_date

cap = cv2.VideoCapture(0)

today = date.today()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


#processess = []
#os.mkdir('Output Images')

pygame.init()

#Screen
WIDTH = 1280
screen = pygame.display.set_mode((WIDTH,659))
clock = pygame.time.Clock()
retry = False

#background and floor Assets
background = pygame.image.load("game graphics/background 2.png").convert()
floor = pygame.image.load("game graphics/floor.png").convert()

#motion
background_x = 0
floor_x = 0

#bird animation loading
bird_1 = pygame.image.load("game graphics/bird-1.png").convert_alpha()
bird_2 = pygame.image.load("game graphics/bird-midflap.png").convert_alpha()
bird_3 = pygame.image.load("game graphics/bird-2.png").convert_alpha()
bird_4 = pygame.image.load("game graphics/bird-4.png").convert_alpha()

#bird animation
bird_frame = (bird_1,bird_2,bird_3,bird_4)
bird_index = 0

bird = bird_frame[bird_index]
bird_rect = bird.get_rect(center = (100,512))

#animation timer
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

#game logic
game_gravity = 0.5
bird_movement = 0
difficulty = 5000
game_active = True
score = 0
high_score = 0
game_font = pygame.font.SysFont('Moonhouse',40)
points = 0.1

#scoring
SCORE = pygame.USEREVENT + 2
pygame.time.set_timer(SCORE,100)

#game pipes
pipes = pygame.image.load("game graphics/pipes.png").convert_alpha()

pipe_list = []
pipe_height = (800,500, 200, 60, 50 , 190, 480, 700, 150)
pipe_speed = 10

#pipe spawn with timer
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,difficulty)

fingers=["Index", "Middle", "Ring", "Pinky", "Thumb"]

#music = pygame.mixer.Sound('game graphics/sound.mp3')


with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():

        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Detections
        # Rendering results

        if results.multi_hand_landmarks:

            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

                # left Hand
                if hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x > hand.landmark[
                    mp_hands.HandLandmark.PINKY_MCP].x:

                    if stage == "down" and hand.landmark[joint_list[0][0]].y > hand.landmark[joint_list[0][1]].y:
                        counter_name += 1
                        stage = "up"

                    if hand.landmark[joint_list[0][0]].y < hand.landmark[joint_list[0][1]].y:
                        stage = "down"

                    LFMax = maxlist(maxangle, Anglelist, joint_list[0][0], joint_list[0][1], joint_list[0][2], hand,L1)
                    LFMin = minlist(minangle, anglelist, joint_list[0][0], joint_list[0][1], joint_list[0][2], hand)

                    if stage2 == "down" and hand.landmark[joint_list[1][0]].y > hand.landmark[joint_list[1][1]].y:
                        counter_name2 += 1
                        stage2 = "up"
                        print(counter_name2)

                    if hand.landmark[joint_list[1][0]].y < hand.landmark[joint_list[1][1]].y:
                        stage2 = "down"

                    LSMax = maxlist(maxangle_2, Anglelist_2, joint_list[1][0], joint_list[1][1], joint_list[1][2], hand,L2)
                    LSMin = minlist(minangle_2, anglelist_2, joint_list[1][0], joint_list[1][1], joint_list[1][2], hand)

                    if stage3 == "down" and hand.landmark[joint_list[2][0]].y > hand.landmark[joint_list[2][1]].y:
                        counter_name3 += 1
                        stage3 = "up"
                        print(counter_name3)

                    if hand.landmark[joint_list[2][0]].y < hand.landmark[joint_list[2][1]].y:
                        stage3 = "down"

                    LTMax = maxlist(maxangle_3, Anglelist_3, joint_list[2][0], joint_list[2][1], joint_list[2][2], hand,L3)
                    LTMin = minlist(minangle_3, anglelist_3, joint_list[2][0], joint_list[2][1], joint_list[2][2], hand)

                    if stage4 == "down" and hand.landmark[joint_list[3][0]].y > hand.landmark[joint_list[3][1]].y:
                        counter_name4 += 1
                        stage4 = "up"
                        print(counter_name4)

                    if hand.landmark[joint_list[3][0]].y < hand.landmark[joint_list[3][1]].y:
                        stage4 = "down"

                    LFFMax = maxlist(maxangle_4, Anglelist_4, joint_list[3][0], joint_list[3][1], joint_list[3][2],
                                     hand,L4)
                    LFFMin = minlist(minangle_4, anglelist_4, joint_list[3][0], joint_list[3][1], joint_list[3][2], hand)

                    if stage5 == "down" and hand.landmark[joint_list[4][0]].x < hand.landmark[joint_list[4][1]].x:
                        counter_name5 += 1
                        stage5 = "up"

                        if stage == "up" and stage2 == "up" and stage3 == "up" and stage4 == "up":
                            bird_movement = 0
                            bird_movement -= 10

                        print(counter_name5)
                    if hand.landmark[joint_list[4][0]].x > hand.landmark[joint_list[4][1]].x:
                        stage5 = "down"

                    LTHMax = maxlist(maxangle_5, Anglelist_5, joint_list[4][0], joint_list[4][1], joint_list[4][2],
                                     hand,L5)
                    LTHMin = minlist(minangle_5, anglelist_5, joint_list[4][0], joint_list[4][1], joint_list[4][2], hand)

                    data = [[today, counter_name, counter_name2, counter_name3, counter_name4, counter_name5]]
                    angledata = [[today, LFMax, LFMin, LSMax, LSMin, LTMax, LTMin, LFFMax, LFFMin, LTHMax, LTHMin]]
                    RecordReal(data, 'LEFT_HAND.xlsx', headers)
                    RecordReal(angledata, 'LEFT_ANGLES.xlsx', headerAngle)

                # #RIGHT HAND
                if hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x < hand.landmark[
                    mp_hands.HandLandmark.PINKY_MCP].x:

                    if Rstage == "down" and hand.landmark[joint_list[0][0]].y > hand.landmark[joint_list[0][1]].y:
                        Rcounter_name += 1
                        Rstage = "up"
                        print(Rcounter_name)

                    if hand.landmark[joint_list[0][0]].y < hand.landmark[joint_list[0][1]].y:
                        Rstage = "down"

                    RFMax = maxlist(Rmaxangle, RAnglelist, joint_list[0][0], joint_list[0][1], joint_list[0][2], hand,R1)
                    RFMin = minlist(Rminangle, Ranglelist, joint_list[0][0], joint_list[0][1], joint_list[0][2], hand)

                    if Rstage2 == "down" and hand.landmark[joint_list[1][0]].y > hand.landmark[joint_list[1][1]].y:
                        Rcounter_name2 += 1
                        Rstage2 = "up"
                        print(Rcounter_name2)

                    if hand.landmark[joint_list[1][0]].y < hand.landmark[joint_list[1][1]].y:
                        Rstage2 = "down"

                    RSMax = maxlist(Rmaxangle_2, RAnglelist_2, joint_list[1][0], joint_list[1][1], joint_list[1][2],
                                    hand,R2)
                    RSMin = minlist(Rminangle_2, Ranglelist_2, joint_list[1][0], joint_list[1][1], joint_list[1][2], hand)

                    if Rstage3 == "down" and hand.landmark[joint_list[2][0]].y > hand.landmark[joint_list[2][1]].y:
                        Rcounter_name3 += 1
                        Rstage3 = "up"
                        print(Rcounter_name3)

                    if hand.landmark[joint_list[2][0]].y < hand.landmark[joint_list[2][1]].y:
                        Rstage3 = "down"

                    RTMax = maxlist(maxangle_3, Anglelist_3, joint_list[2][0], joint_list[2][1], joint_list[2][2], hand,R3)
                    RTMin = minlist(minangle_3, anglelist_3, joint_list[2][0], joint_list[2][1], joint_list[2][2], hand)

                    if Rstage4 == "down" and hand.landmark[joint_list[3][0]].y > hand.landmark[joint_list[3][1]].y:
                        Rcounter_name4 += 1
                        Rstage4 = "up"
                        print(Rcounter_name4)
                    if hand.landmark[joint_list[3][0]].y < hand.landmark[joint_list[3][1]].y:
                        Rstage4 = "down"

                    RFFMax = maxlist(Rmaxangle_4, RAnglelist_4, joint_list[3][0], joint_list[3][1], joint_list[3][2],
                                     hand,R4)
                    RFFMin = minlist(Rminangle_4, Ranglelist_4, joint_list[3][0], joint_list[3][1], joint_list[3][2], hand)

                    if Rstage5 == "down" and hand.landmark[joint_list[4][0]].x > hand.landmark[joint_list[4][1]].x:
                        Rcounter_name5 += 1
                        Rstage5 = "up"

                        if Rstage == "up" and Rstage2 == "up" and Rstage3 == "up" and Rstage4 == "up":
                            bird_movement = 0
                            bird_movement -= 10

                        if game_active == False:
                            retry = True

                        print(Rcounter_name5)
                    if hand.landmark[joint_list[4][0]].x < hand.landmark[joint_list[4][1]].x:
                        Rstage5 = "down"

                    RTHMax = maxlist(Rmaxangle_5, RAnglelist_5, joint_list[4][0], joint_list[4][1], joint_list[4][2],
                                     hand,R5)
                    RTHMin = minlist(Rminangle_5, Ranglelist_5, joint_list[4][0], joint_list[4][1], joint_list[4][2], hand)

                    rdata = [[today, Rcounter_name, Rcounter_name2, Rcounter_name3, Rcounter_name4, Rcounter_name5]]
                    Rangledata = [[today, RFMax, RFMin, RSMax, RSMin, RTMax, RTMin, RFFMax, RFFMin, RTHMax, RTHMin]]
                    RecordReal(rdata, 'RIGHT_HAND.xlsx', headers)
                    RecordReal(Rangledata, 'RIGHT_ANGLES.xlsx', headerAngle)

                # Render left or right detection
                if get_label(num, hand, results):

                    text, coord = get_label(num, hand, results)
                    cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            draw_finger_angles(image, results, joint_list)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                exit()
                break

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and game_active == True:
                    bird_movement = 0
                    bird_movement -= 10

            if retry == True and game_active == False:

                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                retry = False

                score = 0

            if event.type == SPAWNPIPE:

                pipe_list.extend(create_pipe())

            if event.type == BIRDFLAP:

                if bird_index < 3:
                    bird_index += 1
                else:
                    bird_index = 0
                bird, bird_rect = bird_animation()

            if event.type == SCORE:
                score += points

        if game_active:

            background_x -= 10
            Draw_floor()
            points = 0.1
            rotated_bird = fun_rotate(bird)

            bird_movement += game_gravity
            bird_rect.centery += bird_movement

            screen.blit(rotated_bird, bird_rect)

            game_active = checkcollision(pipe_list)

            pipe_list = putting_pipes(pipe_list)
            draw_pipes(pipe_list)

            display_score('x')

            # music.play()

        else:

            if high_score < score:

                high_score = score

            points = 0

            display_score("game_over")

        if floor_x <= -1280:
            floor_x = 0

        if background_x <= -1280:
            background_x = 0

        floor_x -= 10
        pygame.display.update()
        clock.tick(70)

        # Save our image
        #cv2.imwrite(os.path.join('Output Images', '{}.jpg'.format(uuid.uuid1())), image)
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
