import tkinter as tk

root = tk.Tk()
root.title("Styled Basic Calculator")
root.geometry("320x450")
root.resizable(False, False)
root.configure(bg="#282c34")

expression = ""

equation = tk.StringVar()
equation.set("0")

# Display entry
display = tk.Entry(root, textvariable=equation, font=("Segoe UI", 24), bd=0,
                   bg="#1e222a", fg="#ffffff", justify="right", relief="flat",
                   highlightthickness=2, highlightbackground="#444a57", highlightcolor="#ff9500")
display.pack(fill="x", ipady=15, padx=15, pady=20)

btns_frame = tk.Frame(root, bg="#282c34")
btns_frame.pack(expand=True, fill="both")

btn_bg = "#5c6170"
btn_fg = "#f0f0f0"
op_bg = "#ff9500"
op_fg = "#fff"
btn_font = ("Segoe UI", 18, "bold")
btn_active_bg = "#707683"
op_active_bg = "#ffb84d"

def on_enter(e):
    e.widget['background'] = btn_active_bg if e.widget['bg'] == btn_bg else op_active_bg

def on_leave(e):
    e.widget['background'] = btn_bg if e.widget['bg'] == btn_active_bg else op_bg

def press(num):
    global expression
    if expression == "Error":
        expression = ""
    expression += str(num)
    equation.set(expression)

def clear():
    global expression
    expression = ""
    equation.set("0")

def equalpress():
    global expression
    try:
        result = str(eval(expression))
        equation.set(result)
        expression = result
    except:
        equation.set("Error")
        expression = ""

def backspace():
    global expression
    expression = expression[:-1]
    if expression == "":
        equation.set("0")
    else:
        equation.set(expression)

def create_button(text, row, column, width=1, command=None, bg=btn_bg, fg=btn_fg):
    btn = tk.Button(btns_frame, text=text, bg=bg, fg=fg, font=btn_font,
                    bd=0, relief="flat", command=command, activebackground=btn_active_bg,
                    activeforeground=fg, cursor="hand2")
    btn.grid(row=row, column=column, sticky="nsew", padx=8, pady=8, columnspan=width)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

for i in range(5):
    btns_frame.rowconfigure(i, weight=1)
for i in range(4):
    btns_frame.columnconfigure(i, weight=1)

create_button("C", 0, 0, command=clear, bg=op_bg, fg=op_fg)
create_button("⌫", 0, 1, command=backspace, bg=op_bg, fg=op_fg)
create_button("÷", 0, 2, command=lambda: press("/"), bg=op_bg, fg=op_fg)
create_button("×", 0, 3, command=lambda: press("*"), bg=op_bg, fg=op_fg)

create_button("7", 1, 0, command=lambda: press("7"))
create_button("8", 1, 1, command=lambda: press("8"))
create_button("9", 1, 2, command=lambda: press("9"))
create_button("−", 1, 3, command=lambda: press("-"), bg=op_bg, fg=op_fg)

create_button("4", 2, 0, command=lambda: press("4"))
create_button("5", 2, 1, command=lambda: press("5"))
create_button("6", 2, 2, command=lambda: press("6"))
create_button("+", 2, 3, command=lambda: press("+"), bg=op_bg, fg=op_fg)

create_button("1", 3, 0, command=lambda: press("1"))
create_button("2", 3, 1, command=lambda: press("2"))
create_button("3", 3, 2, command=lambda: press("3"))
create_button("=", 3, 3, width=1, command=equalpress, bg=op_bg, fg=op_fg)

create_button("0", 4, 0, width=2, command=lambda: press("0"))
create_button(".", 4, 2, command=lambda: press("."))

root.mainloop()
