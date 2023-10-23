import sys
import pygame
from pygame import mixer
from menu import Menu
from game import Game
from constants import SCREEN_SIZE, ICON_PATH, BACKGROUND_MUSIC_PATH

# Function to load resources with error handling
def load_resource(path, type='image'):
    try:
        if type == 'image':
            return pygame.image.load(path)
        elif type == 'music':
            mixer.music.load(path)
    except pygame.error:
        print(f"Error: Unable to load {type}: {path}")
        if type == 'image':
            return None

# Function to run the game menu
def run_menu(screen):
    menu = Menu(screen)

    while True:
        if menu.process_event():
            break

        menu.draw()

# Function to initialize game settings and resources
def initialize_game():
    icon = load_resource(ICON_PATH)
    if icon:
        pygame.display.set_icon(icon)
    
    pygame.display.set_caption('Chess Game')

    music = load_resource(BACKGROUND_MUSIC_PATH, 'music')
    if music is not None:
        mixer.music.play(-1)

# Main function to initialize pygame and start the game
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    
    initialize_game()
    run_menu(screen)

    game = Game(screen)
    game.run()

    sys.exit() 


if __name__ == "__main__":
    main()
