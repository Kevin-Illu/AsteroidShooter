import pygame, sys, random

def laser_update(laser_list, speed = 300):
    for rect in laser_list:
        rect.y -= round(speed * dt)

        if rect.bottom < 0:
            laser_list.remove(rect)

def meteor_update(meteor_list, speed = 300):
    for meteor_tuple in meteor_list:

        direction = meteor_tuple[1]
        meteor_rect = meteor_tuple[0]
        meteor_rect.center += direction * speed * dt

        if meteor_rect.top > WINDOW_HEIGHT + 100:
            meteor_list.remove(meteor_tuple)

def display_score ():
    score_text = f'Score: {pygame.time.get_ticks() // 1000}'
    text_surf = font.render(score_text, True, "white")
    text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 80))

    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, 'white', text_rect.inflate(50, 20), width=4, border_radius=10)


def laser_timer(can_shoot, duration = 500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot

# game init
# pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.mixer.init() 
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Meteor Shooter')
clock = pygame.time.Clock()

# create a surface
test_surf = pygame.Surface((20, 20))
test_surf.fill((250,250,250))

# importing images
background = pygame.image.load('./graphics/background.png').convert()
ship_surf = pygame.image.load('./graphics/ship.png').convert_alpha()
meteor_surf = pygame.image.load('./graphics/meteor.png').convert_alpha()
laser_surf = pygame.image.load('./graphics/laser.png').convert()

# import sonds
laser_sound = pygame.mixer.Sound('.\sounds\explosion.wav')
background_music = pygame.mixer.Sound('.\sounds\music.wav')
background_music.play(loops = -1)

# import Rectangle
ship_rect = ship_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
laser_list = []

# laser timer
can_shoot = True
shoot_time = None

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)
meteor_list = []

# import text
font = pygame.font.Font('./graphics/subatomic.ttf', 50)
while True:

    # input and events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if event.type == pygame.MOUSEMOTION:
        #     ship_rect.center = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and can_shoot:
                laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
                laser_list.append(laser_rect)

                # timer
                can_shoot = False
                shoot_time = pygame.time.get_ticks()

                # play the sounds
                laser_sound.play()

        if event.type == meteor_timer:

            x_pos = random.randint(0,WINDOW_WIDTH)
            y_pos = random.randint(-100, -50)

            meteor_rect = meteor_surf.get_rect(midbottom = (x_pos, y_pos))
            # create a random direction
            direction = pygame.math.Vector2(random.uniform(-0.5, 0.5),1)

            meteor_list.append((meteor_rect, direction))


    ship_rect.center = pygame.mouse.get_pos() 
    # laser_rect.center = ship_rect.center
    # framerate limit
    dt = clock.tick(120) / 1000

    # update
    laser_update(laser_list)
    can_shoot = laser_timer(can_shoot, 150)

    meteor_update(meteor_list, speed = 500)

    display_surface.fill((0,0,0))
    display_surface.blit(background, (0,0))

    display_score()
    # meteor ship collisions
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect):
            pygame.quit()
            sys.exit()

    for laser_rect in laser_list:
        for meteor_tuple in meteor_list:
            meteor_rect = meteor_tuple[0]
            if laser_rect.colliderect(meteor_rect):
                meteor_list.remove(meteor_tuple)
                laser_list.remove(laser_rect)

    # if len(laser_list) != 0:
    for rect in laser_list:
        display_surface.blit(laser_surf, rect)
    
    for meteor_tuple in meteor_list:
        display_surface.blit(meteor_surf, meteor_tuple[0])

    display_surface.blit(ship_surf, ship_rect)

    # update the fram to the player / update the display surface
    pygame.display.update()
