import tkinter as tk
from math import sqrt


memory = 0
expression = ""


root = tk.Tk()
root.title("Standard Calculator")
root.geometry("400x520")
root.configure(bg="#2c3e50")
root.resizable(False, False)

input_text = tk.StringVar()


entry = tk.Entry(root, textvariable=input_text, font=("Segoe UI", 22, "bold"),
                 bd=0, bg="#ffffff", fg="#2c3e50", justify="right")
entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=20, padx=10, pady=20, sticky="nsew")


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

# Button layout
buttons = [
    ["C", "←", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="],
    ["M+", "M-", "MR", ""]
]

btn_font = ("Segoe UI", 16, "bold")
btn_bg = "#bdc3c7"       
btn_fg = "#2c3e50"        
btn_active = "#95a5a6"    

for r, row in enumerate(buttons):
    for c, btn_text in enumerate(row):
        if btn_text == "":
            continue
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
            ction = memory_plus
        elif btn_text == "M-":
            action = memory_minus
        elif btn_text == "MR":
            action = memory_recall

        button = tk.Button(root, text=btn_text, font=btn_font, bg=btn_bg, fg=btn_fg,
                           activebackground=btn_active, activeforeground=btn_fg,
                           bd=0, command=action)
        button.grid(row=r+1, column=c, sticky="nsew", padx=2, pady=2, ipadx=5, ipady=15)


for i in range(6):  
    root.grid_rowconfigure(i, weight=1)
for j in range(4):
    root.grid_columnconfigure(j, weight=1)

root.mainloop()
            