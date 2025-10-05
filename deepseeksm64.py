from ursina import *

app = Ursina()

# Define a simple block texture or color
class CastleBlock(Entity):
    def __init__(self, position, scale, texture='white_cube'):
        super().__init__(
            model='cube',
            color=color.white,
            texture=texture,
            position=position,
            scale=scale
        )

# Create a ground plane
ground = Entity(model='plane', texture='grass', scale=(40, 1, 40), y=-0.5)

# Build the main central tower
CastleBlock(position=(0, 5, 0), scale=(6, 10, 6))

# Add the main hall/entrance section
CastleBlock(position=(0, 2, -8), scale=(10, 4, 4))

# Create four smaller surrounding towers
tower_positions = [(5, 3, 5), (-5, 3, 5), (5, 3, -5), (-5, 3, -5)]
for pos in tower_positions:
    CastleBlock(position=pos, scale=(3, 6, 3))

# Set up the camera for a classic view
camera.position = (15, 15, -15)
camera.look_at((0, 0, 0))

app.run()
