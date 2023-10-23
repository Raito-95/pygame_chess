
import pygame

# Screen configuration
SCREEN_SIZE = (1000, 640)

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
LIGHT_BLUE = (180, 255, 255)
EXTRA_AREA_COLOR = (240, 240, 240)

# UI element sizes relative to the screen
BUTTON_WIDTH_RATIO = 0.18
BUTTON_HEIGHT_RATIO = 0.08
BUTTON_SPACING_RATIO = 0.12
FONTS_SIZE = int(SCREEN_SIZE[1] * 0.06)

# Calculated button dimensions
BUTTON_WIDTH = int(SCREEN_SIZE[0] * BUTTON_WIDTH_RATIO)
BUTTON_HEIGHT = int(SCREEN_SIZE[1] * BUTTON_HEIGHT_RATIO)

# Preloading piece images
piece_images = {}
pieces = {
    'white_pawn':   ('white', 'pawn'),
    'white_rook':   ('white', 'rook'),
    'white_knight': ('white', 'knight'),
    'white_bishop': ('white', 'bishop'),
    'white_queen':  ('white', 'queen'),
    'white_king':   ('white', 'king'),
    'black_pawn':   ('black', 'pawn'),
    'black_rook':   ('black', 'rook'),
    'black_knight': ('black', 'knight'),
    'black_bishop': ('black', 'bishop'),
    'black_queen':  ('black', 'queen'),
    'black_king':   ('black', 'king')
}

# Loading images for each piece type
for key, (color, name) in pieces.items():
    piece_images[key] = pygame.image.load(f"assets/image/{color}_{name}.png")

# Paths for assets
ICON_PATH = "assets/icon/favicon.ico"
BACKGROUND_MUSIC_PATH = "assets/music/background.mp3"

# Menu options
NEW_GAME = "NEW GAME"
PRACTICE_MODE = "PRACTICE MODE"
EXIT = "EXIT"

# Menu background image path
MENU_BACKGROUND_IMAGE_PATH = "assets/image/menu_background.png"

# Frames per second for the game loop
FPS = 30
