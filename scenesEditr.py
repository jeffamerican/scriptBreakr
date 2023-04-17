import tkinter as tk
from tkinter import ttk
from sceneIO import save_scenes_to_disk
#from breakdownSheet import display_breakdown




def get_color_code(int_ext, day_night):
    if int_ext == "INT." and day_night == "DAY":
        return "yellow"
    elif int_ext == "INT." and day_night == "DUSK":
        return 'yellow'
    elif int_ext == "INT." and day_night == "DAWN":
        return 'yellow'
    elif int_ext == "INT." and day_night == "NIGHT":
        return '#ADD8E6'
    elif int_ext == "EXT." and day_night == "DAY":
        return "white"
    elif int_ext == "EXT." and day_night == "DUSK":
        return "#C8E6C9"
    elif int_ext == "EXT." and day_night == "DAWN":
        return "#C8E6C9"
    elif int_ext == "EXT." and day_night == "NIGHT":
        return "green"
    else:
        return "white"



def script_report(scenes):
    report = {
        "total_scenes": len(scenes),
        "characters": set(),
        "locations": set()
    }

    for scene in scenes:
        if "characters" in scene:
            report["characters"].update(scene["characters"])
        if "location" in scene:
            report["locations"].add(scene["location"])

    # Convert sets to lists for easier handling
    report["characters"] = list(report["characters"])
    report["locations"] = list(report["locations"])

    return report

