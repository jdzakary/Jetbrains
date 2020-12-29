import random
import sqlite3

random.seed()

conn = sqlite3.connect('Tic_Tac_Toe_Database.s3db')
cur = conn.cursor()

board_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
current_player = 'X'
game_over = False
move_array = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
turn = 1

# Win Conditions
diagonal_1 = board_state[0][0] + board_state[1][1] + board_state[2][2]
diagonal_2 = board_state[2][0] + board_state[1][1] + board_state[0][2]
column_1 = board_state[0][0] + board_state[1][0] + board_state[2][0]
column_2 = board_state[0][1] + board_state[1][1] + board_state[2][1]
column_3 = board_state[0][2] + board_state[1][2] + board_state[2][2]
row_1 = board_state[0][0] + board_state[0][1] + board_state[0][2]
row_2 = board_state[1][0] + board_state[1][1] + board_state[1][2]
row_3 = board_state[2][0] + board_state[2][1] + board_state[2][2]

# List of win conditions
win_conditions = {1: diagonal_1, 2: diagonal_2, 3: column_1, 4: column_2, 5: column_3, 6: row_1, 7: row_2, 8: row_3}

# Convert matrix index to linear index
converter = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1], 9: [2, 2]}


def board_print():
    row1 = '| ' + board_state[0][0] + ' ' + board_state[0][1] + ' ' + board_state[0][2] + ' |'
    row2 = '| ' + board_state[1][0] + ' ' + board_state[1][1] + ' ' + board_state[1][2] + ' |'
    row3 = '| ' + board_state[2][0] + ' ' + board_state[2][1] + ' ' + board_state[2][2] + ' |'
    print('---------')
    print(row1)
    print(row2)
    print(row3)
    print('---------')


def setup_board():
    linear_state = input('Enter the cells: ')
    valid_count = linear_state.count('_') + linear_state.count('X') + linear_state.count('O')
    if len(linear_state) != 9:
        print('You must supply exactly 9 squares!')
        setup_board()
    elif valid_count != 9:
        print('The only valid characters are: _ X O')
        setup_board()
    else:
        linear_state = linear_state.replace('_', ' ')
        row1 = [linear_state[0], linear_state[1], linear_state[2]]
        row2 = [linear_state[3], linear_state[4], linear_state[5]]
        row3 = [linear_state[6], linear_state[7], linear_state[8]]
        global board_state
        board_state = [row1, row2, row3]


def check_string(string, number=3):
    if string.count('X') == number:
        return True, 'X'
    elif string.count('O') == number:
        return True, 'O'
    else:
        return False, None


def check_diagonals():
    valid_1, player_1 = check_string(diagonal_1)
    valid_2, player_2 = check_string(diagonal_2)
    if valid_1 is True:
        print(player_1 + ' wins')
        return False
    elif valid_2 is True:
        print(player_2 + ' wins')
        return False
    else:
        return True


def check_rows():
    valid_1, player_1 = check_string(row_1)
    valid_2, player_2 = check_string(row_2)
    valid_3, player_3 = check_string(row_3)
    if valid_1 is True:
        print(player_1 + ' wins')
        return False
    elif valid_2 is True:
        print(player_2 + ' wins')
        return False
    elif valid_3 is True:
        print(player_3 + ' wins')
        return False
    else:
        return True


def check_columns():
    valid_1, player_1 = check_string(column_1)
    valid_2, player_2 = check_string(column_2)
    valid_3, player_3 = check_string(column_3)
    if valid_1 is True:
        print(player_1 + ' wins')
        return False
    elif valid_2 is True:
        print(player_2 + ' wins')
        return False
    elif valid_3 is True:
        print(player_3 + ' wins')
        return False
    else:
        return True


def check_board(minmax=False):
    global game_over
    global diagonal_1
    global diagonal_2
    global column_1
    global column_2
    global column_3
    global row_1
    global row_2
    global row_3
    global win_conditions
    diagonal_1 = board_state[0][0] + board_state[1][1] + board_state[2][2]
    diagonal_2 = board_state[2][0] + board_state[1][1] + board_state[0][2]
    column_1 = board_state[0][0] + board_state[1][0] + board_state[2][0]
    column_2 = board_state[0][1] + board_state[1][1] + board_state[2][1]
    column_3 = board_state[0][2] + board_state[1][2] + board_state[2][2]
    row_1 = board_state[0][0] + board_state[0][1] + board_state[0][2]
    row_2 = board_state[1][0] + board_state[1][1] + board_state[1][2]
    row_3 = board_state[2][0] + board_state[2][1] + board_state[2][2]
    win_conditions = {1: diagonal_1, 2: diagonal_2, 3: column_1, 4: column_2, 5: column_3, 6: row_1, 7: row_2, 8: row_3}
    test_list = [check_diagonals(), check_columns(), check_rows()]
    linear_state = [symbol for row in board_state for symbol in row]
    empty = linear_state.count(' ')
    if all(test_list):
        if empty == 0 and minmax is False:
            print('Draw')
            game_over = True
        elif minmax is False:
            pass
        else:
            return 'Draw'
    elif minmax is False:
        game_over = True


def modify_board(player, x=None, y=None, manual=False):
    global board_state
    global move_array
    global turn
    if manual is True:
        coordinates = input('Enter the coordinates: ').split()
        coordinates = [w for w in coordinates]
        if len(coordinates) == 2:
            x = coordinates[1]
            y = coordinates[0]
        else:
            x = 'A'
            y = 'A'
        if x.isdigit() and y.isdigit():
            x = int(x)
            y = int(y)
            if 1 <= x <= 3 and 1 <= y <= 3:
                y -= 1
                x -= 1
                if board_state[y][x] == ' ':
                    board_state[y][x] = player
                    for key, value in converter.items():
                        if value == [y, x]:
                            move_array[turn] = key
                    turn += 1
                else:
                    print('This cell is occupied! Choose another one!')
                    modify_board(player, manual=True)
            else:
                print('Coordinates should be from 1 to 3!')
                modify_board(player, manual=True)
        else:
            print('You should enter numbers!')
            modify_board(player, manual=True)
    else:
        if board_state[y][x] == ' ':
            board_state[y][x] = player
            for key, value in converter.items():
                if value == [y, x]:
                    move_array[turn] = key
            turn += 1
            return True
        else:
            return False


