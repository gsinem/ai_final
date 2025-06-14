import numpy as np
from game_logic import Move, GameResult, GameLogic
from ai_agent import AIAgent
import time

def simulate_games(num_games=1000, player_strategy='random'):
    """
    Simulate games between the AI and a player using different strategies
    
    Args:
        num_games (int): Number of games to simulate
        player_strategy (str): Strategy for the player ('random', 'pattern', or 'counter')
    """
    ai_agent = AIAgent()
    ai_wins = 0
    player_wins = 0
    draws = 0
    
    # For pattern strategy
    pattern = [Move.ROCK, Move.PAPER, Move.SCISSORS]
    pattern_index = 0
    
    print(f"\nStarting simulation with {num_games} games...")
    print(f"Player strategy: {player_strategy}")
    print("-" * 50)
    
    start_time = time.time()
    
    for game in range(num_games):
        # Determine player's move based on strategy
        if player_strategy == 'random':
            player_move = GameLogic.get_random_move()
        elif player_strategy == 'pattern':
            player_move = pattern[pattern_index]
            pattern_index = (pattern_index + 1) % len(pattern)
        elif player_strategy == 'counter':
            # Counter strategy: always choose the move that would have beaten AI's last move
            if game > 0:
                last_ai_move = ai_agent.ai_history[-1]
                winning_moves = {
                    Move.ROCK: Move.PAPER,
                    Move.PAPER: Move.SCISSORS,
                    Move.SCISSORS: Move.ROCK
                }
                player_move = winning_moves[Move(last_ai_move)]
            else:
                player_move = GameLogic.get_random_move()
        
        # Get AI's move
        ai_move = ai_agent.make_move()
        
        # Determine winner
        result = GameLogic.get_winner(player_move, ai_move)
        
        # Update scores
        if result == GameResult.WIN:
            player_wins += 1
        elif result == GameResult.LOSE:
            ai_wins += 1
        else:
            draws += 1
        
        # Update AI's history
        ai_agent.update_history(player_move, ai_move, result)
        
        # Print progress every 100 games
        if (game + 1) % 100 == 0:
            print(f"Completed {game + 1} games...")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Calculate win rates
    total_games = ai_wins + player_wins + draws
    ai_win_rate = (ai_wins / total_games) * 100
    player_win_rate = (player_wins / total_games) * 100
    draw_rate = (draws / total_games) * 100
    
    print("\nSimulation Results:")
    print("-" * 50)
    print(f"Total games played: {total_games}")
    print(f"AI wins: {ai_wins} ({ai_win_rate:.1f}%)")
    print(f"Player wins: {player_wins} ({player_win_rate:.1f}%)")
    print(f"Draws: {draws} ({draw_rate:.1f}%)")
    print(f"Simulation duration: {duration:.2f} seconds")
    print(f"Games per second: {total_games/duration:.1f}")

def main():
    # Test against different player strategies
    strategies = ['random', 'pattern', 'counter']
    
    for strategy in strategies:
        simulate_games(num_games=1000, player_strategy=strategy)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main() 