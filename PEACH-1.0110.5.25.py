"""
Peach's Castle 3D Render - CatOS 64 Edition
Enhanced visualization and rendering program
Features: Free camera, better lighting, screenshot capability, render modes
"""

from ursina import *
from ursina.shaders import lit_with_shadows_shader
import math

app = Ursina()

# Enhanced color palette
CASTLE_PINK = color.rgb(255, 192, 203)
GRASS_GREEN = color.rgb(34, 139, 34)
SKY_BLUE = color.rgb(135, 206, 250)
STONE_GRAY = color.rgb(169, 169, 169)
DOOR_BROWN = color.rgb(101, 67, 33)
WATER_BLUE = color.rgb(64, 164, 223)
GOLD = color.rgb(255, 215, 0)

# =============================
# ENHANCED LIGHTING SYSTEM
# =============================
sky = Sky(color=SKY_BLUE, texture='white_cube')

# Main directional light (sun)
sun = DirectionalLight(shadows=True, color=color.rgb(255, 250, 240))
sun.look_at(Vec3(1, -1.5, -1))
sun.shadow_map_resolution = (2048, 2048)

# Ambient lighting for softer look
AmbientLight(color=color.rgba(140, 140, 150, 100))

# Accent lights
accent_light_1 = PointLight(parent=scene, position=(-15, 8, -15), color=color.rgb(255, 200, 150))
accent_light_2 = PointLight(parent=scene, position=(15, 8, -15), color=color.rgb(255, 200, 150))

# =============================
# WORLD GEOMETRY - ENHANCED
# =============================

# Ground with subtle texture variation
ground = Entity(
    model='cube', scale=(120, 0.1, 120),
    texture='white_cube', color=GRASS_GREEN, 
    collider='box', shader=lit_with_shadows_shader
)

# Castle base - main structure
castle_base = Entity(
    model='cube', position=(0, 5, -20), scale=(32, 10, 20),
    texture='white_cube', color=CASTLE_PINK, 
    collider='box', shader=lit_with_shadows_shader
)

# Central tower
central_tower = Entity(
    model='cylinder', position=(0, 12, -20), scale=(8, 16, 8),
    texture='white_cube', color=CASTLE_PINK, 
    collider='box', shader=lit_with_shadows_shader
)

# Tower roofs with improved detail
tower_roof = Entity(
    model='cone', position=(0, 21, -20), scale=(10, 8, 10),
    texture='white_cube', color=color.rgb(200, 50, 50),
    shader=lit_with_shadows_shader
)

# Roof top star
roof_star = Entity(
    model='sphere', position=(0, 25, -20), scale=2,
    texture='white_cube', color=GOLD,
    shader=lit_with_shadows_shader
)

# Side towers
left_tower = Entity(
    model='cylinder', position=(-14, 10, -20), scale=(6, 13, 6),
    texture='white_cube', color=CASTLE_PINK, 
    collider='box', shader=lit_with_shadows_shader
)
left_roof = Entity(
    model='cone', position=(-14, 17, -20), scale=(7, 6, 7),
    texture='white_cube', color=color.rgb(200, 50, 50),
    shader=lit_with_shadows_shader
)

right_tower = Entity(
    model='cylinder', position=(14, 10, -20), scale=(6, 13, 6),
    texture='white_cube', color=CASTLE_PINK, 
    collider='box', shader=lit_with_shadows_shader
)
right_roof = Entity(
    model='cone', position=(14, 17, -20), scale=(7, 6, 7),
    texture='white_cube', color=color.rgb(200, 50, 50),
    shader=lit_with_shadows_shader
)

# Main entrance door
door_hinge = Entity(position=(-2.5, 2.5, -10))
main_door = Entity(
    parent=door_hinge, model='cube', 
    position=(2.5, 0, 0), scale=(5, 5, 0.5),
    texture='white_cube', color=DOOR_BROWN, 
    collider='box', shader=lit_with_shadows_shader
)

# Decorative windows
for wx, wy in [(0, 8), (-10, 7), (10, 7), (0, 12)]:
    Entity(
        model='cube', position=(wx, wy, -9.9), scale=(3, 3, 0.2),
        texture='white_cube', color=color.rgba(100, 150, 255, 180),
        shader=lit_with_shadows_shader
    )

# Courtyard walls
wall_left = Entity(
    model='cube', position=(-40, 2.5, 0), scale=(2, 5, 80),
    texture='white_cube', color=STONE_GRAY, 
    collider='box', shader=lit_with_shadows_shader
)
wall_right = Entity(
    model='cube', position=(40, 2.5, 0), scale=(2, 5, 80),
    texture='white_cube', color=STONE_GRAY, 
    collider='box', shader=lit_with_shadows_shader
)
wall_back = Entity(
    model='cube', position=(0, 2.5, 38), scale=(80, 5, 2),
    texture='white_cube', color=STONE_GRAY, 
    collider='box', shader=lit_with_shadows_shader
)

