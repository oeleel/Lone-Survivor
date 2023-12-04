import uvage
import math
import random

camera = uvage.Camera(800, 600)

background = uvage.from_image(400,300, 'cs1110_game_background.png')
background.scale_by(4)

score = 0

player_images = uvage.load_sprite_sheet('sprite_sheet_cs1110.png', 4, 4)
player = uvage.from_image(200,200, player_images[0])
point = uvage.from_circle(400, 300, 'red', 0.01) #for direction of player movement

score_display = uvage.from_text(80,30, 'Score: ' + str(score), 50, 'red') #score display variables
ult_ready = uvage.from_text(87,60, 'R: Ready', 50, 'red')
ult_not_ready = uvage.from_text(120,60, 'R: Not Ready', 50, 'red')

q_ability = uvage.from_image(-1000, -1000, 'qAbility.png') #q-ability variables
q_ability.scale_by(0.05)
ability_off_loc = uvage.from_circle(-1000, -1000, 'red', 1)
q_ability_out = False
q_key_was_pressed = False

ult_orb = uvage.from_image(-100, -100, 'ultimate_ability.png') #ultimate orb variables
ult_orb.scale_by(0.2)
ult_range = uvage.from_circle(-400, -500, 'blue', 200)
has_ult = False
frames = 0

current_x = 0
current_y = 0
position_captured = False

y_down_increment = 0 #goes to 3
x_left_increment = 4 #goes to 7
x_right_increment = 8 #goes to 11
y_up_increment = 12 #goes to 15

last_x_direction = 'right'
last_y_direction = 'down'

screen = 0
frames_enemy_spawn = 0
enemies = []



def player_move():
    global y_up_increment, y_down_increment, x_right_increment, x_left_increment, last_x_direction, last_y_direction

    is_moving = False

    if camera.mouseclick:
        point.center = camera.mouse

    y_abs = abs(point.y - player.y)
    x_abs = abs(point.x - player.x)
    y_dist = point.y - player.y
    x_dist = point.x - player.x

    hypo = math.sqrt(y_dist**2 + x_dist**2)
    speed = 5

    if hypo != 0:
        tx = (x_dist / hypo) * speed
        ty = (y_dist / hypo) * speed
    else:
        tx = 0
        ty = 0

    player.x += tx
    player.y += ty

    if not q_ability_out:
        q_ability.x += tx
        q_ability.y += ty

    is_moving = hypo > 1  # Check if the player is far enough
    idle_bound = 4

    if y_abs < idle_bound  and x_abs < idle_bound:
        is_moving = False
        player.x = point.x
        player.y = point.y
    else:
        is_moving = True

    if is_moving: #updates sprite animation NEED TO FIX THE IDLE STATES 11/26/23
        if abs(y_dist) > abs(x_dist):  # Vertical movement
            if y_dist > 0:  # Down
                y_down_increment = (y_down_increment + 0.3) % 4
                player.image = player_images[int(y_down_increment)]
                last_y_direction = 'down'
            else:  # Up
                y_up_increment = (y_up_increment + 0.3) % 4 + 12
                player.image = player_images[int(y_up_increment)]
                last_y_direction = 'up'
        else:  # Horizontal movement
            if x_dist > 0:  # Right
                x_right_increment = (x_right_increment + 0.3) % 4 + 8
                player.image = player_images[int(x_right_increment)]
                last_x_direction = 'right'
            else:  # Left
                x_left_increment = (x_left_increment + 0.3) % 4 + 4
                player.image = player_images[int(x_left_increment)]
                last_x_direction = 'left'

    else: # not moving
        if last_y_direction == 'down':
            player.image = player_images[0]  # Idle image if not moving
        elif last_y_direction == 'up':
            player.image = player_images[12]
        elif last_x_direction == 'right':
            player.image = player_images[8]
        elif last_x_direction == 'left':
            player.image = player_images[4]

def spawn_enemy():
    global score, frames_enemy_spawn
    base_spawn_rate = 60
    score_factor = score // 10
    spawn_rate = base_spawn_rate - (score_factor * 5)

    if frames_enemy_spawn % spawn_rate == 0:
        enemy = uvage.from_image(-40, -40, 'enemy.png')
        enemy.scale_by(0.1)
        xcoord = random.randint(-40, 840)
        ycoord = random.randint(-40, 640)
        side = random.randint(1, 4)
        if side == 1: #spawn from north
            enemy.x = xcoord
            enemy.y = -40
        if side == 2: #spawn from east
            enemy.x = 840
            enemy.y = ycoord
        if side == 3: #spawn from south
            enemy.x = xcoord
            enemy.y = 640
        if side == 4: #spawn from west
            enemy.x = -40
            enemy.y = ycoord
        enemies.append(enemy)
    frames_enemy_spawn += 1


def chase(): #makes enemy follow player
    for enem in enemies:
        ydist = abs(enem.y - player.y)
        xdist = abs(enem.x - player.x)
        hypo = math.sqrt((ydist ** 2) + (xdist ** 2))
        t = hypo / 4
        if t == 0:
            tx = xdist
            ty = ydist
        else:
            tx = xdist / t
            ty = ydist / t

        if player.x > enem.x:
            enem.x += tx
        if player.x < enem.x:
            enem.x += -tx

        if player.y > enem.y:
            enem.y += ty
        if player.y < enem.y:
            enem.y += -ty

