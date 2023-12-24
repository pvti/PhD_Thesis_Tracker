import datetime
import json
import matplotlib.pyplot as plt
from io import BytesIO

# Constants
contract_start = datetime.datetime(2022, 11, 21)
contract_end = datetime.datetime(2025, 11, 20)

# Calculate time progress
today = datetime.datetime.now()
time_spent = (today - contract_start).days
time_left = (contract_end - today).days
completion = (time_spent / (time_spent + time_left)) * 100

# Draw time progress bar chart
fig, ax = plt.subplots(figsize=(6, 1))
ax.barh([0], [time_spent], color='blue', label='Time Spent')
ax.barh([0], [time_left], left=[time_spent], color='lightgray', label='Time Left')
ax.set_xlim(0, time_spent + time_left)
ax.set_yticks([])
ax.legend(loc='upper right')
fig.tight_layout()

# Save the plot to a BytesIO object
image_stream = BytesIO()
plt.savefig(image_stream, format='png')
plt.close()

# Convert the image stream to a base64-encoded string
image_stream.seek(0)
image_base64 = image_stream.read().encode('base64').decode('utf-8')

# Update README.md
with open('README.md', 'r') as file:
    readme_content = file.read()

readme_content = readme_content.replace('![Time Progress](badge-url-here)', f'![Time Progress](data:image/png;base64,{image_base64})')
readme_content = readme_content.replace('X days', f'{time_spent} days')
readme_content = readme_content.replace('Y days', f'{time_left} days')
readme_content = readme_content.replace('Z%', f'{completion:.2f}%')

with open('README.md', 'w') as file:
    file.write(readme_content)
