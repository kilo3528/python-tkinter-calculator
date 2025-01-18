import tkinter as tk
from tkinter import messagebox

# History of inputs
history = []

def button_click(symbol):
    entry.config(state="normal")  # Temporarily enable editing

    # Save history only before significant changes
    if symbol in ["=", "C", "+", "-", "*", "/"]:
        history.append(entry.get())

    if symbol == "=":
        try:
            result = eval(entry.get())  # Evaluate the expression
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))  # Display the result
        except Exception as e:
            messagebox.showerror("Error", "Invalid expression")  # Show an error message
    elif symbol == "C":
        entry.delete(0, tk.END)  # Clear the entry field
    else:
        entry.insert(tk.END, symbol)  # Add the symbol to the entry field
    entry.config(state="readonly")  # Lock editing

    # Trigger button animation
    animate_button(symbol)


# Function to handle keyboard presses
def key_press(event):
    key = event.char
    ctrl_pressed = (event.state & 0x4) != 0  # Check if Ctrl is pressed
    if ctrl_pressed and event.keysym.lower() == "z":  # Ctrl + Z for undo
        undo()
    elif key in "0123456789+-*/.":  # If it's a number or operator
        button_click(key)
    elif key == "\r":  # Enter key
        history.append(entry.get())  # Save the history after input
        button_click("=")
    elif key == "\x08":  # Backspace key
        entry.config(state="normal")
        entry.delete(len(entry.get()) - 1, tk.END)
        entry.config(state="readonly")
    elif key.lower() in ["c", "с"]:  # Latin "C" or Cyrillic "С"
        button_click("C")


def animate_button(symbol):
    button = button_dict.get(symbol)
    if button:
        # Save the original text and background color of the button
        original_fg = button.cget("fg")
        original_bg = button.cget("bg")
        
        # Temporarily change the button's colors
        button.config(bg="#bcbcbc", fg="#000000")  # Gray background and black text
        
        # Restore the colors after 100ms
        root.after(100, lambda: button.config(bg=original_colors[symbol], fg="#ffffff"))  # White text


def undo():
    if history:  # If the history is not empty
        previous_value = history.pop()  # Get the last value
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(tk.END, previous_value)
        entry.config(state="readonly")


def key_release(event):
    symbol = event.char
    button = button_dict.get(symbol)
    if button:
        # Restore the original color after releasing the key
        button.config(bg=original_colors[symbol], fg="#ffffff")  # White text


# Create the main window of the application
root = tk.Tk()
root.title("Calculator")

# Background color of the window
root.configure(bg="#1f1e1d")

# Entry field where the numbers and expressions will be displayed
entry = tk.Entry(root, font=("Arial", 24), justify="right", state="readonly", 
                 bd=10, relief="sunken", bg="#bcbcbc", fg="#000000")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Bind all keypress events to the key_press function
root.bind("<Key>", key_press)
root.bind("<KeyRelease>", key_release)

# Calculator buttons (numbers and operators)
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "C", "0", "=", "+"
]

# Dictionary to store buttons and their colors
button_dict = {}
original_colors = {}

# Colors setup
digit_color = "#1f1e1d"  # Brown for digits
operator_color = "#FF8C00"  # Orange for operators
clear_color = "#FF0000"  # Red for "C"
equal_color = "#008000"  # Green for "="

# Place buttons in the calculator window
row = 1
col = 0
for button in buttons:
    # Choose color for each button
    if button.isdigit() or button == "0":
        color = digit_color
    elif button in "+-*/":
        color = operator_color
    elif button == "C":
        color = clear_color
    elif button == "=":
        color = equal_color
    
    btn = tk.Button(
        root, text=button, font=("Arial", 18), command=lambda b=button: button_click(b),
        bg=color, fg="#ffffff", bd=1, relief="flat", activebackground="#bcbcbc"
    )
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    # Store the button and its color
    button_dict[button] = btn
    original_colors[button] = color  # Store the initial color of the button
    
    col += 1
    if col > 3:  # If the 4th column is reached, move to a new row
        col = 0
        row += 1

# Dynamically configure button sizes
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(row + 1):
    root.grid_rowconfigure(i, weight=1)

# Run the main loop of the application
root.mainloop()
