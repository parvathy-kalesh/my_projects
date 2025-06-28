import tkinter as tk
from math import sqrt

# Memory storage
memory = 0
expression = ""

# Create main window
root = tk.Tk()
root.title("Advanced Calculator")
root.geometry("400x520")
root.configure(bg="#2c3e50")
root.resizable(False, False)

input_text = tk.StringVar()

# Entry field
entry = tk.Entry(root, textvariable=input_text, font=("Segoe UI", 22), bd=0, bg="#ecf0f1",
                 fg="#2c3e50", justify="right")
entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=20, padx=10, pady=20, sticky="nsew")

# Button action functions
def click(value):
    global expression
    expression += str(value)
    input_text.set(expression)

def clear():
    global expression
    expression = ""
    input_text.set("")

def delete():
    global expression
    expression = expression[:-1]
    input_text.set(expression)

def equal():
    global expression
    try:
        result = str(eval(expression))
        input_text.set(result)
        expression = result
    except:
        input_text.set("Error")
        expression = ""

def square_root():
    global expression
    try:
        result = str(sqrt(float(expression)))
        input_text.set(result)
        expression = result
    except:
        input_text.set("Error")
        expression = ""

def percent():
    global expression
    try:
        result = str(float(expression) / 100)
        input_text.set(result)
        expression = result
    except:
        input_text.set("Error")
        expression = ""

def memory_plus():
    global memory, expression
    try:
        memory += float(expression)
    except:
        pass

def memory_minus():
    global memory, expression
    try:
        memory -= float(expression)
    except:
        pass

def memory_recall():
    global memory, expression
    expression = str(memory)
    input_text.set(expression)

# Button definitions
buttons = [
    ["C", "←", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="],
    ["M+", "M-", "MR", ""]
]

# Style
btn_font = ("Segoe UI", 16)
btn_color = "#34495e"
btn_fg = "#ffffff"
btn_active = "#2980b9"

# Create buttons with grid
for r, row in enumerate(buttons):
    for c, btn_text in enumerate(row):
        if btn_text == "":
            continue  # skip empty
        action = lambda x=btn_text: click(x)
        if btn_text == "C":
            action = clear
        elif btn_text == "←":
            action = delete
        elif btn_text == "=":
            action = equal
        elif btn_text == "√":
            action = square_root
        elif btn_text == "%":
            action = percent
        elif btn_text == "M+":
            action = memory_plus
        elif btn_text == "M-":
            action = memory_minus
        elif btn_text == "MR":
            action = memory_recall

        button = tk.Button(root, text=btn_text, font=btn_font, bg=btn_color, fg=btn_fg,
                           activebackground=btn_active, activeforeground="white",
                           bd=0, command=action)
        button.grid(row=r+1, column=c, sticky="nsew", padx=2, pady=2, ipadx=5, ipady=15)

# Configure grid weights for square layout
for i in range(6):  # total rows including entry
    root.grid_rowconfigure(i, weight=1)
for j in range(4):  # 4 columns
    root.grid_columnconfigure(j, weight=1)

root.mainloop()


