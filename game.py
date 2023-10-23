import pygame
import logging

from board import Board
from constants import SCREEN_SIZE, FPS
from dialog import Dialog

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.dialog = Dialog(screen)
        self.clock = pygame.time.Clock()

        self.running = True
        self.players = {'white': 0, 'black': 1}
        self.current_player = 'white'
        self.board = Board(self.current_player)

        self.square_size = SCREEN_SIZE[1] // 8


    def screen_to_board_coords(self, screen_x, screen_y):
        return screen_x // self.square_size, screen_y // self.square_size

    def draw_board(self):
        self.board.draw_board(self.screen)
        self.board.draw_extra_area(self.screen) 
        for button in self.dialog.buttons:
            self.dialog.draw_button(button["rect"], button["label"])

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.board.current_player = self.current_player

    def handle_game_end(self):
        if self.board.is_checkmate():
            winner = "Black" if self.current_player == 'white' else "White"
            self.dialog.show_message(f"{winner} Wins!")
            self.board.reset_board()
        elif self.board.stalemate():
            self.dialog.show_message("Draw!")
            self.board.reset_board()

    def handle_promotion(self):
        x, y = self.board.pawn_to_promote()
        if x is not None and y is not None:
            self.dialog.show_promotion(x, y, self.board)
        
    def handle_click(self, pos):
        x, y = self.screen_to_board_coords(*pos)
        for button in self.dialog.buttons:
            if button["rect"].collidepoint(x * self.square_size, (y + 1) * self.square_size - 1):
                action = button["action"]
                if action == "proposal":
                    if self.dialog.show_proposal():
                        self.dialog.show_message("Draw!")
                        self.board.reset_board()
                elif action == "surrender":
                    self.dialog.show_message(f"{self.current_player} has surrendered!")

        if not (0 <= x < 8) or not (0 <= y < 8):
            return
        piece = self.board.get_piece(x, y)
        
        if self.board.selected_piece is None:
            if piece is not None and piece.color == self.current_player:
                self.board.select_piece(x, y)
        elif (x, y) == self.board.selected_piece:
            self.board.selected_piece = None
        else:
            if piece is not None and piece.color == self.current_player:
                self.board.selected_piece = None
                self.board.select_piece(x, y)
            else:
                if self.board.move_piece(self.board.selected_piece[0], self.board.selected_piece[1], x, y):
                    self.handle_promotion()
                    self.handle_game_end()
                    self.switch_player()
                    self.board.selected_piece = None

    def run(self):
        while self.running:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_click(event.pos)

            self.draw_board()
            
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
