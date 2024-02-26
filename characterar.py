import pygame
import pygame.camera
import pygame.mouse
import pygame.surfarray
import os
import random
import glob
import cv2
import questionary

pygame.init()
pygame.camera.init()
webcams = pygame.camera.list_cameras()
print(webcams)
webcam = pygame.camera.Camera(webcams[int(input("Enter camera number: "))])
print(f"Using camera {webcam}")
webcam.start()

started = False

characters = glob.glob(os.path.join("characters", "*"))
print(characters)
character = questionary.select("Choose a character", characters).ask()
idle = pygame.image.load(os.path.join(character, "idle.png"))
right = pygame.image.load(os.path.join(character, "right.png"))
left = pygame.transform.flip(right, True, False)

def switch_character():
    global character
    global idle
    global right
    global left
    character += 1
    if character == len(characters):
        character = 0
    idle = pygame.image.load(os.path.join(characters[character], "idle.png"))
    right = pygame.image.load(os.path.join(characters[character], "right.png"))
    left = pygame.transform.flip(right, True, False)
    idle = pygame.transform.scale(idle, (CAMERA_WIDTH / 10, CAMERA_WIDTH / 10))
    right = pygame.transform.scale(right, (CAMERA_WIDTH / 10, CAMERA_WIDTH / 10))
    left = pygame.transform.scale(left, (CAMERA_WIDTH / 10, CAMERA_WIDTH / 10))

first_frame = webcam.get_image()
CAMERA_WIDTH = first_frame.get_width()
CAMERA_HEIGHT = first_frame.get_height()

screen = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT))
screen.fill((0, 0, 0))
pygame.display.set_caption(f"CharacterAR ({character})")
# thorpy.init(screen, thorpy.theme_classic)
# switch_character_button = thorpy.Button("Switch Character")
# switch_character_button.at_unclick = switch_character
# switch_character_button.set_topleft(0, 0)


idle = pygame.transform.scale(idle, (CAMERA_WIDTH / 10, CAMERA_WIDTH / 10))
right = pygame.transform.scale(right, (CAMERA_WIDTH / 10, CAMERA_WIDTH / 10))
left = pygame.transform.scale(left, (CAMERA_WIDTH / 10, CAMERA_WIDTH / 10))


movementdirections = [1, -1, 0]
characterx = 0
charactery = 0
stepsindirection = CAMERA_WIDTH / 10
currentstep = 1
direction = 0
characterbase = (int(idle.get_width() / 2), idle.get_height())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.camera.quit()
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            started = True
        
    
    if currentstep == stepsindirection:
        currentstep = -1
    elif currentstep == 0:
        if characterx >= screen.get_width() - idle.get_width():
            direction = -1
        if characterx <= 0:
            direction = 1
        else:
            direction = random.choice(movementdirections)
    
    if not started:
        characterx = pygame.mouse.get_pos()[0]
        charactery = pygame.mouse.get_pos()[1]
    frame = webcam.get_image()
    screen.blit(frame, (0, 0))
    if started:
        characterx += direction
        edges = cv2.Canny(pygame.surfarray.array3d(frame), 150, 200)
        # screen.blit(pygame.surfarray.make_surface(edges), (0, 0))
        try:
            if edges[characterx + direction + characterbase[0] - 1][charactery + characterbase[1] - 1] != 0:
                charactery -= 1
            elif not edges[characterx + direction + characterbase[0] - 1][charactery + characterbase[1] + 1 - 1]:
                charactery += 1
        except IndexError:
            pass
    #switch_character_button.get_updater().update()
    if direction == 1:
        screen.blit(right, (characterx, charactery))
    if direction == -1:
        screen.blit(left, (characterx, charactery))
    if direction == 0:
        screen.blit(idle, (characterx, charactery))
    pygame.display.flip()
    pygame.display.update()
    currentstep += 1