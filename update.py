import datetime

# Constants
contract_start = datetime.datetime(2022, 11, 21)
contract_end = datetime.datetime(2025, 11, 20)

# Calculate time progress
today = datetime.datetime.now()
time_spent = (today - contract_start).days
time_left = (contract_end - today).days
completion = (time_spent / (time_spent + time_left)) * 100

# Draw a text-based progress bar
bar_length = 100
progress_bar = f"[{'#' * int(bar_length * (time_spent / (time_spent + time_left)))}{'-' * int(bar_length * (time_left / (time_spent + time_left)))}]"

# Format today's date
formatted_today = today.strftime("%d/%m/%Y")

# Read README.md
with open('README.md', 'r') as file:
    readme_lines = file.readlines()

# Update the line with the time progress
for i, line in enumerate(readme_lines):
    if line.startswith('- Today:'):
        readme_lines[i] = f'- Today: {formatted_today}\n'
    elif line.startswith('- Progress:'):
        readme_lines[i] = f'- Progress: {progress_bar}\n'

# Update README.md
with open('README.md', 'w') as file:
    file.writelines(readme_lines)
