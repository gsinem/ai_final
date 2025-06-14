import numpy as np
from collections import deque
from game_logic import Move, GameResult
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class AIAgent:
    def __init__(self, memory_size=15):
        self.memory_size = memory_size
        self.player_history = deque(maxlen=memory_size)
        self.ai_history = deque(maxlen=memory_size)
        self.result_history = deque(maxlen=memory_size)
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.consecutive_wins = 0
        self.max_consecutive_wins = 3
        self.pattern_detected = False
        self.pattern_length = 0
        self.pattern_moves = []
        self.pattern_confidence = 0.0
        self.min_pattern_confidence = 0.7

    def make_move(self) -> Move:
        if self.pattern_detected and len(self.pattern_moves) > 0 and self.pattern_confidence >= self.min_pattern_confidence:
            pattern_prob = min(self.pattern_confidence, 0.6)
            if np.random.random() < pattern_prob:
                next_move = self.pattern_moves[0]
                self.pattern_moves = self.pattern_moves[1:] + [next_move]
                return next_move

        if self.consecutive_wins >= self.max_consecutive_wins and np.random.random() < 0.2:
            self.consecutive_wins = 0
            return self._make_random_move()

        if len(self.player_history) < 3 or not self.is_trained:
            return self._make_random_move()
        
        features = self._prepare_features()
        if features is None:
            return self._make_random_move()
        
        features_scaled = self.scaler.transform([features])
        
        predicted_move = self.model.predict(features_scaled)[0]
        
        if np.random.random() < 0.15:
            return self._make_random_move()
        
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
        
        if result == GameResult.LOSE:
            self.consecutive_wins += 1
        else:
            self.consecutive_wins = 0
        
        self._detect_patterns()
        
        if len(self.player_history) >= 3:
            self._train_model()

    def _detect_patterns(self):
        if len(self.player_history) < 6:
            return

        max_confidence = 0.0
        best_pattern = None
        best_pattern_length = 0

        for pattern_len in range(2, 6):
            if len(self.player_history) >= pattern_len * 3:
                patterns = []
                for i in range(3):
                    start_idx = -(i+1) * pattern_len
                    end_idx = -i * pattern_len if i > 0 else None
                    patterns.append(list(self.player_history)[start_idx:end_idx])
                
                if patterns[0] == patterns[1] == patterns[2]:
                    confidence = 0.5 + (pattern_len / 10)
                    if confidence > max_confidence:
                        max_confidence = confidence
                        best_pattern = patterns[0]
                        best_pattern_length = pattern_len

        if best_pattern is not None:
            self.pattern_detected = True
            self.pattern_length = best_pattern_length
            self.pattern_confidence = max_confidence
            self.pattern_moves = []
            for move in best_pattern:
                winning_moves = {
                    Move.ROCK: Move.PAPER,
                    Move.PAPER: Move.SCISSORS,
                    Move.SCISSORS: Move.ROCK
                }
                self.pattern_moves.append(winning_moves[Move(move)])
        else:
            self.pattern_detected = False
            self.pattern_length = 0
            self.pattern_moves = []
            self.pattern_confidence = 0.0

    def _prepare_features(self):
        if len(self.player_history) < 3:
            return None
        
        features = []
        for i in range(5):
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
        
        for i in range(len(self.player_history) - 1):
            features = []
            for j in range(5):
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
            X = self.scaler.fit_transform(X)
            self.model.fit(X, y)
            self.is_trained = True 