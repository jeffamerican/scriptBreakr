import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from fdxParser import parse_fdx, write_to_csv
from scenesEditr import edit_scenes
from analyzr import analyze
from sceneIO import save_scenes_to_disk, load_scenes_from_disk
import time


def user_choice_dialog():
    root = tk.Tk()
    root.withdraw()

    # Customizing the dialog style
    style = {'bg': '#f0f0f0', 'fg': '#333', 'font': ('Helvetica', 12)}
    root.option_add('*Dialog.msg.font', style['font'])
    root.option_add('*Dialog.msg.foreground', style['fg'])
    root.option_add('*Dialog.msg.background', style['bg'])
    root.option_add('*Dialog.msg.wrapLength', 300)  # in pixels

    # Create a custom dialog with 'New' and 'Cont' buttons
    dialog = tk.Toplevel(root)
    dialog.title('Script Breakdown Options')
    dialog.geometry('400x200')
    dialog.configure(bg=style['bg'])

    label = tk.Label(dialog, text="Would you like to breakdown a new script? If you prefer to continue working on an existing script, please select 'Continue'.", font=style['font'], bg=style['bg'], fg=style['fg'], wraplength=300)
    label.pack(pady=10)

    user_choice = tk.StringVar()

    def new_command():
        user_choice.set('new')
        dialog.destroy()

    def cont_command():
        user_choice.set('cont')
        dialog.destroy()

    new_button = tk.Button(dialog, text='New', command=new_command, font=style['font'], bg='#4c4c4c', fg='#ffffff')
    new_button.pack(side='left', padx=50, pady=10)

    cont_button = tk.Button(dialog, text='Cont', command=cont_command, font=style['font'], bg='#4c4c4c', fg='#ffffff')
    cont_button.pack(side='right', padx=50, pady=10)

    # Wait for the user to close the dialog
    dialog.grab_set()
    dialog.wait_window()

    chosen_option = user_choice.get()
    root.destroy()

    return chosen_option





import os

def choose_file_dialog(folder, title="Choose a file"):
    root = tk.Tk()
    root.withdraw()

    
    # Get the list of files in the folder
    file_list = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    # Customizing the dialog style
    bg_color = '#f0f0f0'
    fg_color = '#333'
    font_family = 'Helvetica'
    font_size = 12
    button_bg = '#4c4c4c'
    button_fg = '#ffffff'

    # Create a listbox for file selection
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry('400x400')
    dialog.configure(bg=bg_color)

    label = tk.Label(dialog, text='Select a file:', font=(font_family, font_size), bg=bg_color, fg=fg_color)
    label.pack(pady=10)

    # Sort the file list by modification time (most recent first)
    sorted_files = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)

    listbox = tk.Listbox(dialog, width=50, height=10, font=(font_family, font_size), bg=bg_color, fg=fg_color, selectbackground=button_bg, selectforeground=button_fg)
    for file in sorted_files:
        listbox.insert(tk.END, file)

    # Set the first item as the default selected item
    listbox.selection_set(0)

    # Bind arrow keys for listbox navigation
    def up_arrow(event):
        if listbox.curselection():
            index = (listbox.curselection()[0] - 1) % listbox.size()
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(index)

    def down_arrow(event):
        if listbox.curselection():
            index = (listbox.curselection()[0] + 1) % listbox.size()
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(index)

    listbox.bind('<Up>', up_arrow)
    listbox.bind('<Down>', down_arrow)

    listbox.pack(pady=10)

    selected_file = tk.StringVar()
    def ok_command():
        if listbox.curselection():
            selected_file.set(sorted_files[listbox.curselection()[0]])
        dialog.destroy()

    ok_button = tk.Button(dialog, text='OK', command=ok_command, font=(font_family, font_size), bg=button_bg, fg=button_fg)
    ok_button.pack(pady=10)

    # Bind Enter key to the same command as the OK button
    dialog.bind('<Return>', lambda event: ok_command())

    # Bind double-click event to the same command as the OK button
    dialog.bind('<Double-1>', lambda event: ok_command())
    
    # Wait for the user to close the dialog
    dialog.grab_set()
    dialog.wait_window()

    # Retrieve the chosen file, if any
    chosen_file = selected_file.get() if selected_file.get() else None

    root.destroy()
    return chosen_file






if __name__ == '__main__':
    current_path = os.getcwd()
    
    input_folder = os.path.join(current_path, 'Put_Screenplay_Here')
    output_folder = os.path.join(current_path, 'Outputs')
    
    os.makedirs(output_folder, exist_ok=True)

    user_choice = user_choice_dialog()
    if user_choice == 'new':
        input_files = [f for f in os.listdir(input_folder) if f.endswith('.fdx')]
        if not input_files:
            print(f"No FDX files found in the folder '{input_folder}'. Please add a screenplay FDX and run the script again.")
            exit()

        chosen_fdx = choose_file_dialog(input_folder, "Choose an FDX file")
        if chosen_fdx:
            input_fdx = os.path.join(input_folder, chosen_fdx)
            print("Parsing...\n")
            raw_scenes = parse_fdx(input_fdx)
            print("Analyzing...\n")
            analyzed_scenes = analyze(raw_scenes)
            input_fdx_basename = os.path.splitext(chosen_fdx)[0]
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            output_file = os.path.join(output_folder, f"{input_fdx_basename}_{timestamp}.json")
            print("Saving...")
            save_scenes_to_disk(analyzed_scenes, output_file)
        else:
            print("Invalid selection. Please try again.")
            exit()
    else:
        # Load the scenes from the saved JSON file
        json_files = [f for f in os.listdir(output_folder) if f.endswith('.json')]
        if not json_files:
            print(f"No JSON files found in the folder '{output_folder}'. Please make sure a scenes data file exists or choose to breakdown a new script.")
            exit()

        chosen_json = choose_file_dialog(output_folder, "Choose a JSON file")

        if chosen_json:
            output_file = os.path.join(output_folder, chosen_json)
            analyzed_scenes = load_scenes_from_disk(output_file)
        else:
            print("Invalid selection. Please try again.")
            exit()
    
    edited_scenes = edit_scenes(analyzed_scenes, output_file)
