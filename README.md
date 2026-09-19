# Los Álamos Chess AI

An AI agent for **Los Álamos Chess**, a simplified 6×6 chess variant, developed as the final project for the **Introduction to Artificial Intelligence** course at the **Universidad Nacional de Colombia**.

The project models the game as an **adversarial search problem**, implementing **Minimax with Alpha-Beta Pruning**, multiple evaluation heuristics, and an interactive graphical interface.

## Demo

🎥 **Project video:**  
https://drive.google.com/file/d/17j08n8xWiGeZ8xqK4pbjEBlvFDNu25VO/view

---

## About Los Álamos Chess

Los Álamos Chess was created in the 1950s as one of the earliest chess variants used for artificial intelligence research.

Compared to standard chess, it uses:

- 6×6 board
- No bishops
- No castling
- No en passant
- No initial two-square pawn move
- Automatic pawn promotion

These simplifications reduce complexity while preserving the strategic nature of adversarial search.

---

## Features

- Minimax search with configurable depth.
- Alpha-Beta Pruning for reducing explored branches.
- Three evaluation heuristics with different play styles.
- Complete move generation for all supported pieces.
- Interactive graphical interface built in Python.
- Automatic game simulation for heuristic comparisons.

---

## Search Algorithm

The agent searches the game tree using **Minimax** while alternating between maximizing and minimizing players.

Alpha-Beta Pruning significantly reduces unnecessary exploration, making deeper searches feasible without changing the final decision.

<AsyncImage query="minimax alpha beta pruning game tree diagram" aspectRatio="16:9" maxHeight=420/>

### State Representation

Each game state contains:

- 6×6 board matrix
- Current player's turn

Successor states are generated from every legal move according to Los Álamos Chess rules.

---

## Evaluation Heuristics

The project compares three different evaluation functions.

### Material Advantage

Classic piece-value evaluation.

| Piece | Value |
|------|------:|
| Pawn | 1 |
| Knight | 3 |
| Rook | 5 |
| Queen | 9 |
| King | 1000 |

Fast and effective for tactical positions.

### Center Control

Combines material with control of the four central squares.

Designed to encourage stronger opening play and positional development.

### Dynamic King

Adapts evaluation depending on the game phase.

- **Middlegame:** prioritizes king safety.
- **Endgame:** encourages king activity and centralization.

This produces a more context-aware playing style.

---

## Experimental Results

The project evaluates the agent under different search depths and heuristics.

### Search Depth

| Depth | Avg. Time | Expanded Nodes |
|------:|----------:|---------------:|
| 1 | 0.016 s | 104 |
| 2 | 0.232 s | 3,246 |
| 3 | 1.249 s | 42,680 |

Increasing depth improves decision quality but also causes exponential growth in explored states.

### Heuristic Comparison

At depth 3:

| Heuristic | Avg. Time | Winner |
|-----------|----------:|--------|
| Material | 0.405 s | Black |
| Center | 1.275 s | White |
| Dynamic King | 1.756 s | White |

Across multiple simulated games:

- **Center** consistently outperformed Material in opening play.
- **Dynamic King** achieved stronger performance during longer games and endgames.
- **Material** remained the fastest heuristic.

---

## Technologies

- Python
- Pyglet
- Object-Oriented Programming
- Minimax
- Alpha-Beta Pruning

---

## Project Structure

```text
proyecto2IA/
├── main.py
├── tablero.py
├── jugador.py
├── pieza.py
├── heuristicas.py
├── interfaz.py
├── assets/
└── README.md
```

*(Adjust the structure if your repository changes.)*

---

## Future Improvements

- Move ordering for faster Alpha-Beta pruning.
- Transposition tables and state caching.
- Improved positional heuristics.
- Reinforcement Learning for stronger gameplay.

---

## Authors

- Deiver Jair Bernal Garzón
- Tania Julieth Araque Dueñas
- Brayan Manuel Rubiano Páramo

**Universidad Nacional de Colombia**  
Introduction to Artificial Intelligence — 2025

