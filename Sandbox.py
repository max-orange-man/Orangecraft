from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(development_mode=False)

# variables
block_texture = "grass"
block_hue = 80

# voxel class
class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(parent=scene,
            position=position,
            model="cube",
            texture=block_texture,
            color=color.hsv(block_hue,1,1),
            highlight_color=color.white
        )

# starter blocks
for z in range(32):
    for x in range(32):
        Voxel(position=(x-16,0,z-16))

# hand
Entity(
    parent=camera.ui,
    model="cube",
    color="#ffb366",
    scale=(.2,.2,.5),
    rotation=(150,-10),
    position=(.5,-.3)
)

# sky
Entity(
    model="sphere",
    texture="sky_default",
    double_sided=True,
    scale=10000
)

# controls
def input(key):
    # place block [RMB]
    if key == "right mouse down":
        hit_info = raycast(camera.world_position,camera.forward,distance=5)
        if hit_info.hit:
            Voxel(position=hit_info.entity.position+hit_info.normal)

    # break block [LMB]
    if key == "left mouse down" and mouse.hovered_entity:
        hit_info = raycast(camera.world_position,camera.forward,distance=5)
        if hit_info.hit:
            destroy(mouse.hovered_entity)

    # pick grass block [1]
    if key == "1":
        global block_texture, block_hue
        block_texture = "grass"
        block_hue = 80

    # pick wood block [2]
    if key == "2":
        block_texture = "sky_default"
        block_hue = 25

    # pick water block [3]
    if key == "3":
        block_texture = "sky_default"
        block_hue = 180

    # pick brick block [4]
    if key == "4":
        block_texture = "brick"
        block_hue = 0

    # quit game [escape]
    if key == "escape":
        quit()

# create the player and run the game
FirstPersonController()
app.run()