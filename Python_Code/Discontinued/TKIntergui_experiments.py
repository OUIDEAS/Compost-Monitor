import tkinter as tk

# def update_label_color():
#     if my_variable.get():
#         label.config(bg='green')  # Set label background color to green if variable is True
#     else:
#         label.config(bg='red')  # Set label background color to red if variable is False

# # Create a Tkinter window
# window = tk.Tk()
# window.title("Variable Indicator")
# window.geometry("500x500")

# # Create a Boolean variable
# my_variable = tk.BooleanVar()
# my_variable.set(False)  # Set initial value to False

# # Create a label and set its initial background color
# label = tk.Label(window, text="Variable Status", width=15, height=3)
# label.pack()
# update_label_color()

# # Create a button to toggle the variable value
# toggle_button = tk.Button(window, text="Toggle", command=lambda: my_variable.set(not my_variable.get()))
# toggle_button.pack()

# # Add a trace to the variable so that the label color is updated whenever the variable changes
# my_variable.trace('w', lambda *args: update_label_color())

# # Start the Tkinter event loop
# window.mainloop()


# import tkinter as tk

# Function to update the label color based on the variable value
# def update_label_color(index):
#     if my_variables[index].get():
#         labels[index].config(bg='green')  # Set label background color to green if variable is True
#     else:
#         labels[index].config(bg='red')  # Set label background color to red if variable is False

# # Function to toggle the variable value
# def toggle_variable(index):
#     my_variables[index].set(not my_variables[index].get())
#     update_label_color(index)

# # Create a Tkinter window
# window = tk.Tk()
# window.title("Variable Indicators")

# # Create variables and labels
# my_variables = []
# labels = []
# varLabels = ['Container']
# for i in range(16):
#     var = tk.BooleanVar()
#     var.set(False)
#     my_variables.append(var)
#     label = tk.Label(window, text=f"Variable {i+1}", width=20, height=2)
#     label.pack()
#     labels.append(label)
#     update_label_color(i)

#     # Create toggle buttons for each variable
#     toggle_button = tk.Button(window, text="Toggle", command=lambda index=i: toggle_variable(index))
#     toggle_button.pack()

# # Start the Tkinter event loop
# window.mainloop()

# import tkinter as tk

# Function to update the square color based on the variable value
# def update_square_color(section_index, square_index):
#     if my_variables[section_index][square_index].get():
#         squares[section_index][square_index].config(bg='green')  # Set square background color to green if variable is True
#     else:
#         squares[section_index][square_index].config(bg='red')  # Set square background color to red if variable is False

# # Function to toggle the variable value
# def toggle_variable(section_index, square_index):
#     my_variables[section_index][square_index].set(not my_variables[section_index][square_index].get())
#     update_square_color(section_index, square_index)

# # Create a Tkinter window
# window = tk.Tk()
# window.title("Variable Sections")

# # Create variables and squares for each section
# my_variables = []
# squares = []
# for i in range(4):
#     section_variables = []
#     section_squares = []
#     for j in range(5):
#         var = tk.BooleanVar()
#         var.set(False)
#         section_variables.append(var)
#         square = tk.Label(window, width=10, height=5)
#         square.pack(side=tk.LEFT)
#         section_squares.append(square)
#         update_square_color(i, j)
        
#         # Create toggle buttons for each square
#         toggle_button = tk.Button(window, text="Toggle", command=lambda section=i, square=j: toggle_variable(section, square))
#         toggle_button.pack(side=tk.LEFT)
        
#     my_variables.append(section_variables)
#     squares.append(section_squares)

# # Start the Tkinter event loop
# window.mainloop()


# import tkinter as tk

# # Function to update the square color based on the variable value
# def update_square_color(section_index, square_index):
#     if my_variables[section_index][square_index].get():
#         squares[section_index][square_index].config(bg='green')  # Set square background color to green if variable is True
#     else:
#         squares[section_index][square_index].config(bg='red')  # Set square background color to red if variable is False

# # Function to toggle the variable value
# def toggle_variable(section_index, square_index):
#     my_variables[section_index][square_index].set(not my_variables[section_index][square_index].get())
#     update_square_color(section_index, square_index)

# # Create a Tkinter window
# window = tk.Tk()
# window.title("Variable Sections")

# # Create variables and squares for each section
# my_variables = []
# squares = []
# for i in range(4):
#     section_variables = []
#     section_squares = []
#     for j in range(5):
#         var = tk.BooleanVar()
#         var.set(False)
#         section_variables.append(var)
#         square = tk.Label(window, width=10, height=5)
#         square.pack(side=tk.LEFT)
#         section_squares.append(square)
#     my_variables.append(section_variables)
#     squares.append(section_squares)

# # Set initial square colors
# for i in range(4):
#     for j in range(5):
#         update_square_color(i, j)

#         # Create toggle buttons for each square
#         toggle_button = tk.Button(window, text="Toggle", command=lambda section=i, square=j: toggle_variable(section, square))
#         toggle_button.pack(side=tk.LEFT)

# # Start the Tkinter event loop
# window.mainloop()

# Function to update the square color based on the variable value
# def update_square_color(section_index, square_index):
#     if my_variables[section_index][square_index].get():
#         squares[section_index][square_index].config(bg='green')  # Set square background color to green if variable is True
#     else:
#         squares[section_index][square_index].config(bg='red')  # Set square background color to red if variable is False

# # Function to toggle the variable value
# def toggle_variable(section_index, square_index):
#     my_variables[section_index][square_index].set(not my_variables[section_index][square_index].get())
#     update_square_color(section_index, square_index)

# # Create a Tkinter window
# window = tk.Tk()
# window.title("Variable Sections")

