
import tkinter as tk

# PROJECT 01 - 2D Virtual Robot Simulator

# ----- Map settings -----
GRID_SIZE = 7
CELL_SIZE = 60
MARGIN = 35

# Starting robot position
robot_x = 3
robot_y = 3

# Create application window
window = tk.Tk()
window.title("My First 2D Robot Simulator")

# Create the robot's map
map_size = GRID_SIZE * CELL_SIZE + 2 * MARGIN

canvas = tk.Canvas(
    window,
    width=map_size,
    height=map_size,
    bg="white"
)
canvas.pack(padx=10, pady=10)

# Draw grid lines
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

# Draw coordinate labels
for i in range(GRID_SIZE):
    canvas.create_text(
        MARGIN + (i + 0.5) * CELL_SIZE,
        map_size - 15,
        text=str(i)
    )

    canvas.create_text(
        17,
        MARGIN + (GRID_SIZE - i - 0.5) * CELL_SIZE,
        text=str(i)
    )

# Position display
status = tk.Label(window, font=("Arial", 14))
status.pack(pady=5)


# Draw our virtual robot
def draw_robot():
    canvas.delete("robot")

    # Convert robot coordinates to screen pixels
    px = MARGIN + (robot_x + 0.5) * CELL_SIZE
    py = MARGIN + (GRID_SIZE - robot_y - 0.5) * CELL_SIZE

    radius = 20

    canvas.create_oval(
        px - radius, py - radius,
        px + radius, py + radius,
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

    status.config(
        text=f"Robot Position: X={robot_x}, Y={robot_y}"
    )


# Function to move the robot
def move_robot(dx, dy):
    global robot_x, robot_y

    new_x = robot_x + dx
    new_y = robot_y + dy

    # Prevent movement outside the map
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        robot_x = new_x
        robot_y = new_y
        draw_robot()
    else:
        status.config(text="Map boundary reached!")


# Control buttons
controls = tk.Frame(window)
controls.pack(pady=10)

tk.Button(
    controls, text="UP",
    command=lambda: move_robot(0, 1)
).grid(row=0, column=1)

tk.Button(
    controls, text="LEFT",
    command=lambda: move_robot(-1, 0)
).grid(row=1, column=0)

tk.Button(
    controls, text="DOWN",
    command=lambda: move_robot(0, -1)
).grid(row=1, column=1)

tk.Button(
    controls, text="RIGHT",
    command=lambda: move_robot(1, 0)
).grid(row=1, column=2)

# Keyboard arrow controls
window.bind("<Up>", lambda e: move_robot(0, 1))
window.bind("<Down>", lambda e: move_robot(0, -1))
window.bind("<Left>", lambda e: move_robot(-1, 0))
window.bind("<Right>", lambda e: move_robot(1, 0))

# Show robot at initial position
draw_robot()

# Keep application running
window.mainloop()
