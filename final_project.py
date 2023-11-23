import uvage

camera = uvage.Camera(800, 600)

sheet = uvage.load_sprite_sheet('sprite_sheet_cs1110.png', 4, 4)
player = uvage.from_image(200,200, sheet[0])

def player_move(): # might need to use slope to get character to move in the direction we please
    if camera.mouseclick:






def tick():
    camera.draw(player)
    camera.display()


uvage.timer_loop(60, tick)