# Moat with transparency
moat = Entity(
    model='cube', position=(0, -0.2, 5), scale=(28, 0.15, 16),
    texture='white_cube', color=color.rgba(64, 164, 223, 160),
    shader=lit_with_shadows_shader
)

# Stone bridge
bridge = Entity(
    model='cube', position=(0, 0.15, 5), scale=(6, 0.25, 16),
    texture='white_cube', color=STONE_GRAY, 
    collider='box', shader=lit_with_shadows_shader
)

# =============================
# ENHANCED TREES
# =============================
class DetailedTree(Entity):
    def __init__(self, position=(0, 0, 0), scale_factor=1):
        super().__init__(position=position)
        # Trunk
        Entity(
            parent=self, model='cube', 
            position=(0, 1.5*scale_factor, 0), 
            scale=(1*scale_factor, 3*scale_factor, 1*scale_factor),
            texture='white_cube', color=color.rgb(101, 67, 33),
            shader=lit_with_shadows_shader
        )
        # Foliage layers
        for i, (h, s) in enumerate([(3.5, 4.5), (4.8, 3.5), (5.8, 2.5)]):
            Entity(
                parent=self, model='sphere',
                position=(0, h*scale_factor, 0),
                scale=(s*scale_factor, s*0.8*scale_factor, s*scale_factor),
                texture='white_cube', color=color.rgb(0, 128 + i*10, 0),
                shader=lit_with_shadows_shader
            )

# Place trees around courtyard
tree_positions = [
    (-28, 0, 22), (28, 0, 22),
    (-28, 0, 0), (28, 0, 0),
    (-28, 0, -8), (28, 0, -8),
    (-22, 0, 28), (22, 0, 28),
    (-18, 0, 18), (18, 0, 18),
    (-12, 0, 25), (12, 0, 25)
]

for pos in tree_positions:
    DetailedTree(position=pos, scale_factor=1.0)

# =============================
# DECORATIVE ELEMENTS
# =============================

# Entrance pillars
for x in [-10, 10]:
    pillar = Entity(
        model='cylinder', position=(x, 2.5, -5), scale=(1.8, 5, 1.8),
        texture='white_cube', color=STONE_GRAY, 
        collider='box', shader=lit_with_shadows_shader
    )
    pillar_top = Entity(
        model='cube', position=(x, 5.2, -5), scale=(2.5, 0.5, 2.5),
        texture='white_cube', color=STONE_GRAY,
        shader=lit_with_shadows_shader
    )

# Decorative bushes
bush_positions = [
    (-16, 0.5, -8), (16, 0.5, -8),
    (-10, 0.5, -2), (10, 0.5, -2),
    (-20, 0.5, 10), (20, 0.5, 10),
    (0, 0.5, 18), (-8, 0.5, 15), (8, 0.5, 15)
]

for pos in bush_positions:
    Entity(
        model='sphere', position=pos, scale=(2.5, 1.2, 2.5),
        texture='white_cube', color=color.rgb(0, 100, 0),
        shader=lit_with_shadows_shader
    )

# Animated coins as decorative elements
class AnimatedCoin(Entity):
    def __init__(self, position=(0, 1, 0)):
        super().__init__(
            model='cylinder', position=position, 
            scale=(1, 0.15, 1),
            texture='white_cube', color=GOLD,
            shader=lit_with_shadows_shader
        )
        self.base_y = self.y
        self.t = position[0] + position[2]  # phase offset

    def update(self):
        self.rotation_y += 80 * time.dt
        self.t += time.dt * 2
        self.y = self.base_y + math.sin(self.t) * 0.2

# Place decorative coins
for pos in [(6, 1.5, 12), (-6, 1.5, 12), (0, 1.5, 18), (10, 1.5, 2), (-10, 1.5, 2)]:
    AnimatedCoin(position=pos)

# Rotating star on top of castle
def update_star():
    roof_star.rotation_y += 30 * time.dt
    roof_star.y += math.sin(time.time() * 2) * 0.003

# =============================
# CAMERA SYSTEM - FREE ROAM
# =============================
class FreeCamera(Entity):
    def __init__(self):
        super().__init__()
        self.position = Vec3(0, 15, 40)
        self.rotation = Vec3(20, 0, 0)
        self.speed = 20
        self.rotation_speed = 50
        camera.parent = self
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 75

    def update(self):
        # WASD movement
        direction = Vec3(
            held_keys['d'] - held_keys['a'],
            held_keys['e'] - held_keys['q'],  # E/Q for up/down
            held_keys['w'] - held_keys['s']
        ).normalized()
        
        speed = self.speed * (2 if held_keys['shift'] else 1)
        self.position += self.forward * direction.z * speed * time.dt
        self.position += self.right * direction.x * speed * time.dt
        self.position += self.up * direction.y * speed * time.dt
        
        # Mouse look
        if held_keys['right mouse']:
            self.rotation_y += mouse.velocity[0] * self.rotation_speed
            self.rotation_x -= mouse.velocity[1] * self.rotation_speed
            self.rotation_x = clamp(self.rotation_x, -89, 89)

