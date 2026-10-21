
import tkinter as tk
import csv
from pathlib import Path

# PROJECT 01 - PHASE 4
# Autonomous Virtual Robot

GRID_SIZE = 7
CELL_SIZE = 60
MARGIN = 35

START_X = 3
START_Y = 3

robot_x = START_X
robot_y = START_Y
step_index = 0
history = []

# Planned robot movements
MOVES = [
    ("UP", 0, 1),
    ("RIGHT", 1, 0),
    ("DOWN", 0, -1),
    ("LEFT", -1, 0),
]

# Create graphical window
window = tk.Tk()
window.title("Autonomous Robot Simulator")

map_size = GRID_SIZE * CELL_SIZE + 2 * MARGIN

canvas = tk.Canvas(
    window,
    width=map_size,
    height=map_size,
    bg="white"
)
canvas.pack(padx=10, pady=10)

# Draw map grid
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

# Display robot status
status = tk.Label(
    window,
    text="Robot ready",
    font=("Arial", 13)
)
status.pack(pady=5)


# Convert grid coordinates to screen pixels
def to_pixels(x, y):
    px = MARGIN + (x + 0.5) * CELL_SIZE
    py = MARGIN + (GRID_SIZE - y - 0.5) * CELL_SIZE
    return px, py


# Draw robot at current position
def draw_robot():
    canvas.delete("robot")

    px, py = to_pixels(robot_x, robot_y)

    canvas.create_oval(
        px - 20, py - 20,
        px + 20, py + 20,
        fill="#0d9488",
        outline="black",
        tags="robot"
    )

    canvas.create_text(
        px, py,
        text="R",
        fill="white",
        font=("Arial", 14, "bold"),
        tags="robot"
    )


# Save movement history to a CSV file
def save_history():
    file_path = Path(__file__).with_name(
        "robot_path.csv"
    )

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "step", "action", "x", "y"
        ])

        writer.writerows(history)

    status.config(
        text="Mission completed! Path saved."
    )

    print("Movement saved to:", file_path)


# Execute the next planned movement
def move_next():
    global robot_x, robot_y, step_index

    # Check whether the mission is finished
    if step_index >= len(MOVES):
        save_history()
        start_button.config(state="normal")
        return

    action, dx, dy = MOVES[step_index]

    new_x = robot_x + dx
    new_y = robot_y + dy

    # Check map boundaries
    if not (
        0 <= new_x < GRID_SIZE
        and 0 <= new_y < GRID_SIZE
    ):
        status.config(text="Boundary reached!")
        start_button.config(state="normal")
        return

    # Remember the previous position
    old_x, old_y = to_pixels(robot_x, robot_y)

    # Update robot position
    robot_x = new_x
    robot_y = new_y

    # Draw traveled path
    new_px, new_py = to_pixels(robot_x, robot_y)

    canvas.create_line(
        old_x, old_y,
        new_px, new_py,
        fill="#0d9488",
        width=3,
        tags="trail"
    )

    draw_robot()

    step_index += 1

    # Remember movement
    history.append([
        step_index,
        action,
        robot_x,
        robot_y
    ])

    status.config(
        text=f"Step {step_index}: {action} "
             f"| X={robot_x}, Y={robot_y}"
    )

    # Wait 700 milliseconds before next move
    window.after(300, move_next)


# Start robot mission
def start_robot():
    global robot_x, robot_y, step_index, history

    robot_x = START_X
    robot_y = START_Y
    step_index = 0

    history = [[0, "START", robot_x, robot_y]]

    canvas.delete("trail")
    draw_robot()

    start_button.config(state="disabled")
    status.config(text="Mission started!")

    window.after(300, move_next)


# Start button
start_button = tk.Button(
    window,
    text="START AUTONOMOUS ROBOT",
    font=("Arial", 12),
    command=start_robot
)
start_button.pack(pady=12)

# Draw starting position
draw_robot()

# Run application
window.mainloop()
