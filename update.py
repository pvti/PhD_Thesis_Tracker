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
bar_length = 50
progress_bar = f"[{'#' * int(bar_length * (time_spent / (time_spent + time_left)))}{'-' * int(bar_length * (time_left / (time_spent + time_left)))}]"

# Read README.md
with open('README.md', 'r') as file:
    readme_lines = file.readlines()

# Update the line with the time progress
for i, line in enumerate(readme_lines):
    if line.startswith('![Time Progress]('):
        readme_lines[i] = f'![Time Progress]{progress_bar}\n'
        break

# Update README.md
with open('README.md', 'w') as file:
    file.writelines(readme_lines)
