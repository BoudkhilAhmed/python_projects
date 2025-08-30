import tkinter as tk
from tkinter import ttk

# ---------- Logic ----------
new_operation = False

def update_calc(char):
    global new_operation
    operation_txt = operation.get().strip('0')
    operation_result = compute_opr(operation_txt)

    if char == '=':
        update_history(operation_txt)

        if isnumber(operation_result):
            result.set(str(operation_result))
        else:
            operation.set(f'Er: {operation_result}')
            result.set('')
            
        new_operation = True

    elif char == '⌫':
        operation.set(operation_txt[:-1])
        new_operation = False
    elif char == 'C':
        operation.set('')
        new_operation = False
    else:
        if new_operation == True:
            operation.set(result.get())
            new_operation = False
        operation.set(operation.get() + char)

def update_history(operation_txt):
    with open('history.txt', 'a') as hisFile:
        try:
            hisFile.write(f'{operation_txt} = {str(eval(operation_txt))}\n')
        except Exception as e:
            hisFile.write(f'{operation_txt} = {e}\n')
        
def show_history():
    win = tk.Toplevel(calc)
    win.title("History")
    text = tk.Text(win, width=30, height=10)
    text.pack()
    try:
        with open("history.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            lines = lines[::-1]
            text.insert("1.0", "".join(lines[:6]))
    except:
        text.insert("1.0", "No history yet.")

def compute_opr(operation_txt):
    try:
        result = round(eval(str(operation_txt)), 4)
    except Exception as e:
        return str(e)
    return str(result)

def isnumber(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# ---------- UI ----------
# Palette & Fonts
BG = "#222831"
CARD = "#2a2f36"
TXT = "#eeeeee"
RESULT_TXT = "#565656ff"
ACCENT = "#00adb5"
DANGER = "#ff4d4f"
MUTED = "#4d535e"

DISPLAY_FONT = ("Segoe UI", 22)
BTN_FONT = ("Segoe UI", 14)
RESULT_FONT = ("Segoe UI", 16)

# Calc Window
calc = tk.Tk()
calc.title("Calculator")
calc.geometry("320x500")
calc.columnconfigure(0, weight=1)
calc.rowconfigure(0, weight=1)
calc.configure(bg=BG)

# Dark Style
style = ttk.Style(calc)
style.theme_use("clam")
style.configure("Root.TFrame", background=BG)
style.configure("Card.TFrame", background=CARD)

style.configure("Display.TLabel",
    background=CARD, foreground=TXT,
    font=DISPLAY_FONT, anchor="w", padding=(12, 14)
)
style.configure("DisplayR.TLabel",
    background=CARD, foreground=TXT,
    font=DISPLAY_FONT, anchor="w", padding=(12, 14)
)
style.configure("Digit.TButton", font=BTN_FONT, padding=10,
    background=MUTED, foreground=TXT, borderwidth=0
)
style.map("Digit.TButton",
    background=[("active", "#5a616d"), ("pressed", "#6b7380")]
)
style.configure("Op.TButton", font=("Segoe UI", 14, "bold"),
    padding=10, background=ACCENT, foreground="#ffffff"
)
style.map("Op.TButton",
    background=[("active", "#11c3cd"), ("pressed", "#0fb0b9")]
)
style.configure("Action.TButton", 
    font=BTN_FONT, padding=10,
    background="#f66", foreground="#ffffff"
)
style.map("Action.TButton",
    background=[("active", "#ff7a7c"), ("pressed", "#ff5e60")]
)
style.configure("Equal.TButton", font=("Segoe UI", 16, "bold"),
    padding=10, background=DANGER, foreground="#ffffff"
)
style.map("Equal.TButton",
    background=[("active", "#ff6d6f"), ("pressed", "#ff5759")]
)

# Calculator Frame
root_frame = ttk.Frame(calc, style="Root.TFrame", padding=12)
root_frame.rowconfigure(0, weight=1)
root_frame.columnconfigure(0, weight=1)

# Operation & Result Frame
card = ttk.Frame(root_frame, style="Card.TFrame", padding=10)
card.rowconfigure(0, weight=1)
card.rowconfigure(1, weight=1)
card.rowconfigure(2, weight=1)
card.columnconfigure(0, weight=1)

operation = tk.StringVar(value="")
result = tk.StringVar(value="result")
display_opr = ttk.Label(card, textvariable=operation, style="Display.TLabel")
display_result = ttk.Label(card, textvariable=result, style="DisplayR.TLabel")

# keys Frame
keys = ttk.Frame(card, style="Card.TFrame")
for r in range(5):
    keys.rowconfigure(r, weight=1)
for c in range(4):
    keys.columnconfigure(c, weight=1)

def make_btn(parent, text, style_name, r, c, cmd, span=1):
    b = ttk.Button(parent, text=text, style=style_name, command=cmd, cursor="hand2")
    b.grid(row=r, column=c, columnspan=span, sticky="nsew", padx=3, pady=3)
    return b

# Row 0: C, ⌫, ÷, 🕓
make_btn(keys, "C",   "Action.TButton", 0, 0, lambda: update_calc('C'))
make_btn(keys, "⌫", "Action.TButton", 0, 1, lambda: update_calc('⌫'))
make_btn(keys, "÷",   "Op.TButton",     0, 2, lambda: update_calc('/'))
make_btn(keys, "🕓",   "Digit.TButton",     0, 3, lambda: show_history())

# Digits & ops
digits = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("-", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("+", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("*", 3, 3),
    ("0", 4, 0), (".", 4, 1)
]
for t, r, c in digits:
    style_name = "Digit.TButton" if t.isdigit() or t == "." else "Op.TButton"
    make_btn(keys, t, style_name, r, c, lambda ch=t: update_calc(ch))

# Equal button spans two columns
make_btn(keys, "=", "Equal.TButton", 4, 2, lambda: update_calc('='), span=2)

# grid
root_frame.grid(row=0, column=0, sticky="nsew")
card.grid(row=1, column=0, sticky="nsew")
display_opr.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 8))
display_result.grid(row=1, column=0, columnspan=4, sticky="nse", pady=(0, 8))
keys.grid(row=2, column=0, sticky="nsew")


calc.mainloop()
