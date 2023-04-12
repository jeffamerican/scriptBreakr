import os
#import csv
#from dotenv import load_dotenv
from fdxParser import parse_fdx, write_to_csv
import time

# Main script
if __name__ == '__main__':
    # Get the current working directory
    current_path = os.getcwd()
    
    input_folder = os.path.join(current_path, 'Put_Screenplay_Here')
    output_folder = os.path.join(current_path, 'Outputs')
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get the input screenplay file
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.fdx')]
    if not input_files:
        print(f"No FDX files found in the folder '{input_folder}'. Please add a screenplay FDX and run the script again.")
        exit()
    input_fdx = os.path.join(input_folder, input_files[0])

    # Set the output file name with timestamp
    input_fdx_basename = os.path.splitext(input_files[0])[0]
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_csv = os.path.join(output_folder, f"{input_fdx_basename}_{timestamp}.csv")

    scenes = parse_fdx(input_fdx)
    write_to_csv(scenes, output_csv)
    print(f"Scene breakdown saved to {output_csv}")
