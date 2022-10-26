import time
import random
import os
import keyboard
from bprint import bprint
from player import Player
from bomb import Bomb

# board dimensions, must be even
X_MAX = Y_MAX = 15

board = [] # matrix of integers -> 0 = empty space, 1 = breakable wall, 2 = fire, 3 = unbreakable wall
bombs = [] # list of Bomb
p1 = Player(0, 0, 1, 1)

# keyboard controls: w, a, s, d, space
def on_press_w(_): move_player(p1.x, p1.y-1)
def on_press_a(_): move_player(p1.x-1, p1.y)
def on_press_s(_): move_player(p1.x, p1.y+1)
def on_press_d(_): move_player(p1.x+1, p1.y)
def on_press_space(_): bombs.append(Bomb(p1.x, p1.y, 12, p1.fire))

# create a new board with random walls
def generate_board():
    global board

    # create breakable walls
    for i in range(X_MAX):
        board.append([])
        for j in range(Y_MAX):
            board[i].append(random.randint(0, 1))

    # create unbreakable walls
    for i in range(1, X_MAX, 2):
        for j in range(1, Y_MAX, 2):
            board[i][j] = 3

    # reserve borders for players
    board[0][0]   = board[1][0]   = board[0][1] = 0
    board[0][-1]  = board[1][-1]  = board[0][-2] = 0
    board[-1][0]  = board[-2][0]  = board[-1][1] = 0
    board[-1][-1] = board[-2][-1] = board[-1][-2] = 0


# draw board, players and bombs
def draw():
    for i in range(X_MAX+2): bprint.p("X", bprint.PINK) # upper board border
    print("")
    for i in range(X_MAX):
        bprint.p("X", bprint.PINK) # left board border
        for j in range(Y_MAX):
            if i == p1.y and j == p1.x: # block is a player
                bprint.p("P", bprint.OKGREEN)
                continue
            is_bomb = False
            for bomb in bombs:
                if i == bomb.y and j == bomb.x: # block is a bomb
                    is_bomb = True
                    bomb.draw()
                    break
            if is_bomb: continue
            elif board[i][j] == 0: bprint.p(" ", bprint.BOLD)  # block is an empty space
            elif board[i][j] == 1: bprint.p("W", bprint.WHITE) # block is a wall
            elif board[i][j] == 2: bprint.p("*", bprint.RED)   # block is a fire
            elif board[i][j] == 3: bprint.p("X", bprint.PINK)  # block is an unbreakable wall
        bprint.p("X", bprint.PINK) # right board border
        print("")
    for i in range(X_MAX+2): bprint.p("X", bprint.PINK) # bottom board border
    print("\n")
    print(f'{bprint.OKGREEN}Player 1: 🔥{p1.fire} 💣{p1.bombs}{bprint.ENDC}') # player status


# move player if new position is valid
def move_player(x, y):
    if board[y][x] == 0 and x>=0 and y>=0 and x<=X_MAX and y<=Y_MAX:
        p1.x = x
        p1.y = y


# every block that is not a type 3 (unbreakable) should become fire
def block_explode(x, y):
    global board
    if board[x][y] != 3: board[x][y] = 2


# transform fire blocks into empty spaces
def block_free(x, y):
    global board
    if board[x][y] == 2: board[x][y] = 0


# when timer is 0 the bomb explodes; when timer is -3 the fire disappears
def process_bombs():
    global bombs, board

    # decrease timers
    for i in range(len(bombs)):
        bombs[i].timer -= 1

    # find which bombs are exploding and/or exploded
    exploding = []
    exploded = []
    for i in range(len(bombs)):
        if bombs[i].timer == 0:
            exploding.append(i)
        if bombs[i].timer == -3:
            exploded.append(i)

    # TODO: this part only works if range=1
    # transform adjacent walls into fire
    for b in exploding:
        bomb = bombs[b]
        for i in (0, bomb.range):
            block_explode(bomb.y+i, bomb.x)
            block_explode(bomb.y-i, bomb.x)
            block_explode(bomb.y, bomb.x+i)
            block_explode(bomb.y, bomb.x-i)

    # TODO: this part only works if range=1
    # transform fire blocks into empty squares and delete bomb from list
    for b in exploded:
        bomb = bombs[b]
        print(bomb.range)
        for i in (0, bomb.range):
            block_free(bomb.y+i, bomb.x)
            block_free(bomb.y-i, bomb.x)
            block_free(bomb.y, bomb.x+i)
            block_free(bomb.y, bomb.x-i)
        board[bomb.y][bomb.x] = 0
        del bombs[b]


if __name__ == "__main__":
    generate_board()
    keyboard.on_press_key("w", on_press_w)
    keyboard.on_press_key("a", on_press_a)
    keyboard.on_press_key("s", on_press_s)
    keyboard.on_press_key("d", on_press_d)
    keyboard.on_press_key("space", on_press_space)
    while True:
        os.system('clear')
        draw()
        process_bombs()
        time.sleep(0.1)

