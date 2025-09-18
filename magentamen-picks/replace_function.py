# Script to replace the fetch_game_results function
import re

# Read the current app.py file
with open('app.py', 'r') as f:
    content = f.read()

# Read the new function
with open('new_fetch_function.py', 'r') as f:
    new_function = f.read()

# Find the function boundaries
start_pattern = r'def fetch_game_results\(week, season\):'
end_pattern = r'def store_game_results\(week, season, game_results\):'

# Find start and end positions
start_match = re.search(start_pattern, content)
end_match = re.search(end_pattern, content)

if start_match and end_match:
    start_pos = start_match.start()
    end_pos = end_match.start()
    
    # Replace the function
    new_content = content[:start_pos] + new_function + '\n\n' + content[end_pos:]
    
    # Write the updated content
    with open('app.py', 'w') as f:
        f.write(new_content)
    
    print("Successfully replaced fetch_game_results function!")
else:
    print("Could not find function boundaries")
