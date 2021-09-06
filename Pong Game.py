import pygame, random
from pygame import mixer

def ball_animation():
    global ball_velocity_x, ball_velocity_y, player_score, comp_score, score_time

    ball.x += ball_velocity_x
    ball.y += ball_velocity_y

    if ball.top <= 0 or ball.bottom >= display_screen_height:
        pygame.mixer.Sound.play(rebound_sound)
        ball_velocity_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        player_score += 1

    if ball.right >= display_screen_width:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        comp_score += 1

    if ball.colliderect(player) and ball_velocity_x > 0:
        pygame.mixer.Sound.play(rebound_sound)
        if abs(ball.right - player.left) < 21:
            ball_velocity_x *= -1
        elif abs(ball.top - player.bottom) < 21 and ball_velocity_y < 0:
            ball_velocity_y *= -1
        elif abs(ball.bottom - player.top) < 21 and ball_velocity_y > 0:
            ball_velocity_y *= -1

    if ball.colliderect(comp) and ball_velocity_x < 0:
        pygame.mixer.Sound.play(rebound_sound)
        if abs(ball.left - comp.right) < 21:
            ball_velocity_x *= -1
        elif abs(ball.top - comp.bottom) < 21 and ball_velocity_y < 0:
            ball_velocity_y *= -1
        elif abs(ball.bottom - comp.top) < 21 and ball_velocity_y > 0:
            ball_velocity_y *= -1

def player_animation():
    
    player.y += player_velocity
    
    if player.top <= 0:
        player.top = 0

    if player.bottom >= display_screen_height:
        player.bottom = display_screen_height


def comp_ai():
    if comp.top < ball.y:
        comp.y += comp_velocity
    if comp.bottom >= ball.y:
        comp.bottom -= comp_velocity

    if comp.top <= 0:
        comp.top = 0
    if comp.bottom >= display_screen_height:
        comp.bottom = display_screen_height


def ball_start():
    global ball_velocity_x, ball_velocity_y, ball_movement, score_time

    ball.center = (display_screen_width/2, display_screen_height/2)
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 1000:
        ready = basic_font.render("Ready", False, (255, 0, 0))
        display_screen.blit(ready, (display_screen_width/2 -55, display_screen_height/2 - 100))

    if 1000 < current_time - score_time < 2000:
        steady = basic_font.render("Steady", False, (255, 255, 0))
        display_screen.blit(steady, (display_screen_width/2 -60, display_screen_height/2 - 100))

    if 2000 < current_time - score_time < 3000:
        go = basic_font.render("GO!", False, (0, 200, 0))
        display_screen.blit(go, (display_screen_width/2 -35, display_screen_height/2 - 100))

    if current_time - score_time < 3000:
        ball_velocity_x, ball_velocity_y = 0,0

    else:
        ball_velocity_x = 7 * random.choice((1, -1))
        ball_velocity_y = 7 * random.choice((1, -1))
        score_time = None

pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

display_screen_width = 800
display_screen_height = 600
display_screen = pygame.display.set_mode((display_screen_width, display_screen_height))
bg_color = pygame.Color(0, 0, 0)
pygame.display.set_caption("Pong!")

ball = pygame.Rect(display_screen_width / 2 - 15, display_screen_height / 2 - 15, 30, 30)
player = pygame.Rect(display_screen_width - 20, display_screen_height / 2 - 70, 10, 100)
comp = pygame.Rect(10, display_screen_height / 2 - 70, 10, 100)

ball_velocity_x = random.choice((1, -1))
ball_velocity_y = random.choice((1, -1))
player_velocity = 0
comp_velocity = 7
ball_movement = False
score_time = True

player_score = 0
comp_score = 0
basic_font = pygame.font.Font("freesansbold.ttf", 40)

rebound_sound = pygame.mixer.Sound("rebound.wav")
score_sound = pygame.mixer.Sound("score.wav")
mixer.music.load("bg_music.wav")
mixer.music.play(-1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_velocity -= 6
            if event.key == pygame.K_DOWN:
                player_velocity += 6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_velocity += 6
            if event.key == pygame.K_DOWN:
                player_velocity -= 6


    ball_animation()
    player_animation()
    comp_ai()


    display_screen.fill(bg_color)
    pygame.draw.rect(display_screen, (0, 0, 255), player)
    pygame.draw.rect(display_screen, (255, 0, 0), comp)
    pygame.draw.ellipse(display_screen, (255, 255, 255), ball)
    pygame.draw.aaline(display_screen, (255, 255, 255), (display_screen_width / 2, 0), (display_screen_width / 2, display_screen_height))

    if score_time:
        ball_start()


    player_text = basic_font.render(f"{player_score}", False, (0, 0, 255))
    display_screen.blit(player_text, (435, 65))

    comp_text = basic_font.render(f"{comp_score}", False, (255, 0, 0))
    display_screen.blit(comp_text, (345, 65))

    scoreboard = basic_font.render("Score", False, (255, 255, 255))
    display_screen.blit(scoreboard, (345, 10))

    pygame.display.flip()
    clock.tick(60)
        
