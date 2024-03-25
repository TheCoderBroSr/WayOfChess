# Way of Chess
CS Class 12th Project 2024-25

## Project Description
A simplified [﻿chess.com](https://chess.com/) copy :)

Can be accessed @ [﻿github.com/TheCoderBroSr/WayOfChess](https://github.com/TheCoderBroSr/WayOfChess) 

<ins>Note:</ins> Project still in development mode

## Running the Project
1. Clone the GitHub repo
2. Open the CMD (Windows) and change the current directory to the project directory

   ```
   cd <path_to_project>
   ```
   
4. Create a Python virtual environment in the project directory using the following command:
   
   ```
   python -m venv <project_path>/<name_of_venv>
   ```

5. Activate the virtual environment
   
   On windows(CMD):

   ```
   <name_of_venv>\Scripts\Activate
   ```

6. Install the pip dependencies in `requirements.txt` using the following command:

   ```
   pip install -r requirements.txt
   ```

7. Finally, run the flask project using the following command:

   ```
   flask run
   ```

## Gameplay
- **Local 1v1 (White & Black)**
    - Profile creation (skip if already done).
    - Log in to profiles.
- **Different Game Modes**
    - Normal (w/ different time controls)
    - *Checkmate Roulette (checkmate with a random piece)
    - *Piece odds (one player starts with a piece less. E.g. knight odds, bishop odds, rook odds, etc.)
- **Match Analysis**
    - *A different tab where a particular game can be analyzed using a chess engine like Stockfish 16.
      
'*' -> Future implementation

## Other Future Implementations
- vs Bots
- Learning Area (opening prep. / study game positions etc)
- Puzzle Solving
- Leaderboard (Various COD-inspired titles like diamond, platinum etc) (eg. +5/±2/-3 -> W/D/L)


## Possible Project Implementations
- **The game itself**
    1. Web-based approach - using HTML & CSS for the game frontend and chessboard, and Python Flask for the backend.
    2. Local Application - using Python Pygame.
- **Data Management**
    1. MySQL DB - Store small details like player name, match result, etc.
    2. File Handling - Store large details like moves played in localized files.
    3. Data Retrieval - During log-in, *match analysis or *Leaderboard.
    4. Data Insertion - During sign-in, after match etc.

## Team Members
1. [Akuma-no-kami](https://github.com/Akuma-no-kami) - Satvik Singh
2. [YJProjects](https://github.com/YJProjects) - Yashas Jain
3. [TheCoderBroSr](https://github.com/TheCoderBroSr) - Arhant Kumar
