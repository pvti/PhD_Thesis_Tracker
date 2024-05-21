import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
import numpy as np
import random

# Set a font that supports the required Unicode characters (emojis)
plt.rcParams["font.family"] = "DejaVu Sans"

# Constants
CONTRACT_START = datetime.datetime(2022, 11, 21)
CONTRACT_END = datetime.datetime(2025, 11, 20)
mouse_size = 0.0

# Function to calculate time progress
def calculate_time_progress():
    today = datetime.datetime.now()
    time_spent = (today - CONTRACT_START).days + 1
    time_left = (CONTRACT_END - today).days + 1
    completion = (time_spent / (time_spent + time_left)) * 100
    return time_spent, time_left, completion

def generate_progress_badge(completion):
    # Get color from the RdYlGn colormap
    progress = completion / 100
    colors = plt.cm.RdYlGn(progress)

    # Generate Markdown text for the badge
    badge_text = f'![Progress](https://img.shields.io/badge/Progress-{completion:.2f}%25-{mcolors.to_hex(colors)[1:]}?style=flat-square)'

    return badge_text

# Function to draw a text-based progress bar
def draw_progress_bar(bar_length, completion):
    filled_length = int(bar_length * (completion / 100))
    bar = f"[{'+' * filled_length}{'-' * (bar_length - filled_length)}]"
    return bar

# Function to update README.md with time progress
def update_readme(progress_bar, formatted_today, time_spent, time_left, completion):
    progress_badge = generate_progress_badge(completion)

    with open('README.md', 'r') as file:
        readme_lines = file.readlines()

    for i, line in enumerate(readme_lines):
        if line.startswith('![Progress]'):
            readme_lines[i] = f'{progress_badge}\n'
        elif line.startswith('- Today:'):
            readme_lines[i] = f'- Today: {formatted_today}\n'
        elif line.startswith('- Time Spent:'):
            readme_lines[i] = f'- Time Spent: {time_spent} days\n'
        elif line.startswith('- Time Left:'):
            readme_lines[i] = f'- Time Left: {time_left} days\n'
        elif line.startswith('- Completion:'):
            # Round completion to 2 decimal places, add %, and make it bold
            formatted_completion = f'<b>{completion:.2f}%</b>'
            readme_lines[i] = f'- Completion: {formatted_completion}\n'
        elif line.startswith('- Progress:'):
            readme_lines[i] = f'- Progress: {progress_bar}\n'

    with open('README.md', 'w') as file:
        file.writelines(readme_lines)

# Function to update time progress and draw progress bar
def update_and_draw_progress():
    time_spent, time_left, completion = calculate_time_progress()
    progress_bar = draw_progress_bar(bar_length=100, completion=completion)
    formatted_today = datetime.datetime.now().strftime("%d/%m/%Y")
    update_readme(progress_bar, formatted_today, time_spent, time_left, completion)
    animate_progress_with_items(spent_time=time_spent, left_time=time_left, total_frames=100)

# Function to eat an item
def eat_item(item, mouse_marker):
    global mouse_size
    mouse_size += 0.1  # Increase the size of the mouse when it eats an item
    mouse_marker.set_fontsize(12 + mouse_size * 10)
    item.set_visible(False)

# Function to update animation frame
def update_animation(frame, total_frames, bar, mouse_marker, items, spent_time_percentage, title_text):
    progress = frame / total_frames * spent_time_percentage
    colors = plt.cm.RdYlGn(progress)

    # Update the progress bar data
    bar[0].set_width(progress)
    bar[0].set_facecolor(colors)

    # Update the title
    exact_percentage = round(progress * 100, 2)
    title_text.set_text(f"Progress: {exact_percentage}%")

    # Update the mouse marker position
    mouse_marker.set_x(progress)

    # Check for collision with items
    for item, x_pos in items:
        if abs(progress - x_pos) < 0.02:  # Adjust the collision threshold as needed
            eat_item(item, mouse_marker)

# Function to animate progress with items
def animate_progress_with_items(spent_time, left_time, total_frames=100):
    global mouse_size

    fig, ax = plt.subplots()

    # Create an initial progress bar
    bar = ax.barh(0, 0, color='green', edgecolor='black', linewidth=1, height=1.0)

    # Create an initial mouse marker
    # mouse_marker = ax.text(0, 0, '🐭', fontsize=12, va='center', ha='right')
    status = random.choice(['😉', '😳', '😅', '😎', '😂', '😊', '😖', '😥', '😂', '😋', '😃', '😚', '😉', '😝', '😦', '😕', '😒', '😔', '😞', '😇'])
    mouse_marker = ax.text(0, 0, status, fontsize=12, va='center', ha='right')

    # Set the x-axis limits
    ax.set_xlim(0, 1)

    # Remove y-axis ticks and labels
    ax.set_yticks([])
    ax.set_yticklabels([])

    # Set the title
    title_text = ax.text(0.5, 1.05, "Progress: 0.00%", transform=ax.transAxes, ha='center')

    # Create random items (fruits and fromage) along the progress bar
    item_positions = np.sort(np.random.rand(20))
    item_y_positions = (np.random.rand(20) - 0.5) * 2  # Randomize y-positions between -0.5 and 0.5
    items = []
    for x_pos, y_pos in zip(item_positions, item_y_positions):
        # item_type = random.choice(['🍎', '🍌', '🍇', '🧀'])  # Fruits and fromage
        item_type = random.choice(['😉', '😳', '😅', '😎', '😂', '😊', '😖', '😥', '😂', '😋', '😃', '😚', '😉', '😝', '😦', '😕', '😒', '😔', '😞', '😇'])  # Fruits and fromage
        item = ax.text(x_pos, y_pos, item_type, fontsize=12, va='center', ha='center')
        items.append((item, x_pos))

    # Create the animation
    animation = FuncAnimation(fig, update_animation, fargs=(total_frames, bar, mouse_marker, items, spent_time / (spent_time + left_time), title_text),
                              frames=range(total_frames), interval=50)

    # Save the animation to a GIF file
    animation.save("progress.gif", writer='pillow', fps=20)

update_and_draw_progress()
