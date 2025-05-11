import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to generate a new random maze
def generate_maze(size=10):
    maze = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]
    maze[0][0] = maze[size-1][size-1] = 0  # Start and goal as free cells
    return maze

# Function to display the maze
def display_maze(maze, frame):
    plt.clf()
    plt.imshow(maze, cmap="binary")
    plt.title("Maze")
    plt.axis("off")
    canvas = FigureCanvasTkAgg(plt.gcf(), master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function placeholders for algorithms
def dijkstra():
    print("Dijkstra's Algorithm selected!")

def a_star():
    print("A* Search Algorithm selected!")

def bfs():
    print("Breadth-First Search selected!")

# Main GUI application
def main():
    size = 10  # Maze size
    current_maze = generate_maze(size)

    # Tkinter root
    root = tk.Tk()
    root.title("Maze Generator & Pathfinding")

    # Frame for maze
    maze_frame = tk.Frame(root)
    maze_frame.pack()

    # Frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack()

    # Display the initial maze
    display_maze(current_maze, maze_frame)

    # Button to regenerate the maze
    def regenerate_maze():
        nonlocal current_maze
        current_maze = generate_maze(size)
        for widget in maze_frame.winfo_children():
            widget.destroy()
        display_maze(current_maze, maze_frame)

    tk.Button(button_frame, text="Generate New Maze", command=regenerate_maze).pack(side=tk.LEFT)
    tk.Button(button_frame, text="Dijkstra's Algorithm", command=dijkstra).pack(side=tk.LEFT)
    tk.Button(button_frame, text="A* Search", command=a_star).pack(side=tk.LEFT)
    tk.Button(button_frame, text="BFS Algorithm", command=bfs).pack(side=tk.LEFT)

    root.mainloop()

if __name__ == "_main_":
    main()