#  IMPORT FUNCTION
import pygame
import sys
import random
from pygame.constants import K_SPACE, K_r, K_s
from time import sleep

# START PYGAME
pygame.init()


# VARIABLE
score = 0
main_arz = 288
main_tol = 505
floor_animation = 0
jazebe = 0.20
movement = 0
pipe_list = []
game_status = True
bird_list_index = 0
active_score = True
font = pygame.font.Font(r'G:\Pygame Flappy Bird\assets\font\Font.TTF', 25)
high_score = 0
clock_speed = 90

# LOAD IMAGE FOR BACKGROUND
main_background = pygame.image.load(
    r'G:\Pygame Flappy Bird\assets\img\bg1.png')

# LOAD FLOOR IMAGE FOR BLIT ON THE BACKGROUND AND PIPES
main_floor = pygame.image.load(r'G:\Pygame Flappy Bird\assets\img\floor.png')

# LOAD BIRD MID IMAGE FOR BLIT AND FLAP
bird_mid = pygame.image.load(
    r'G:\Pygame Flappy Bird\assets\img\red_bird_mid_flap.png')
# LOAD BIRD DOWN IMAGE  FOR BLIT WHEN GO DOWN
bird_down = pygame.image.load(
    r'G:\Pygame Flappy Bird\assets\img\red_bird_down_flap.png')
# LOAD BIRD UP IMAGE FOR BLIT FOR BLIT WHEN JUMP WITH SPACE
bird_up = pygame.image.load(
    r'G:\Pygame Flappy Bird\assets\img\red_bird_up_flap.png')
# LOAD PIPE IMAGE FOR BLIT ON BACKGROUND AND UNDER FLOOR
pipe_image = pygame.image.load(
    r'G:\Pygame Flappy Bird\assets\img\pipe_green.png')

game_over_image = pygame.image.load(r'G:\Pygame Flappy Bird\assets\img\message.png')
game_over_image_rect = game_over_image.get_rect(center=(main_arz/2, 250))

sound_win = pygame.mixer.Sound(
    r'G:\Pygame Flappy Bird\assets\sound\smb_stomp.wav')

sound_game_over = pygame.mixer.Sound(
    r'G:\Pygame Flappy Bird\assets\sound\smb_mariodie.wav')

sound_pipe_bang = pygame.mixer.Sound(r'G:\Pygame Flappy Bird\assets\sound\sfx_hit.wav')
sound_win = pygame.mixer.Sound(r'G:\Pygame Flappy Bird\assets\sound\sfx_wing.wav')
# DEFINE
# GENEATOR PIPE RECT(POR KARDAN LIST)


def generator_pipe_rect():
    # SET PIPE SIZE RANDOM
    randop_pipe = random.randrange(150, 400)
    # BOTTOM PIPE
    pipe_rect_down = pipe_image.get_rect(midbottom=(300, randop_pipe - 117))
    # TOP PIPE
    pipe_rect_up = pipe_image.get_rect(midtop=(300, randop_pipe))
    return pipe_rect_up, pipe_rect_down


# PIPE MOVEMEN
def pipe(pipes):
    for pipe in pipes:
        # PIPE SPEED
        pipe.centerx -= 3
    # SAVE PIPE IN DISPLAY AND DEL OUT DISPLAY PIPE
    inside_pipe = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipe


# PIPE BLIT
def display_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom > 300:
            main_screen.blit(pipe_image, pipe)
        else:
            # PIPE BOTTOM COMMAND (x = FALSE , Y = TRUE)
            pipe_image_bottom = pygame.transform.flip(pipe_image, False, True)
            main_screen.blit(pipe_image_bottom, pipe)


# BARKHORD BA RECT HA
def pipe_bang(pipes):
    for pipe in pipes:
        # PIPES
        if bird_image_rect.colliderect(pipe):
            sound_pipe_bang.play()
            sound_game_over.play()
            sleep(3)
            return False
            break
        # FLOOR AND SKY
        if bird_image_rect.top <= -30 or bird_image_rect.bottom >= 400:
            sound_pipe_bang.play()
            sound_pipe_bang.play()
            sleep(3)
            return False
            break
            
    return True


def bird_animation():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center=(35, bird_image_rect.centery))
    return new_bird, new_bird_rect


