
import tkinter as tk
from pathfinding_core import find_path
import csv
from pathlib import Path

# PROJECT 01 - PHASE 5
# Obstacle-Aware Robot Pathfinding

GRID_SIZE = 7
CELL_SIZE = 60
MARGIN = 35

START = (1, 1)
GOAL = (5, 1)

# Build a vertical wall.
# The top cell (3, 6) remains open.
OBSTACLES = {(3, y) for y in range(4)}

robot_position = START
current_path = []
step_index = 0
history = []


# --------------------------------
# GRAPHICAL INTERFACE
# --------------------------------

window = tk.Tk()
window.title("Robot Pathfinding Simulator")

map_size = GRID_SIZE * CELL_SIZE + 2 * MARGIN

canvas = tk.Canvas(
    window,
    width=map_size,
    height=map_size,
    bg="white"
)

canvas.pack(padx=10, pady=10)


def to_pixels(x, y):
    px = MARGIN + (x + 0.5) * CELL_SIZE
    py = MARGIN + (GRID_SIZE - y - 0.5) * CELL_SIZE
    return px, py


# Draw grid
for i in range(GRID_SIZE + 1):

    p = MARGIN + i * CELL_SIZE

    canvas.create_line(
        p, MARGIN,
        p, map_size - MARGIN,
        fill="lightgray"
    )

    canvas.create_line(
        MARGIN, p,
        map_size - MARGIN, p,
        fill="lightgray"
    )


# Draw obstacles
for x, y in OBSTACLES:

    px, py = to_pixels(x, y)

    canvas.create_rectangle(
        px - 27, py - 27,
        px + 27, py + 27,
        fill="#64748b",
        outline=""
    )


# Draw the destination
goal_px, goal_py = to_pixels(*GOAL)

canvas.create_oval(
    goal_px - 20, goal_py - 20,
    goal_px + 20, goal_py + 20,
    fill="#16a34a",
    outline=""
)

canvas.create_text(
    goal_px, goal_py,
    text="G",
    fill="white",
    font=("Arial", 12, "bold")
)


status = tk.Label(
    window,
    text="Robot ready to find a path",
    font=("Arial", 12)
)
status.pack(pady=5)


def draw_robot():

    canvas.delete("robot")

    px, py = to_pixels(*robot_position)

    canvas.create_oval(
        px - 18, py - 18,
        px + 18, py + 18,
        fill="#2563eb",
        outline="black",
        tags="robot"
    )

    canvas.create_text(
        px, py,
        text="R",
        fill="white",
        font=("Arial", 12, "bold"),
        tags="robot"
    )


# --------------------------------
# SAVE MOVEMENT HISTORY
# --------------------------------

def save_history():

    file_path = Path(__file__).with_name(
        "pathfinding_results.csv"
    )

    with open(file_path, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["step", "x", "y"])
        writer.writerows(history)

    status.config(
        text=f"Goal reached! {step_index} moves completed."
    )

    print("Results saved to:", file_path)


# --------------------------------
# AUTOMATIC ROBOT MOVEMENT
# --------------------------------

def move_next():

    global robot_position, step_index

    if step_index >= len(current_path) - 1:
        save_history()
        start_button.config(state="normal")
        return

    old_position = robot_position

    step_index += 1
    robot_position = current_path[step_index]

    x1, y1 = to_pixels(*old_position)
    x2, y2 = to_pixels(*robot_position)

    # Draw the traveled path
    canvas.create_line(
        x1, y1, x2, y2,
        fill="#0d9488",
        width=3,
        tags="trail"
    )

    draw_robot()

    history.append([
        step_index,
        robot_position[0],
        robot_position[1]
    ])

    status.config(
        text=f"Step {step_index}: "
             f"Position {robot_position}"
    )

    window.after(500, move_next)


def start_robot():

    global current_path
    global robot_position, step_index, history

    robot_position = START
    step_index = 0
    history = [[0, START[0], START[1]]]

    canvas.delete("trail")
    draw_robot()

    # Find a path using BFS
    current_path = find_path(
    START, GOAL, OBSTACLES, GRID_SIZE
    )

    if current_path is None:

        status.config(
            text="No path found! Destination unreachable."
        )
        return

    print("Calculated path:", current_path)
    print("Total moves:", len(current_path) - 1)

    status.config(
        text="Path found! Starting movement..."
    )

    start_button.config(state="disabled")

    window.after(500, move_next)


# Start button
start_button = tk.Button(
    window,
    text="FIND PATH AND START ROBOT",
    command=start_robot,
    font=("Arial", 12)
)

start_button.pack(pady=12)

draw_robot()

window.mainloop()
