from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(development_mode=False)

# blocks
x = 0
y = 0
z = 0
for i in range(128):
	Entity(
		model="cube",
		texture="white_cube",
		color=color.random_color(),
		collider="box",
		position=(x,y,z)
	)
	x += random.randint(1,2)
	y += random.randint(0,1)
	z += random.randint(1,2)

# finish block
y += 1
z += 2
Entity(
	model="cube",
	texture="noise",
	collider="box",
	scale=(2,1,2),
	position=(x,y,z)
)

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
    # quit game [escape]
    if key == "escape":
        quit()

# create the player and run the game
FirstPersonController(gravity=.5)
app.run()