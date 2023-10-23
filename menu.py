
import sys
import pygame
import constants

# Function to handle image loading and error checking
def load_image(path):
    try:
        image = pygame.image.load(path)
        return image.convert() if image else None
    except pygame.error:
        print(f"Error: Unable to load image at {path}")
        return None

# Function to handle font loading and error checking
def load_font(name, size):
    try:
        return pygame.font.SysFont(name, size)
    except pygame.error:
        print(f"Error: Unable to load font {name} with size {size}")
        return pygame.font.Font(None, size)  # default font if desired one is not found

from constants import SCREEN_SIZE, FONTS_SIZE, BUTTON_SPACING_RATIO, WHITE

class Menu:
    # Class method to load and scale images, and load fonts
    @classmethod
    def load_resources(cls):
        background_image = load_image(constants.MENU_BACKGROUND_IMAGE_PATH)
        if background_image:
            background_image = pygame.transform.scale(background_image, SCREEN_SIZE)

        title_font = load_font("Script MT Bold", int(FONTS_SIZE * 3))
        menu_font = load_font("Script MT Bold", int(FONTS_SIZE * 2))

        return background_image, title_font, menu_font

    # Initializer for menu setup
    def __init__(self, screen):
        self.screen = screen
        self.background_image, self.title_font, self.menu_font = self.load_resources()

        # Define menu options
        self.menu_options = [
            constants.NEW_GAME,
            constants.EXIT
        ]

        # Render title text
        self.title_text = self.title_font.render('CHESS GAME', True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3))

        # Setup menu options' texts and positions
        self.option_texts = []
        self.option_rects = []
        self.option_actions = []

        for i, option in enumerate(self.menu_options):
            option_text = self.menu_font.render(option, True, WHITE)
            option_rect = option_text.get_rect(
                center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + i * (SCREEN_SIZE[1] * BUTTON_SPACING_RATIO)))
            self.option_texts.append(option_text)
            self.option_rects.append(option_rect)
            self.option_actions.append(option)

    # Method to draw menu on the screen
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.title_text, self.title_rect)

        for i, option_text in enumerate(self.option_texts):
            self.screen.blit(option_text, self.option_rects[i])

        pygame.display.flip()

    # Method to handle menu events
    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for option_rect, option in zip(self.option_rects, self.option_actions):
                        if option_rect.collidepoint(mouse_pos):
                            if option == constants.NEW_GAME:
                                return True
                            elif option == constants.EXIT:
                                sys.exit()

        return False