cam_controller = FreeCamera()
mouse.locked = False

# =============================
# UI & CONTROLS
# =============================
render_mode = 0
render_modes = ['Lit', 'Wireframe', 'Normals']

ui_panel = Entity(model='quad', parent=camera.ui, z=1, 
                  scale=(0.4, 0.2), position=(-0.65, 0.42),
                  color=color.rgba(0, 0, 0, 180))

title = Text(
    "PEACH'S CASTLE - 3D RENDER",
    position=(-0.85, 0.48), scale=1.8,
    color=color.white, background=True
)

controls = Text(
    "WASD: Move | E/Q: Up/Down | SHIFT: Fast\nRight Mouse: Look | 1-3: Render Modes\nF11: Fullscreen | F12: Screenshot | ESC: Quit",
    position=(-0.85, 0.42), scale=1,
    color=color.azure, background=True
)

mode_text = Text(
    f"Render Mode: {render_modes[render_mode]}",
    position=(-0.85, 0.36), scale=1.1,
    color=color.yellow, background=True
)

fps_text = Text(
    "FPS: 60",
    position=(0.7, 0.48), scale=1.2,
    color=color.lime, background=True
)

# =============================
# CAMERA PRESETS
# =============================
camera_presets = [
    {"pos": Vec3(0, 15, 40), "rot": Vec3(20, 0, 0), "name": "Front View"},
    {"pos": Vec3(0, 25, -35), "rot": Vec3(35, 180, 0), "name": "Rear View"},
    {"pos": Vec3(45, 20, 0), "rot": Vec3(25, 270, 0), "name": "Side View"},
    {"pos": Vec3(0, 50, 0), "rot": Vec3(89, 0, 0), "name": "Top View"},
    {"pos": Vec3(-25, 12, 15), "rot": Vec3(15, 35, 0), "name": "Scenic View"}
]
current_preset = 0

def set_camera_preset(index):
    global current_preset
    current_preset = index % len(camera_presets)
    preset = camera_presets[current_preset]
    cam_controller.position = preset["pos"]
    cam_controller.rotation = preset["rot"]
    invoke(lambda: setattr(Text(preset["name"], scale=2, origin=(0,0), 
           position=(0, 0), background=True), 'enabled', False), delay=1.5)

# =============================
# INPUT HANDLING
# =============================
def input(key):
    global render_mode
    
    if key == 'escape':
        quit()
    
    # Render modes
    elif key == '1':
        render_mode = 0
        for e in scene.entities:
            if hasattr(e, 'shader'):
                e.shader = lit_with_shadows_shader
        mode_text.text = f"Render Mode: {render_modes[render_mode]}"
    
    elif key == '2':
        render_mode = 1
        for e in scene.entities:
            e.shader = None
        mode_text.text = f"Render Mode: {render_modes[render_mode]}"
    
    elif key == '3':
        render_mode = 2
        mode_text.text = f"Render Mode: {render_modes[render_mode]} (not impl.)"
    
    # Camera presets
    elif key == 'space':
        set_camera_preset(current_preset + 1)
    
    # Screenshot
    elif key == 'f12':
        screenshot_name = f'peach_castle_{int(time.time())}.png'
        try:
            window.screenshot(screenshot_name)
            Text(f"Screenshot saved: {screenshot_name}", scale=1.5, origin=(0,0),
                 position=(0, -0.3), background=True, duration=2)
        except:
            Text("Screenshot failed", scale=1.5, origin=(0,0),
                 position=(0, -0.3), background=True, color=color.red, duration=2)
    
    # Fullscreen
    elif key == 'f11':
        window.fullscreen = not window.fullscreen
    
    # Lock/unlock mouse
    elif key == 'tab':
        mouse.locked = not mouse.locked

# =============================
# MAIN UPDATE LOOP
# =============================
def update():
    update_star()
    fps_text.text = f"FPS: {int(1/time.dt) if time.dt > 0 else 60}"
    
    # Gentle camera sway when idle (optional cinematic effect)
    if not any([held_keys['w'], held_keys['a'], held_keys['s'], held_keys['d']]):
        cam_controller.rotation_y += math.sin(time.time() * 0.3) * 0.02

# =============================
# WINDOW CONFIG
# =============================
window.title = "Peach's Castle 3D Render - CatOS 64"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False

# Initial camera preset
set_camera_preset(0)

app.run()
