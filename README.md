# ai_final
# Rock-Paper-Scissors AI Game

A Python-based Rock-Paper-Scissors game featuring an intelligent AI opponent that learns from player patterns and adapts its strategy. The game combines machine learning with traditional game logic to create an engaging and challenging experience.

## Features

- Interactive GUI with clickable buttons
- AI opponent that learns from player patterns
- Real-time score tracking
- Visual feedback for game outcomes
- Adaptive AI difficulty
- Modern and user-friendly interface

## Technical Implementation

### AI Architecture
The AI uses a hybrid approach combining:
- Machine Learning (Random Forest Classifier)
- Pattern Recognition
- Adaptive Strategy
- Rule-based Logic

### Key Components
1. **Game Logic** (`game_logic.py`)
   - Core game mechanics
   - Move validation
   - Win condition checking

2. **AI Agent** (`ai_agent.py`)
   - Pattern recognition
   - Move prediction
   - Adaptive learning
   - Difficulty balancing

3. **Game Interface** (`main.py`)
   - Pygame-based GUI
   - Interactive buttons
   - Score display
   - Move history

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/gsinem/ai_final/]
cd rock-paper-scissors-ai
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. Game Controls:
   - Click the "Rock" button to play Rock
   - Click the "Paper" button to play Paper
   - Click the "Scissors" button to play Scissors
   - Press 'Q' to quit the game

## AI Implementation Details

### Learning Mechanism
- The AI maintains a history of:
  - Player moves
  - AI moves
  - Game results
- Uses this history to predict player patterns
- Adapts strategy based on player behavior

### Difficulty Balancing
- Implements consecutive win tracking
- Random move generation to prevent predictability
- Adaptive difficulty based on player performance

## Dependencies

- Python 3.8+
- Pygame 2.5.2
- NumPy 1.24.3
- scikit-learn 1.3.0

## Project Structure

```
rock-paper-scissors-ai/
├── main.py           # Main game loop and GUI
├── ai_agent.py       # AI implementation
├── game_logic.py     # Game rules and logic
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation
```

## Future Improvements

- Add sound effects
- Implement different AI difficulty levels
- Add game statistics and analytics
- Create a tournament mode
- Add multiplayer support

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