# # Create variables and squares for each section
# my_variables = []
# squares = []
# for i in range(4):
#     section_variables = []
#     section_squares = []
#     section_frame = tk.Frame(window)  # Create a frame for each section
#     section_frame.pack()

#     for j in range(5):
#         var = tk.BooleanVar()
#         var.set(False)
#         section_variables.append(var)
#         square = tk.Label(section_frame, width=10, height=5)
#         square.pack(side=tk.LEFT, padx=5, pady=5)  # Add padding between squares
#         section_squares.append(square)

#         # Create toggle buttons for each square
#         toggle_button = tk.Button(section_frame, text="Toggle", command=lambda section=i, square=j: toggle_variable(section, square))
#         toggle_button.pack(side=tk.LEFT)

#     my_variables.append(section_variables)
#     squares.append(section_squares)

#     # Update square colors after creating the section
#     for j in range(5):
#         update_square_color(i, j)

# # Start the Tkinter event loop
# window.mainloop()

# import tkinter as tk

# Function to update the square color based on the variable value
# def update_square_color(section_index, square_index):
#     if my_variables[section_index][square_index].get():
#         squares[section_index][square_index].config(bg='green')  # Set square background color to green if variable is True
#     else:
#         squares[section_index][square_index].config(bg='red')  # Set square background color to red if variable is False

# # Function to toggle the variable value
# def toggle_variable(section_index, square_index):
#     my_variables[section_index][square_index].set(not my_variables[section_index][square_index].get())
#     update_square_color(section_index, square_index)

# # Create a Tkinter window
# window = tk.Tk()
# window.title("Variable Sections")

# # Create variables and squares for each section
# my_variables = []
# squares = []
# for i in range(4):
#     section_variables = []
#     section_squares = []
#     section_frame = tk.Frame(window)  # Create a frame for each section
#     section_frame.pack()

#     for j in range(5):
#         var = tk.BooleanVar()
#         var.set(False)
#         section_variables.append(var)
#         square = tk.Label(section_frame, width=10, height=5)
#         square.grid(row=j, column=0, padx=5, pady=5)  # Use grid instead of pack
#         section_squares.append(square)

#         # Create toggle buttons for each square
#         toggle_button = tk.Button(section_frame, text="Toggle", command=lambda section=i, square=j: toggle_variable(section, square))
#         toggle_button.grid(row=j, column=1, padx=5, pady=5)  # Use grid instead of pack

#     my_variables.append(section_variables)
#     squares.append(section_squares)

#     # Update square colors after creating the section
#     for j in range(5):
#         update_square_color(i, j)

# # Start the Tkinter event loop
# window.mainloop()



# #Function to update the square color based on the variable value
# def update_square_color(section_index, square_index):
#     if my_variables[section_index][square_index].get():
#         squares[section_index][square_index].config(bg='green')  # Set square background color to green if variable is True
#     else:
#         squares[section_index][square_index].config(bg='red')  # Set square background color to red if variable is False

# # Function to toggle the variable value
# def toggle_variable(section_index, square_index):
#     my_variables[section_index][square_index].set(not my_variables[section_index][square_index].get())
#     update_square_color(section_index, square_index)

# # Create a Tkinter window
# window = tk.Tk()
# window.title("Variable Sections")

# # Create variables and squares for each section
# my_variables = []
# squares = []
# for i in range(4):
#     section_variables = []
#     section_squares = []
#     for j in range(5):
#         var = tk.BooleanVar()
#         var.set(False)
#         section_variables.append(var)
#         square = tk.Label(window, width=10, height=5)
#         square.grid(row=i, column=j, padx=5, pady=5)  # Use grid with appropriate row and column indices
#         section_squares.append(square)

#     my_variables.append(section_variables)
#     squares.append(section_squares)

#     # Update square colors after creating the section
#     for j in range(5):
#         update_square_color(i, j)

# # Start the Tkinter event loop
# window.mainloop()

# import tkinter as tk


##----------------------------------------Below is good code - just needs updated with variable labels------------------------------------##
##----------------------------------------------------------------------------------------------------------------------------------------##
# Function to update the square color based on the variable value
def update_square_color(section_index, square_index):
    if my_variables[section_index][square_index].get():
        squares[section_index][square_index].config(bg='green')  # Set square background color to green if variable is True
    else:
        squares[section_index][square_index].config(bg='red')  # Set square background color to red if variable is False

# Function to toggle the variable value
def toggle_variable(section_index, square_index):
    my_variables[section_index][square_index].set(not my_variables[section_index][square_index].get())
    update_square_color(section_index, square_index)

# Create a Tkinter window
window = tk.Tk()
window.title("Variable Sections")

# Create variables and squares for each section
my_variables = []
squares = []
variable_names = [
    ["Var1", "Var2", "Var3", "Var4", "Var5"],
    ["Var6", "Var7", "Var8", "Var9", "Var10"],
    ["Var11", "Var12", "Var13", "Var14", "Var15"],
    ["Var16", "Var17", "Var18", "Var19", "Var20"]
]

for i in range(4):
    section_variables = []
    section_squares = []
    for j in range(5):
        var = tk.BooleanVar()
        var.set(False)
        section_variables.append(var)
        square = tk.Label(window, text=variable_names[i][j], width=10, height=5)
        square.grid(row=i, column=j, padx=5, pady=5)  # Use grid with appropriate row and column indices
        section_squares.append(square)

    my_variables.append(section_variables)
    squares.append(section_squares)

    # Update square colors after creating the section
    for j in range(5):
        update_square_color(i, j)

# Start the Tkinter event loop
window.mainloop()

