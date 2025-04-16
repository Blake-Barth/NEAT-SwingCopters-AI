# 🧠 NEAT SwingCopters AI Agent

This project demonstrates a **NEAT** (NeuroEvolution of Augmenting Topologies)–based AI agent that learns to play **SwingCopters** — a fast-paced game inspired by *Flappy Bird*, where the player (or AI) must navigate through swinging obstacles.

---

## 🚀 Getting Started

### Requirements

- Python 3.7+
- `pygame`
- `neat-python`

Install all dependencies with:

```bash
pip install -r requirements.txt

🎮 How to Play Manually

To play the game yourself, run:

python play_game.py

Controls:

    🖱️ Click to start the game

    🖱️ Click again to change the copter’s direction

    ␣ Press Space to restart after a game over

Try to avoid the swinging obstacles and aim for the highest score!
🤖 Watch the AI Agent

To watch the AI agent (trained using NEAT) play the game, run:

python run_NEAT.py

The algorithm will evolve and control the copter automatically, improving its performance over generations.
📁 Project Structure

.
├── play_game.py              # Manual gameplay script
├── run_NEAT.py               # Runs NEAT algorithm to evolve the AI agent
├── requirements.txt          # Python dependencies
├── config/
│   └── config-feedforward.txt    # NEAT configuration file
├── classes/
│   ├── copter.py             # Copter class
│   ├── obstacle.py           # Obstacle logic
│   └── ...                   # Other game-related objects
├── audio/
│   └── ...                   # Game sound effects
├── images/
│   └── ...                   # Game sprites and background assets
└── models/                   # (Optional) Saved genomes or checkpoints


---

Let me know if you want to add a **GIF demo**, badges (like Python version or license), or a section on **how NEAT works** behind the scenes!

