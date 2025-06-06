"""Manages the game"""

import chess


class GameManager:
    def __init__(self, board, player_white, player_black):
        self.board = board
        self.players = {chess.WHITE: player_white, chess.BLACK: player_black}
        self.current_turn = chess.WHITE
        self.move_history = []

    def handle_turn(self):
        player = self.players[self.current_turn]

        if player.is_human:
            # Wait for human input via drag/drop
            return
        else:
            move = player.choose_move(self.board)
            if move in self.board.legal_moves:
                self.make_move(move)

    def make_move(self, move):
        self.board.push(move)
        self.move_history.append(move)
        self.current_turn = not self.current_turn
