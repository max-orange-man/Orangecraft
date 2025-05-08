from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.ursfx import ursfx
from ursina.prefabs.health_bar import HealthBar

app = Ursina(development_mode=False)

# starter grass blocks
for z in range(32):
    for x in range(32):
        Entity(
            model="cube",
            texture="grass",
            color=color.hsv(80,1,1),
            collider="box",
            position=(x-16,0,z-16)
        )

# starter brick blocks
for i in range(64):
    Entity(
        model="cube",
        texture="brick",
        color=color.red,
        collider="box",
        x=random.randint(-16,16),
        y=1,
        z=random.randint(-16,16),
    )

# sky
Entity(
    model="sphere",
    texture="sky_sunset",
    double_sided=True,
    scale=10000
)

# player
player = FirstPersonController(z=-10)
player.collider = BoxCollider(player, (0,1,0), (1,2,1))

# gun
gun = Entity(model="cube", parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.gray, on_cooldown=False)
gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model="quad", color=color.yellow, enabled=False)

shootables_parent = Entity()
mouse.traverse_target = shootables_parent

# controls
def update():
    # shoot [LMB]
    if held_keys["left mouse"]:
        shoot()
def input(key):
    # quit game [escape]
    if key == "escape":
        quit()

# shoot function
def shoot():
    if not gun.on_cooldown:
        gun.on_cooldown = True
        gun.muzzle_flash.enabled = True
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave="noise", pitch=random.uniform(-13,-12), pitch_change=-12, speed=3.0)
        invoke(gun.muzzle_flash.disable, delay=.05)
        invoke(setattr, gun, "on_cooldown", False, delay=.15)
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, "hp"):
            mouse.hovered_entity.hp -= 10
            mouse.hovered_entity.blink(color.red)

# enemy (zombie) class
class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model="cube", scale_y=2, origin_y=-.5, texture="sky_default", color=color.green, collider="box", **kwargs)
        self.health_bar = Entity(parent=self, y=1.2, model="cube", color=color.red, world_scale=(1.5,.1,.1))
        self.max_hp = 100
        self.hp = self.max_hp

    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 40:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(player.position, "y")
        hit_info = raycast(self.world_position + (0,1,0), self.forward, 30, ignore=(self))
        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1

# enemies (zombies)
for z in range(3):
    for x in range(3):
        Enemy(x=x*4-2, z=z*3)

# run the game
app.run()