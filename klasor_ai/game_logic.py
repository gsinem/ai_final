from enum import Enum
import random

class Move(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class GameResult(Enum):
    WIN = 1
    LOSE = -1
    DRAW = 0

class GameLogic:
    @staticmethod
    def get_winner(player_move: Move, ai_move: Move) -> GameResult:
        if player_move == ai_move:
            return GameResult.DRAW
        
        winning_moves = {
            Move.ROCK: Move.SCISSORS,
            Move.PAPER: Move.ROCK,
            Move.SCISSORS: Move.PAPER
        }
        
        if winning_moves[player_move] == ai_move:
            return GameResult.WIN
        return GameResult.LOSE

    @staticmethod
    def get_random_move() -> Move:
        return random.choice(list(Move))

    @staticmethod
    def move_to_string(move: Move) -> str:
        return move.name.capitalize()

    @staticmethod
    def string_to_move(move_str: str) -> Move:
        return Move[move_str.upper()] 