import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageDraw, ImageTk

folder = os.path.dirname(os.path.abspath(__file__))
img_folder = folder + '/img'

size = 80
pad = 15
radius = 15

human = 'X'
bot = 'O'

lines = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def win(b, p):
    for a, c, d in lines:
        if b[a] == b[c] == b[d] == p:
            return True
    return False


def full(b):
    return ' ' not in b


def empty(b):
    return [i for i, v in enumerate(b) if v == ' ']


def minimax(b, d, mx):
    if win(b, bot):
        return 10 - d
    if win(b, human):
        return d - 10
    if full(b):
        return 0

    if mx:
        best = -999
        for i in empty(b):
            b[i] = bot
            s = minimax(b, d + 1, False)
            b[i] = ' '
            if s > best:
                best = s
        return best

    best = 999
    for i in empty(b):
        b[i] = human
        s = minimax(b, d + 1, True)
        b[i] = ' '
        if s < best:
            best = s
    return best


def bot_move(b):
    best = -999
    idx = None
    for i in empty(b):
        b[i] = bot
        s = minimax(b, 0, False)
        b[i] = ' '
        if s > best:
            best = s
            idx = i
    return idx


def load_img(name):
    for ext in ('.png', '.jpg', '.jpeg', '.gif', '.bmp'):
        p = img_folder + '/' + name + ext
        if os.path.exists(p):
            inner = size - pad
            im = Image.open(p).convert("RGB").resize((inner, inner), Image.LANCZOS)
            mask = Image.new("L", (inner, inner), 0)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, inner - 1, inner - 1), radius=radius, fill=255)
            tile = Image.new("RGB", (size, size), (255, 255, 255))
            tile.paste(im, (pad // 2, pad // 2), mask)
            return ImageTk.PhotoImage(tile, master=root)
    return None


root = tk.Tk()
root.title("Крестики-нолики")
root.resizable(False, False)
root.configure(bg='white')

w, h = 400, 480
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

pic_x = load_img('x')
pic_o = load_img('o')

board = [' ' for i in range(9)]
cells = []
wait = False


def set_mark(w, who):
    if who == human and pic_x:
        w.config(image=pic_x, text='')
    elif who == bot and pic_o:
        w.config(image=pic_o, text='')
    else:
        w.config(image='', text=who, fg='blue' if who == human else 'red')


def click(i):
    global wait
    if wait or board[i] != ' ':
        return
    if win(board, human) or win(board, bot) or full(board):
        return

    board[i] = human
    set_mark(cells[i], human)

    if win(board, human):
        messagebox.showinfo("Игра окончена", "Вы победили!")
        wait = True
        return
    if full(board):
        messagebox.showinfo("Игра окончена", "Ничья!")
        wait = True
        return

    wait = True
    root.after(200, bot_turn)


def bot_turn():
    global wait
    i = bot_move(board)
    if i is not None:
        board[i] = bot
        set_mark(cells[i], bot)

    if win(board, bot):
        messagebox.showinfo("Игра окончена", "Компьютер победил!")
        wait = True
        return
    if full(board):
        messagebox.showinfo("Игра окончена", "Ничья!")
        wait = True
        return

    wait = False


def restart():
    global board, wait
    board = [' ' for i in range(9)]
    wait = False
    for c in cells:
        c.config(image='', text=' ', fg='black')


grid = tk.Frame(root, bg='white')
grid.pack(pady=20)

for i in range(9):
    box = tk.Frame(grid, width=size, height=size, bg='white', borderwidth=1, relief='solid')
    box.grid(row=i // 3, column=i % 3, padx=2, pady=2)
    box.grid_propagate(False)
    box.pack_propagate(False)

    lbl = tk.Label(box, text=' ', font=('Arial', 40, 'bold'), bg='white', image='')
    lbl.place(x=0, y=0, relwidth=1, relheight=1)
    lbl.bind("<Button-1>", lambda e, idx=i: click(idx))
    cells.append(lbl)

tk.Button(root, text='Новая игра', font=('Arial', 14), command=restart).pack(pady=10)

root.mainloop()