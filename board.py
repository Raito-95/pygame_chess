import pygame
from piece import Pawn, Rook, Knight, Bishop, Queen, King
from constants import SCREEN_SIZE, WHITE, GRAY, RED, LIGHT_BLUE, EXTRA_AREA_COLOR, piece_images


class Board:
    def __init__(self, current_player):
        self.board = self.setup_board()
        self.current_player = current_player
        self.selected_piece = None
        self.last_move = None
        self.move_history = []
        self.half_move_counter = 0
        
        self.max_history_length = 8

    def setup_board(self):
        return [
            [Rook('black', 0, 0), Knight('black', 1, 0), Bishop('black', 2, 0), Queen('black', 3, 0),
             King('black', 4, 0), Bishop('black', 5, 0), Knight('black', 6, 0), Rook('black', 7, 0)],
            [Pawn('black', x, 1) for x in range(8)],
            [None] * 8, [None] * 8, [None] * 8, [None] * 8,
            [Pawn('white', x, 6) for x in range(8)],
            [Rook('white', 0, 7), Knight('white', 1, 7), Bishop('white', 2, 7), Queen('white', 3, 7),
             King('white', 4, 7), Bishop('white', 5, 7), Knight('white', 6, 7), Rook('white', 7, 7)]
        ]

    def reset_board(self):
        self.__init__('white')

    def draw_board(self, screen):
        if self.board is None:
            return
        square_size = SCREEN_SIZE[1] // 8

        for y, x in [(y, x) for y in range(8) for x in range(8)]:
            rect = pygame.Rect(x * square_size, y * square_size, square_size, square_size)
            pygame.draw.rect(screen, WHITE if (x + y) % 2 == 0 else GRAY, rect)
            
            piece = self.board[y][x]
            if piece:
                piece_image = piece_images[f"{piece.color}_{piece.piece_type}"]
                piece_rect = piece_image.get_rect()
                piece_rect.center = rect.center
                screen.blit(piece_image, piece_rect)

                if self.selected_piece and self.selected_piece == (x, y):
                    pygame.draw.rect(screen, RED, rect, 4)

        if self.selected_piece:
            possible_moves = self.get_possible_moves(*self.selected_piece)
            for move_x, move_y in possible_moves:
                highlight_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                highlight_surface.fill((0, 0, 0, 0))
                pygame.draw.rect(highlight_surface, LIGHT_BLUE + (100,), (0, 0, square_size, square_size), 0)
                screen.blit(highlight_surface, (move_x * square_size, move_y * square_size))

        pygame.display.update()

    def draw_extra_area(self, screen):
        extra_area_width = SCREEN_SIZE[0] - SCREEN_SIZE[1]
        extra_area_height = SCREEN_SIZE[1]
        extra_area_rect = pygame.Rect(SCREEN_SIZE[1], 0, extra_area_width, extra_area_height)
        pygame.draw.rect(screen, EXTRA_AREA_COLOR, extra_area_rect)

    def get_piece(self, x, y):
        return self.board[y][x]

    def select_piece(self, x, y):
        piece = self.get_piece(x, y)

        if piece is not None and piece.color == self.current_player:
            self.selected_piece = (x, y)

    def get_possible_moves(self, x, y):
        moves = [(move_x, move_y) for move_y in range(8) for move_x in range(8)
                if self.valid_move(x, y, move_x, move_y)]
        return moves
    
    def valid_move(self, from_x, from_y, to_x, to_y):
        piece = self.get_piece(from_x, from_y)

        if piece is not None and piece.move(self, from_x, from_y, to_x, to_y):
            return True
        return False
    
    def move_piece(self, from_x, from_y, to_x, to_y):
        piece = self.get_piece(from_x, from_y)
        
        if self.board[to_y][to_x] is not None:
            self.half_move_counter = 0

        if self.valid_move(from_x, from_y, to_x, to_y):
            self.board[to_y][to_x] = piece
            self.board[from_y][from_x] = None
            
            self.last_move = ((from_x, from_y), (to_x, to_y))
            self.add_move_to_history(self.last_move)
            self.half_move_counter+=1

            if isinstance(piece, King) and abs(to_x - from_x) == 2:
                rook_from_x = 7 if to_x > from_x else 0
                rook_to_x = (from_x + to_x) // 2
                
                rook = self.get_piece(rook_from_x, from_y)
                self.board[from_y][rook_to_x] = rook
                self.board[from_y][rook_from_x] = None

            if isinstance(piece, Pawn) and abs(from_y - to_y) == 1 and abs(from_x - to_x) == 1:
                self.board[from_y][to_x] = None
            
            return True
        else:
            return False

    def add_move_to_history(self, last_move):
        if len(self.move_history) >= self.max_history_length:
            self.move_history.pop(0)
        self.move_history.append(last_move)

    def pawn_to_promote(self):
        promotion_row = 0 if self.current_player == 'white' else 7

        for x, piece in enumerate(self.board[promotion_row]):
            if isinstance(piece, Pawn):
                return x, promotion_row
        return None, None

    def promote_pawn(self, x, y, piece_type):
        if self.board is None:
            return

        piece = self.get_piece(x, y)
        if piece is None:
            return

        self.board[y][x] = self.create_piece(piece.color, piece_type, x, y)

    def create_piece(self, color, piece_type, x, y):
        if piece_type == 'queen':
            return Queen(color, x, y)
        elif piece_type == 'rook':
            return Rook(color, x, y)
        elif piece_type == 'bishop':
            return Bishop(color, x, y)
        elif piece_type == 'knight':
            return Knight(color, x, y)

    def is_square_under_attack(self, x, y):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(col, row)
                if piece is not None and piece.color != self.current_player:
                    if self.valid_move(col, row, x, y):
                        return True
        return False

    def is_in_check(self):
        king_position = None
        
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color == self.current_player:
                    king_position = (x, y)
                    break
            if king_position:
                break

        if king_position is None:
            return False

        return self.is_square_under_attack(*king_position)

    def is_checkmate(self):
        if not self.is_in_check():
            return False

        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece is not None and piece.color == self.current_player:
                    valid_moves = self.get_possible_moves(x, y)
                    for move in valid_moves:
                        if self.valid_move(x, y, *move):
                            return False
        return True

    def stalemate(self):
        if len(self.move_history) >= 8:
            if self.move_history[-1] == self.move_history[-5] and self.move_history[-3] == self.move_history[-7] and \
                    self.move_history[-2] == self.move_history[-6] and self.move_history[-4] == self.move_history[-8]:
                return True

        if self.half_move_counter >= 100:
            return True

        kings_count = 0
        pieces_count = 0
        for row in self.board:
            for piece in row:
                if isinstance(piece, King):
                    kings_count += 1
                if piece is not None:
                    pieces_count += 1
        if kings_count == 2 and pieces_count == 2:
            return True

        current_player_in_check = self.is_in_check()
        has_valid_moves = False
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece is not None and piece.color == self.current_player:
                    valid_moves = self.get_possible_moves(x, y)
                    if any(self.valid_move(x, y, *move) for move in valid_moves):
                        has_valid_moves = True
                        break
            if has_valid_moves:
                break

        if not current_player_in_check and not has_valid_moves:
            return True

        return False
