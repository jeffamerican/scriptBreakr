import tkinter as tk
from tkinter import ttk

def display_breakdown(entries, scene_data):
    for i, key in enumerate(scene_data.keys()):
        entry = entries[key]
        value = scene_data.get(key, '')
        if isinstance(value, list):
            value = '\n'.join(value)
        entry.insert(0, str(value))
        
 #   form_window = tk.Toplevel(root)
 #   form_window.title("Breakdown Sheet")
 #   form_window.withdraw() # Hide the window initially

#    form_frame = ttk.Frame(form_window)
 #   form_frame.grid(row=0, column=0, padx=5, pady=5)

    

    #form_window.mainloop()

# Example usage:
#selected_scene = {
#    'heading': 'INT. ROOM - DAY',
#    'actions': ['Action 1', 'Action 2'],
#    'dialogues': ['Dialogue 1', 'Dialogue 2']
#}
#display_breakdown(selected_scene)