def spawn_ult():
    global frames, has_ult
    if has_ult == False:
        if frames == 240:
            ult_orb.x = random.randint(100, 700)
            ult_orb.y = random.randint(100, 500)
            frames = 0
        else:
            frames += 1

def grab_ult():
    global has_ult
    if player.touches(ult_orb):
        has_ult = True
        ult_orb.x = -100
        ult_orb.y = -100


def use_ult():
    global has_ult,score, score_display
    if uvage.is_pressing("r") and has_ult == True:
        has_ult = False
        touch = [] #must create list bc pop makes list shorter
        ult_range.x = player.x
        ult_range.y = player.y
        for q in range(len(enemies)):
            if ult_range.touches(enemies[q]):
                touch.append(q)
        for w in touch[::-1]:
            enemies.pop(w)
        score += len(touch)
        score_display = uvage.from_text(80,30, 'Score: ' + str(score), 50, 'red')
        ult_range.x = -400
        ult_range.y = -500

def fireball():
    global q_ability_out, q_ability_dx, q_ability_dy, current_x, current_y, position_captured, q_og_x, q_og_y

    if uvage.is_pressing('q') and not q_ability_out:
        if not position_captured:
            q_ability.x = player.x
            q_ability.y = player.y

            stored_mouse_x = camera.mousex
            stored_mouse_y = camera.mousey
            position_captured = True

            q_ability_dx = stored_mouse_x - player.x
            q_ability_dy = stored_mouse_y - player.y


            distance = math.sqrt(q_ability_dx ** 2 + q_ability_dy ** 2)
            if distance != 0:
                q_ability_dx /= distance
                q_ability_dy /= distance

            q_ability_out = True

    if q_ability_out:
        q_ability.x += q_ability_dx * 12
        q_ability.y += q_ability_dy * 12

        if q_ability.x > camera.width or q_ability.x < 0 or q_ability.y > camera.height or q_ability.y < 0:
            q_ability.x = ability_off_loc.x
            q_ability.y = ability_off_loc.y
            q_ability_out = False
            position_captured = False

def enemy_kill():
    global score, score_display
    touch = []
    for q in range(len(enemies)):
        if q_ability.touches(enemies[q], 5, 5):
            touch.append(q)
            q_ability.x = ability_off_loc.x
            q_ability.y = ability_off_loc.y
            score += 1
            score_display = uvage.from_text(80,30, 'Score: ' + str(score), 50, 'red')

    for w in touch[::-1]:
        enemies.pop(w)

def player_die():
    global screen, score
    for enemy in enemies:
        if player.touches(enemy, -50, -50):
            screen = 2


def tick():
    global score_display, score, has_ult, screen, enemies, player, q_ability, ult_orb, frames, frames_enemy_spawn

    if screen == 0:
        camera.clear('black')
        camera.draw(uvage.from_text(400, 100, 'Lone Survivor', 100, 'white', True))
        camera.draw(uvage.from_text(400, 200, 'Click mouse to move', 30, 'white'))
        camera.draw(uvage.from_text(400, 230, 'Press Q to shoot', 30, 'white'))
        camera.draw(uvage.from_text(400, 260, 'Press R to use Ultimate; will exterminate all close enemies', 30, 'white'))
        camera.draw(uvage.from_color(400, 400, 'white', 120, 70))
        camera.draw(uvage.from_text(400, 400, 'Play', 70, 'black', True))
        if camera.mouseclick:
            point.center = camera.mouse
        if point.x >= 340 and point.x <= 460 and point.y >= 365 and point.y <= 435:
            screen = 1

        camera.display()

    if screen == 1:
        camera.clear('black')

        camera.draw(background)
        camera.draw(player)
        camera.draw(point)

        camera.draw(ult_orb)
        camera.draw(ult_range)
        spawn_ult()
        grab_ult()
        use_ult()

        enemy_kill()
        camera.draw(q_ability)
        player_move()
        spawn_enemy()

        fireball()
        chase()

        if has_ult:
            camera.draw(ult_ready)
        else:
            camera.draw(ult_not_ready)

        for i in enemies:
            camera.draw(i)

        score_display = uvage.from_text(80,30, 'Score: ' + str(score), 50, 'red')
        camera.draw(score_display)
        player_die()
        camera.display()

    if screen == 2:
        camera.clear('black')
        camera.draw(uvage.from_text(400, 250, 'Game over!', 100, 'white'))
        camera.draw(uvage.from_text(400, 310, 'Your score was: ' + str(score),35, 'white'))
        camera.draw(uvage.from_text(400, 560, 'Press space bar to return to home screen', 30, 'white'))

        if uvage.is_pressing('space'):
            screen = 0
            score = 0
            score_display = uvage.from_text(80,30, 'Score: ' + str(score), 50, 'red')
            enemies = []
            player.x = 200  # Reset player position
            player.y = 200
            q_ability.x = ability_off_loc.x  # Reset q_ability position
            q_ability.y = ability_off_loc.y
            ult_orb.x = -100  # Reset ult_orb position
            ult_orb.y = -100
            frames = 0
            frames_enemy_spawn = 0
            has_ult = False
        camera.display()


uvage.timer_loop(60, tick)