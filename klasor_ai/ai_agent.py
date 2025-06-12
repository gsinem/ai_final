import numpy as np
from collections import deque
from game_logic import Move, GameResult
from sklearn.ensemble import RandomForestClassifier

class AIAgent:
    def __init__(self, memory_size=10):
        self.memory_size = memory_size
        self.player_history = deque(maxlen=memory_size)
        self.ai_history = deque(maxlen=memory_size)
        self.result_history = deque(maxlen=memory_size)
        self.model = RandomForestClassifier(n_estimators=100)
        self.is_trained = False
        self.consecutive_wins = 0
        self.max_consecutive_wins = 2

    def make_move(self) -> Move:
        # If AI is winning too much, occasionally make a random move
        if self.consecutive_wins >= self.max_consecutive_wins and np.random.random() < 0.3:
            self.consecutive_wins = 0
            return self._make_random_move()

        if len(self.player_history) < 3 or not self.is_trained:
            return self._make_random_move()
        
        # Prepare features for prediction
        features = self._prepare_features()
        if features is None:
            return self._make_random_move()
        
        # Predict player's next move
        predicted_move = self.model.predict([features])[0]
        
        # Sometimes make a random move to be less predictable
        if np.random.random() < 0.2:
            return self._make_random_move()
        
        # Choose winning move against predicted player move
        winning_moves = {
            Move.ROCK: Move.PAPER,
            Move.PAPER: Move.SCISSORS,
            Move.SCISSORS: Move.ROCK
        }
        
        return winning_moves[Move(predicted_move)]

    def _make_random_move(self) -> Move:
        return np.random.choice(list(Move))

    def update_history(self, player_move: Move, ai_move: Move, result: GameResult):
        self.player_history.append(player_move.value)
        self.ai_history.append(ai_move.value)
        self.result_history.append(result.value)
        
        # Update consecutive wins counter
        if result == GameResult.LOSE:
            self.consecutive_wins += 1
        else:
            self.consecutive_wins = 0
        
        if len(self.player_history) >= 3:
            self._train_model()

    def _prepare_features(self):
        if len(self.player_history) < 3:
            return None
        
        # Create feature vector from recent history
        features = []
        for i in range(3):
            if i < len(self.player_history):
                features.extend([
                    self.player_history[-i-1],
                    self.ai_history[-i-1],
                    self.result_history[-i-1]
                ])
            else:
                features.extend([0, 0, 0])
        
        return features

    def _train_model(self):
        if len(self.player_history) < 3:
            return
        
        X = []
        y = []
        
        # Create training data from history
        for i in range(len(self.player_history) - 1):
            features = []
            for j in range(3):
                if i + j < len(self.player_history):
                    features.extend([
                        self.player_history[i + j],
                        self.ai_history[i + j],
                        self.result_history[i + j]
                    ])
                else:
                    features.extend([0, 0, 0])
            
            X.append(features)
            y.append(self.player_history[i + 1])
        
        if len(X) > 0:
            self.model.fit(X, y)
            self.is_trained = True 