def update_player():
    global current_player
    linear_state = [symbol for row in board_state for symbol in row]
    count_x = linear_state.count('X')
    count_o = linear_state.count('O')
    if count_o < count_x:
        current_player = 'O'
    else:
        current_player = 'X'


def computer_easy():
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    while modify_board(current_player, x, y) is False:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
    modify_board(current_player, x, y)


def computer_medium():
    moves = 0
    for condition, contents in win_conditions.items():
        if contents.count(' ') == 1:
            valid, player = check_string(contents, 2)
            if valid and player == current_player:
                z = contents.index(' ')
                conditions_vector = {1: [z, z], 2: [2-z, z], 3: [z, 0], 4: [z, 1], 5: [z, 2], 6: [0, z], 7: [1, z], 8: [2, z]}
                x = conditions_vector[condition][0]
                y = conditions_vector[condition][1]
                modify_board(current_player, y, x)
                moves += 1
                break
    for condition, contents in win_conditions.items():
        if contents.count(' ') == 1 and moves == 0:
            valid, player = check_string(contents, 2)
            if valid and player != current_player:
                z = contents.index(' ')
                conditions_vector = {1: [z, z], 2: [2-z, z], 3: [z, 0], 4: [z, 1], 5: [z, 2], 6: [0, z], 7: [1, z], 8: [2, z]}
                x = conditions_vector[condition][0]
                y = conditions_vector[condition][1]
                modify_board(current_player, y, x)
                moves += 1
                break
    if moves == 0:
        computer_easy()
        moves += 1


def computer_hard():
    moves = 0
    for condition, contents in win_conditions.items():
        if contents.count(' ') == 1:
            valid, player = check_string(contents, 2)
            if valid and player == current_player:
                z = contents.index(' ')
                conditions_vector = {1: [z, z], 2: [2 - z, z], 3: [z, 0], 4: [z, 1], 5: [z, 2], 6: [0, z], 7: [1, z],
                                     8: [2, z]}
                x = conditions_vector[condition][0]
                y = conditions_vector[condition][1]
                modify_board(current_player, y, x)
                moves += 1
                break
    for condition, contents in win_conditions.items():
        if contents.count(' ') == 1 and moves == 0:
            valid, player = check_string(contents, 2)
            if valid and player != current_player:
                z = contents.index(' ')
                conditions_vector = {1: [z, z], 2: [2 - z, z], 3: [z, 0], 4: [z, 1], 5: [z, 2], 6: [0, z], 7: [1, z],
                                     8: [2, z]}
                x = conditions_vector[condition][0]
                y = conditions_vector[condition][1]
                modify_board(current_player, y, x)
                moves += 1
                break
    if board_state[1][1] == 'X' and turn == 2:
        modify_board(current_player, 0, 0)
        moves += 1
    if moves == 0:
        sql_conditions = ''
        current_move = 1
        remaining_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for key, value in move_array.items():
            if value != 0:
                if len(sql_conditions) == 0:
                    sql_conditions += 'move' + str(key) + ' = ' + str(value)
                else:
                    sql_conditions += ' AND move' + str(key) + ' = ' + str(value)
                current_move += 1
                remaining_moves.remove(value)

        best = -100
        for move in remaining_moves:
            if len(sql_conditions) == 0:
                new_conditions = 'move' + str(current_move) + ' = ' + str(move)
            else:
                new_conditions = sql_conditions + ' AND move' + str(current_move) + ' = ' + str(move)
            cur.execute("select * from games_2 where " + new_conditions)
            results = cur.fetchall()
            total_score = 0
            for x in range(0, len(results)):
                if results[x][9] == current_player:
                    score = 50 + results[x].count(0)
                elif results[x][9] != 'D':
                    score = -50 - results[x].count(0)
                else:
                    score = 0
                total_score += score
            if len(results) != 0:
                average = total_score / len(results)
            else:
                average = 0
            if average > best:
                best = average
                best_move = move

        for key, value in converter.items():
            if best_move == key:
                y = converter[key][0]
                x = converter[key][1]
        modify_board(current_player, x, y)

def make_move(difficulty):
    if difficulty == 'easy':
        computer_easy()
        print('Making move level "easy"')
    elif difficulty == 'medium':
        computer_medium()
        print('Making move level "medium"')
    elif difficulty == 'hard':
        computer_hard()
        print('Making move level "hard"')
    elif difficulty == 'user':
        modify_board(current_player, manual=True)
    else:
        print('That difficulty does not exist!')


def home():
    actions = input('Input command: ').split()
    if actions[0] == 'start':
        if len(actions) == 3:
            global game_over
            global board_state
            global move_array
            global turn
            while game_over is False:
                board_print()
                check_board()
                update_player()
                if game_over is False:
                    pass
                else:
                    break
                make_move(actions[1])
                board_print()
                check_board()
                update_player()
                if game_over is False:
                    pass
                else:
                    break
                make_move(actions[2])
            game_over = False
            board_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            move_array = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
            turn = 1
            print()
            home()
        else:
            print('Bad parameters!')
            home()
    elif actions[0] == 'exit':
        exit()
    else:
        print('Bad parameters!')
        home()


home()
