import tkinter as tk
import metaheuristics
import LPsolver


def create_board(n):
    board = []
    for _ in range(n):
        row = [0] * n
        board.append(row)
    return board


def button_click(row, col):
    if board[row][col] == 0:
        board[row][col] = 1
        buttons[row][col].configure(bg='black', activebackground='gray25')
    elif board[row][col] == 1:
        board[row][col] = '0'
        buttons[row][col].configure(text='0')
    elif board[row][col] == '4':
        board[row][col] = 0
        buttons[row][col].configure(text='', bg='white', activebackground='gray75')
    elif type(board[row][col]) == str:
        temp = str(int(board[row][col])+1)
        board[row][col] = temp
        buttons[row][col].configure(text=temp)


def save_board():
    for row in board:
        print(row)
    print('\n\n\n')
    eksport(board)


def change_size():
    new_size = int(size_entry.get())

    for row in buttons:
        for button in row:
            button.destroy()

    for row in buttons_meta:
        for button in row:
            button.destroy()

    for row in buttons_lp:
        for button in row:
            button.destroy()

    global board
    board = create_board(new_size)
    create_board_buttons(new_size)


def create_board_buttons(n):
    global buttons, buttons_meta, buttons_lp

    buttons = []
    for row in range(n):
        button_row = []
        for col in range(n):
            button = tk.Button(board_frame1, text='', width=2, height=1, bg='white', activebackground='gray75', fg='white',
                               activeforeground='white', bd=1, command=lambda r=row, c=col: button_click(r, c))
            button.grid(row=row, column=col)
            button_row.append(button)
        buttons.append(button_row)

    buttons_meta = []
    for row in range(n):
        button_row = []
        for col in range(n):
            button = tk.Button(board_frame2, text='', width=2, height=1, bg='white', activebackground='gray75', fg='white',
                               activeforeground='white', bd=1)
            button.grid(row=row, column=col)
            button_row.append(button)
        buttons_meta.append(button_row)

    buttons_lp = []
    for row in range(n):
        button_row = []
        for col in range(n):
            button = tk.Button(board_frame3, text='', width=2, height=1, bg='white', activebackground='gray75', fg='white',
                               activeforeground='white', bd=1)
            button.grid(row=row, column=col)
            button_row.append(button)
        buttons_lp.append(button_row)



def create_gui(n):
    global root, board, board_frame1, board_frame2, board_frame3, size_entry

    root = tk.Tk()
    root.title("Akari Solver")

    control_frame = tk.Frame(root)
    control_frame.grid(row=0, column=0, columnspan=3, pady=10)

    tk.Label(control_frame, text="Board size:").grid(row=0, column=0)
    size_entry = tk.Entry(control_frame, width=5)
    size_entry.grid(row=0, column=1)
    size_entry.insert(0, str(n))

    size_button = tk.Button(control_frame, text="Change size", command=change_size)
    size_button.grid(row=0, column=2)

    board_frame1 = tk.Frame(root)
    board_frame1.grid(row=1, column=0, padx=10, pady=10)

    board_frame2 = tk.Frame(root)
    board_frame2.grid(row=1, column=1, padx=10, pady=10)

    board_frame3 = tk.Frame(root)
    board_frame3.grid(row=1, column=2, padx=10, pady=10)

    board = create_board(n)
    create_board_buttons(n)

    board_label = tk.Label(root, text="Board")
    board_label.grid(row=2, column=0, padx=5, pady=5)

    meta_label = tk.Label(root, text="Metaheuristics")
    meta_label.grid(row=2, column=1, padx=5, pady=5)

    lp_label = tk.Label(root, text="Linear Programming")
    lp_label.grid(row=2, column=2, padx=5, pady=5)

    save_button = tk.Button(root, text="Solve", command=save_board)
    save_button.grid(row=3, columnspan=3)

    root.mainloop()


