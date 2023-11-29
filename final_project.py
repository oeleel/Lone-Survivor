import uvage
import math
import random

camera = uvage.Camera(800, 600)

player_images = uvage.load_sprite_sheet('sprite_sheet_cs1110.png', 4, 4)
player = uvage.from_image(200,200, player_images[0])
point = uvage.from_circle(400, 300, 'red', 5) #used to show mouseclick on screen

y_down_increment = 0 #goes to 3
x_left_increment = 4 #goes to 7
x_right_increment = 8 #goes to 11
y_up_increment = 12 #goes to 15

last_x_direction = 'right'
last_y_direction = 'down'

#flipped = False
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
    speed = 7

    if hypo != 0:
        tx = (x_dist / hypo) * speed
        ty = (y_dist / hypo) * speed
    else:
        tx = 0
        ty = 0

    player.x += tx
    player.y += ty

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
    spawn_rate = random.randint(1, 90)
    if spawn_rate < 3: #spawn one about every 3 seconds DOES NOT SPAWN EVER 3 SEOCNDS
        enemy = uvage.from_image(-40, -40, 'enemy.png')
        enemy.scale_by(0.1)
        xcoord = random.randint(-40, 840)
        ycoord = random.randint(-40, 640)
        side = random.randint(1, 4) #determines which side of the screen enemy spawns from
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

def chase(): #makes enemy follow player
    global flipped
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


        for q in enemies: #enemies cant overlap
            for w in enemies:
                if q != w:
                    q.move_to_stop_overlapping(w)


def tick():
    camera.clear('black')
    camera.draw(player)
    camera.draw(point)
    player_move()
    spawn_enemy()
    chase()
    for i in enemies:
        camera.draw(i)
    camera.display()


uvage.timer_loop(60, tick)