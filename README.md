# Scripting-Project
This project automates/scripts using python the compilation and organization of game source code files written in Go. It searches for directories containing the keyword "game," compiles the Go code within, and organizes the compiled games into a target directory.

## Installation
- Python installed (3.9 or higher)
- Go installed (required for compiling Go code) - https://go.dev/

## Usage
Clone the repository to your local machine or download zip folder, then in terminal run this command (cla). 
This passes the two arguments which are the source (where we are looking=data), and the target (where we want to put the new dir=target).
```
python get_game_data.py data target
```

##Screenshots
![image](https://github.com/ahmadbasyouni10/Scripting-Project/assets/120362910/4c0ec71d-8f61-472f-9233-92440b7baca2)

Directory Path should be created, with the games compiled in it
![image](https://github.com/ahmadbasyouni10/Scripting-Project/assets/120362910/02e73da2-d8db-4a9b-80f7-3b0aa6d84227)