def display_script_report(report):
    report_window = tk.Toplevel()
    report_window.title("Script Report")
    report_window.lift()

    row = 0
    for key, value in report.items():
        # Display the key as a label
        label = ttk.Label(report_window, text=f"{key.replace('_', ' ').title()}:")
        label.grid(row=row, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Display the value as a label or listbox, depending on the data type
        if isinstance(value, list):
            listbox = tk.Listbox(report_window, height=min(len(value), 10), width=30)
            for item in value:
                listbox.insert(tk.END, item)
            listbox.grid(row=row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        else:
            value_label = ttk.Label(report_window, text=str(value))
            value_label.grid(row=row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        row += 1

    close_button = ttk.Button(report_window, text="Close", command=report_window.destroy)
    close_button.grid(row=row, column=1, padx=5, pady=5, sticky=(tk.E, tk.S))

def display_breakdown(entries, scene_data):
    for i, key in enumerate(scene_data.keys()):
        entry = entries.get(key, None)
        if entry:
            value = scene_data.get(key, '')
            if isinstance(value, list):
                value = '\n'.join(value)
            entry.insert(0, str(value))
        else:
            print(f"Key '{key}' not found in entries")


def on_scene_select(event, scenes, actions_text, dialogues_text):
    widget = event.widget
    index = widget.curselection()[0]
    selected_scene = scenes[index]
    print("Selected scene: ", selected_scene)

    actions_text.delete(1.0, tk.END)
    actions_text.insert(tk.END, "\n".join(selected_scene["actions"]))

    dialogues_text.delete(1.0, tk.END)
    dialogues_text.insert(tk.END, "\n".join(selected_scene["dialogues"]))
    
def edit_scenes(scenes, output_file):
    root = tk.Tk()
    root.title("Scene Editor")
    global form_window
    global entries
    global hidden_columns
    hidden_columns = []

    form_window = tk.Toplevel(root)
    form_window.title("Breakdown Sheet")

    form_frame = ttk.Frame(form_window)
    form_frame.grid(row=0, column=0, padx=5, pady=5)

    entries = {}
    for i, key in enumerate(scenes[0].keys()):
        label = ttk.Label(form_frame, text=key)
        label.grid(row=i, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        entry = ttk.Entry(form_frame, width=50)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        entries[key] = entry


    def update_breakdown(scene_data):
        for key, entry in entries.items():
            value = scene_data.get(key, '')
            if isinstance(value, list):
                value = '\n'.join(value)
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
            entry.config(state="readonly")
    
    def on_scene_select(event):
        item = treeview.selection()[0]
        selected_scene = scenes[int(item)]
        update_breakdown(selected_scene)
        #display_breakdown(entries, selected_scene)
        form_window.deiconify() # make the form window visible
        form_window.lift()
        print("Selected scene: ", selected_scene)

    def edit_cell(event):
        nonlocal entry
        if entry:
            entry.destroy()
        row_id = treeview.identify_row(event.y)
        column_id = treeview.identify_column(event.x)
        x, y, width, height = treeview.bbox(row_id, column_id)
        original_value = treeview.set(row_id, column=column_id)

        entry = tk.Entry(treeview, width=width // 10)
        entry.insert(0, original_value)
        entry.place(x=x, y=y, anchor=tk.NW, width=width)
        entry.bind('<FocusOut>', lambda event: stop_edit(row_id, column_id))
        entry.bind('<Return>', lambda event: stop_edit(row_id, column_id))
        entry.focus_set()


    def hide_column(column_id):
        global hidden_columns
        column_key = treeview["columns"][int(column_id[1:]) - 1]
        hidden_columns.append(column_key)
        treeview["columns"] = [key for key in treeview["columns"] if key != column_key]
        redraw_tree()  # Redraw the entire tree after hiding the column


    def unhide_all_columns():
        global hidden_columns
        treeview["columns"] = list(scenes[0].keys())  # Reset the columns to their original state
        hidden_columns = []  # Reset the hidden_columns list
        redraw_tree()  # Redraw the entire tree after hiding the column


    def stop_edit(row_id, column_id):
        nonlocal entry
        if entry:
            row_index = int(row_id)
            column_index = int(column_id[1:]) - 1
            key = treeview["columns"][column_index]
            value = entry.get()

            if isinstance(scenes[row_index][key], list):
                scenes[row_index][key] = value.split("\n")
            else:
                scenes[row_index][key] = value

            treeview.set(row_id, column=column_id, value=value)
            entry.destroy()
            entry = None
            report = script_report(scenes)
            display_script_report(report)
            
            # Save the updated scenes to disk
            save_scenes_to_disk(scenes, output_file)

    def redraw_tree():
        # Clear the treeview
        treeview.delete(*treeview.get_children())

        # Redraw column headers
        for key in treeview["columns"]:
            treeview.heading(key, text=key)
            treeview.column(key, anchor=tk.W)

        # Re-insert rows with the updated data
        for index, scene in enumerate(scenes):
            values = tuple(scene[key] if isinstance(scene[key], str) else "; ".join(scene[key]) if isinstance(scene[key], (list, tuple)) else str(scene[key]) for key in treeview["columns"])
            treeview.insert("", "end", iid=index, values=values, tags=(f"row{index}",))
            treeview.tag_configure(f"row{index}", background=get_color_code(scene.get('int_ext', ''), scene.get('day_night', '')))

        # Adjust column widths after redrawing the tree
        adjust_column_widths()

   
    
    def save_and_close(output_file):
        save_scenes_to_disk(scenes, output_file)
        root.destroy()

    def adjust_column_widths():
        max_cell_length = 40
        for col in treeview["columns"]:
            max_width = 0
            for scene in scenes:
                cell_value = scene[col]
                cell_width = len(str(cell_value)) * 10  # Estimate the width based on the length of the cell value
                max_width = max(max_width, cell_width)
            max_width = min(max_width, max_cell_length * 10)  # Limit the column width to 40 characters
            treeview.column(col, width=max_width)

    def delete_column(column_id):
        column_key = treeview["columns"][int(column_id[1:]) - 1]

        # Remove the column from the Treeview
        treeview["columns"] = [key for key in treeview["columns"] if key != column_key]

        # Remove the column from the scenes data structure
        for scene in scenes:
            del scene[column_key]

        # Clear the treeview
        treeview.delete(*treeview.get_children())

        # Re-insert rows with the updated data
        for index, scene in enumerate(scenes):
            values = tuple(scene[key] if isinstance(scene[key], str) else "; ".join(scene[key]) if isinstance(scene[key], (list, tuple)) else str(scene[key]) for key in scene)
            treeview.insert("", "end", iid=index, values=values, tags=(f"row{index}",))
            treeview.tag_configure(f"row{index}", background="#E1E1E1")

        # Redraw column headers
        redraw_tree()

        # Adjust column widths after deleting the column
        adjust_column_widths()

        report = script_report(scenes)
        display_script_report(report)

        # Save the updated scenes to disk
        save_scenes_to_disk(scenes, output_file)

    def on_right_click(event):
        column_id = treeview.identify_column(event.x)
        if not column_id:  # Do nothing if no column is clicked
            return

        menu = tk.Menu(treeview, tearoff=0)
        menu.add_command(label="Hide", command=lambda: hide_column(column_id))
        menu.add_command(label="Delete Column", command=lambda: delete_column(column_id))
        if hidden_columns:
            menu.add_command(label="Unhide All", command=unhide_all_columns)
        menu.post(event.x_root, event.y_root)


    # Set a theme for better appearance
    style = ttk.Style()
    style.theme_use("clam")

    main_frame = ttk.Frame(root, padding="10 10 10 0")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Configure rows and columns to expand with the window
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)

    treeview = ttk.Treeview(main_frame, columns=list(scenes[0].keys()), show="headings")
    treeview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Create vertical scrollbar and link it to the Treeview
    v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=treeview.yview)
    v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    treeview.configure(yscrollcommand=v_scrollbar.set)

    # Create horizontal scrollbar and link it to the Treeview
    h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=treeview.xview)
    h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    treeview.configure(xscrollcommand=h_scrollbar.set)

    for key in scenes[0].keys():
        treeview.heading(key, text=key)
        treeview.column(key, anchor=tk.W)

    for index, scene in enumerate(scenes):
        values = tuple(str(scene[key]) if isinstance(scene[key], str) else "; ".join(scene[key]) if isinstance(scene[key], (list, tuple)) else str(scene[key]) for key in treeview["columns"])
        treeview.insert("", "end", iid=index, values=values, tags=(f"row{index}",))
        treeview.tag_configure(f"row{index}", background=get_color_code(scene.get('int_ext', ''), scene.get('day_night', '')))

    # Customize the Treeview appearance
    style.configure("Treeview",
                    background="#D0D0D0",
                    fieldbackground="#E1E1E1",
                    foreground="black",
                    font=("Helvetica", 11),
                    rowheight=18)

    style.configure("Treeview.Heading",
                    background="#CCCCCC",
                    foreground="black",
                    font=("Helvetica", 12, "bold"))

    # Remove the Treeview border
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    treeview.bind("<<TreeviewSelect>>", on_scene_select)
    treeview.bind("<Double-1>", edit_cell)
    treeview.bind("<Button-3>", on_right_click)

    entry = None

    adjust_column_widths()

    # Set the window width to the width of the screen and center it
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = screen_width
    window_height = min(int(screen_height * 0.8), 800)  # Limit the height to 80% of the screen height or 800px, whichever is smaller
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    done_button = ttk.Button(main_frame, text="DONE", command=lambda: save_and_close(output_file))
    done_button.grid(row=1, column=0, pady=(10, 0), sticky=tk.E)

    report = script_report(scenes)
    display_script_report(report)
    root.mainloop()





# Example usage:
# scenes = parse_fdx(input_fdx)
# edit_scenes(scenes)