def eksport(board):
    meta_board = [] #metaheuristics: 0 - empty field; 1 - field with light; 'wall' - wall field
    n = len(board)
    wall = 0
    wall_notclear = 0

    connections = [[0 for _ in range(n ** 2)] for _ in range(n ** 2)]

    # auxiliary variables about wall limitations
    limitwall_val= []
    limitwall_idx = []

    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                meta_board.append(0)
                connections[(i*n)+j][(i*n)+j] = 1
                try:
                    k = 1
                    while board[i][j+k] == 0:
                        connections[(i*n)+j][(i*n)+j+k] = 1
                        k += 1
                except IndexError:
                    pass
                try:
                    k = 1
                    while board[i][j-k] == 0 and j - k >= 0:
                        connections[(i*n)+j][(i*n)+j-k] = 1
                        k += 1
                except IndexError:
                    pass
                try:
                    k = 1
                    while board[i+k][j] == 0:
                        connections[(i*n)+j][((i + k) * n) + j] = 1
                        k += 1
                except IndexError:
                    pass
                try:
                    k = 1
                    while board[i-k][j] == 0 and i - k >= 0:
                        connections[(i*n)+j][((i - k) * n) + j] = 1
                        k += 1
                except IndexError:
                    pass


            else:
                meta_board.append('wall')
                wall += 1
                if board[i][j] != 1:
                    wall_notclear += 1
                    limitwall_val.append(int(board[i][j]))
                    temp = []
                    if i + 1 <= n - 1 and board[i+1][j] == 0:
                        temp.append(((i + 1) * n) + j + 1)
                    if j + 1 <= n - 1 and board[i][j+1] == 0:
                        temp.append((i * n) + j + 2)
                    if i - 1 >= 0 and board[i-1][j] == 0:
                        temp.append(((i - 1) * n) + j + 1)
                    if j - 1 >= 0 and board[i][j-1] == 0:
                        temp.append((i * n) + j)

                    limitwall_idx.append(temp)


        columns = []
        rows = []
        for i in range(n):
            temp = []
            for j in range(n):
                if board[i][j] == 0:
                    temp.append((i*n)+j+1)
                else:
                    rows.append(temp)
                    temp = []
                if j == n - 1:
                    rows.append(temp)
        for j in range(n):
            temp = []
            for i in range(n):
                if board[i][j] == 0:
                    temp.append((i*n)+j+1)
                else:
                    columns.append(temp)
                    temp = []
                if i == n - 1:
                    columns.append(temp)

        while [] in columns:
            columns.remove([])

        while [] in rows:
            rows.remove([])

    # print(meta_board)
    # print(wall)
    # print(wall_notclear)
    # print(connections)
    # print(limitwall_val)
    # print(limitwall_idx)
    # print(columns)
    # print(rows)
    # print()

    show_solved_meta(limitwall_idx, limitwall_val, columns, rows, connections, meta_board, board)
    show_solved_lp(limitwall_idx, limitwall_val, columns, rows, connections, wall, board)


def check_if_light(connections, meta_board, idx):
    temp = 0
    for i in range(len(connections[idx])):
        if type(meta_board[i]) != str:
            temp += meta_board[i] * connections[idx][i]
        if temp > 0:
            return True
    return False

def show_solved_meta(limitwall_idx, limitwall_val, columns, rows, connections, meta_board, board):
    solved_board, score, time_meta = metaheuristics.metaheuristics(limitwall_idx, limitwall_val, columns, rows, connections, meta_board)
    print(solved_board, score, time_meta)

    for row in range(len(board)):
        for col in range(len(board[0])):
            if solved_board[len(board) * row + col] == 0:
                is_lighten = check_if_light(connections, solved_board, len(board) * row + col)
                if is_lighten:
                    buttons_meta[row][col].configure(bg='#f7ffa8', text='')
                else:
                    buttons_meta[row][col].configure(bg='white', text='')
            elif solved_board[len(board) * row + col] == 1:
                buttons_meta[row][col].configure(bg='yellow', text='o', fg='black')
            else:
                text = '' if board[row][col] == 1 else board[row][col]
                buttons_meta[row][col].configure(bg='black', text=text, fg='white')

def show_solved_lp(limitwall_idx, limitwall_val, columns, rows, connections, wall, board):
    solved_board, score, time_meta = LPsolver.lp_solve(wall, connections, limitwall_val, limitwall_idx, columns, rows)
    print(solved_board, score, time_meta)

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] != 0:
                text = '' if board[row][col] == 1 else board[row][col]
                buttons_lp[row][col].configure(bg='black', text=text, fg='white')
            elif solved_board[len(board) * row + col] == 0:
                is_lighten = check_if_light(connections, solved_board, len(board) * row + col)
                if is_lighten:
                    buttons_lp[row][col].configure(bg='#f7ffa8', text='')
                else:
                    buttons_lp[row][col].configure(bg='white', text='')
            elif solved_board[len(board) * row + col] == 1:
                buttons_lp[row][col].configure(bg='yellow', text='o', fg='black')
            else:
                buttons_lp[row][col].configure(bg='white', text='')


# n = int(input("Enter the board size: "))
# create_gui(n)
if __name__ == "__main__":
    create_gui(4)
