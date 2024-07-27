[
import pandas as pd
import numpy as np

# Load Care Areas
care_areas_df = pd.read_csv('CareArea.csv')

# Load Metadata
metadata_df = pd.read_csv('MetaData.csv')
main_field_size = metadata_df['MainFieldSize'].iloc[0]

# Convert Care Areas to list of tuples
care_areas = [
    (row['x1'], row['y1'], row['x2'], row['y2'])
    for _, row in care_areas_df.iterrows()
]

# Function to check if a point is inside any care area
def is_inside_care_area(x, y, care_areas):
    for (x1, y1, x2, y2) in care_areas:
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
    return False

# Function to place Main Fields to cover all Care Areas
def place_main_fields(care_areas, main_field_size):
    # Extract the bounds of the care areas
    x_min = min(area[0] for area in care_areas)
    y_min = min(area[1] for area in care_areas)
    x_max = max(area[2] for area in care_areas)
    y_max = max(area[3] for area in care_areas)
    
    main_fields = []
    
    # Create a grid and mark care areas
    grid_width = int(np.ceil(x_max - x_min))
    grid_height = int(np.ceil(y_max - y_min))
    grid = np.zeros((grid_width, grid_height))
    for (x1, y1, x2, y2) in care_areas:
        grid[int(x1 - x_min):int(x2 - x_min), int(y1 - y_min):int(y2 - y_min)] = 1
    
    # Place main fields
    x = x_min
    while x <= x_max:
        y = y_min
        while y <= y_max:
            x1_grid = int(x - x_min)
            y1_grid = int(y - y_min)
            x2_grid = int(min(x + main_field_size - x_min, grid_width))
            y2_grid = int(min(y + main_field_size - y_min, grid_height))
            
            if np.sum(grid[x1_grid:x2_grid, y1_grid:y2_grid]) > 0:
                main_fields.append((x, y, x + main_field_size, y + main_field_size))
                # Clear the grid area covered by the main field to avoid double counting
                grid[x1_grid:x2_grid, y1_grid:y2_grid] = 0
            y += main_field_size
        x += main_field_size
    
    return main_fields

# Place the Main Fields
main_fields = place_main_fields(care_areas, main_field_size)

# Convert the results to a DataFrame
main_fields_df = pd.DataFrame(main_fields, columns=['x1', 'y1', 'x2', 'y2'])

# Save the results to a CSV file
main_fields_df.to_csv('MainFields.csv', index=False)

# Print the placed Main Fields
print(main_fields_df)
