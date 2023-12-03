import uvage
import random
import math

camera = uvage.Camera(800, 600)
mc = uvage.from_circle(400, 300, 'black', 20)
point = uvage.from_circle(400, 300, 'red', 5)



def move_mc():
    if camera.mouseclick:
        point.center = camera.mouse

    ydist = abs(point.y - mc.y)
    xdist = abs(point.x - mc.x)
    hypo = math.sqrt((ydist ** 2) + (xdist ** 2))
    t = hypo / 7
    if t == 0:
        tx = xdist
        ty = ydist
    else:
        tx = xdist / t
        ty = ydist / t

    if point.x > mc.x:
        mc.x += tx
    if point.x < mc.x:
        mc.x += -tx
    if point.y > mc.y:
        mc.y += ty
    if point.y < mc.y:
        mc.y += -ty






def tick():
    camera.clear('white')
    camera.draw(mc)
    camera.draw(point)
    move_mc()
    camera.display()

uvage.timer_loop(30, tick)