def score_fun(status):
    if status == 'active':
        font = pygame.font.Font(
            r'G:\Pygame Flappy Bird\assets\font\Font.TTF', 35)
        txt1 = font.render(str(score), False, (0, 0, 0))
        txt1_rect = txt1.get_rect(center=(main_arz/2, 50))
        main_screen.blit(txt1, txt1_rect)
    if status == 'game_over':
        # SCORE
        font = pygame.font.Font(
            r'G:\Pygame Flappy Bird\assets\font\Font.TTF', 25)
        txt1 = font.render('score', False, (0, 0, 0))
        txt1_rect = txt1.get_rect(center=(main_arz/2, 425))
        main_screen.blit(txt1, txt1_rect)

        font = pygame.font.Font(
            r'G:\Pygame Flappy Bird\assets\font\Font.TTF', 40)
        txt1 = font.render(f'{score}', False, (0, 0, 0))
        txt1_rect = txt1.get_rect(center=(main_arz/2, 475))
        main_screen.blit(txt1, txt1_rect)

        # HIGH SCORE
        font = pygame.font.Font(
            r'G:\Pygame Flappy Bird\assets\font\Font.TTF', 40)
        txt2 = font.render('RECORD', False, (255, 215, 0))
        txt2_rect = txt2.get_rect(center=(main_arz/2, 25))
        main_screen.blit(txt2, txt2_rect)

        font = pygame.font.Font(
            r'G:\Pygame Flappy Bird\assets\font\Font.TTF', 55)
        txt2 = font.render(f'{high_score}', False, (255, 215, 0))
        txt2_rect = txt2.get_rect(center=(main_arz/2, 75))
        main_screen.blit(txt2, txt2_rect)


def score_update():
    global score, high_score, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 20 < pipe.centerx < 25 and active_score == True:
                score += 1
                sound_win.play()
                active_score = False
            if pipe.centerx == 0:
                active_score = True
    if score > high_score:
        high_score = score


# SPEED SHOW PIPE ON DISPLAY
pipe_creator = pygame.USEREVENT
bird_creator = pygame.USEREVENT + 1
pygame.time.set_timer(bird_creator, 90)
pygame.time.set_timer(pipe_creator, 1200)

bird_list = [bird_mid, bird_down, bird_up]
bird_image = bird_list[bird_list_index]

# SET BIRD RECT
bird_image_rect = bird_mid.get_rect(center=(35, 200))

# UPDATE SPEED
clock = pygame.time.Clock()
main_screen = pygame.display.set_mode((main_arz, main_tol))

while True:
    # GET MOUSE AND KEYBOARD EVENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # EXIT
            pygame.quit()
            sys.exit()

        # BIRD JUMP
        if event.type == pygame.KEYDOWN:  # (FESHAR DADN KEY)
            if event.key == K_SPACE:  # (SPACE KEY)
                movement = 0
                movement -= 4.5  # (JUMP PIXEL)

            if event.key == pygame.K_s and game_status == False:
                game_status = True
                pipe_list.clear()
                bird_image_rect.center = (35, 200)
                movement = 0
                score = 0
        if score == 20:
            clock_speed = 95

        if score == 40:
            clock_speed = 110
        if score > 70:
            clock_speed = 160
        # FOR APPEND Y,X IN PIPE_LIST
        if event.type == pipe_creator:
            # EXTAND FOR 2,3,4,.. / APPEND FOR ONE VARIABLE
            pipe_list.extend(generator_pipe_rect())

        # FOR APPEND Y,X IN BIRD_LIST
        if event.type == bird_creator:
            if bird_list_index < 2:
                bird_list_index += 1
            else:
                bird_list_index = 0

            bird_image, bird_image_rect = bird_animation()

    # BACKGROUND IMAGE
    main_screen.blit(main_background, (0, 0))
    

    if game_status:
        display_pipes(pipe_list)
        if floor_animation <= -300:
            floor_animation = 0
        # BIRD IMAGE
        main_screen.blit(bird_image, bird_image_rect)
        # BIRD ANIMATION
        movement += jazebe
        bird_image_rect.centery += movement
        # BLIT PIPES
        game_status = pipe_bang(pipe_list)
        pipe_list = pipe(pipe_list)
        # FLOOR IMAGE
        main_screen.blit(main_floor, (floor_animation, 400))
        # FLOOR ANIMATION
        main_screen.blit(main_floor, (floor_animation + 290, 400))
        floor_animation -= 1
        score_update()
        score_fun('active')

    else:
        score_fun('game_over')
        main_screen.blit(game_over_image, game_over_image_rect)

    # DISPLAY UPDATE
    pygame.display.update()
    # GAME SPEED
    clock.tick(clock_speed)
