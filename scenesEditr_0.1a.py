import tkinter as tk
from tkinter import ttk

def get_color_code(heading):
    if "INT." in heading and "DAY" in heading:
        return "yellow"
    elif "INT." in heading and "NIGHT" in heading:
        return "blue"
    elif "EXT." in heading and "DAY" in heading:
        return "white"
    elif "EXT." in heading and "NIGHT" in heading:
        return "green"
    else:
        return "white"

def on_scene_select(event, scenes, actions_text, dialogues_text):
    widget = event.widget
    index = widget.curselection()[0]
    selected_scene = scenes[index]
    print("Selected scene: ", selected_scene)

    actions_text.delete(1.0, tk.END)
    actions_text.insert(tk.END, "\n".join(selected_scene["actions"]))

    dialogues_text.delete(1.0, tk.END)
    dialogues_text.insert(tk.END, "\n".join(selected_scene["dialogues"]))

class MultiLineListbox(tk.Listbox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

    def insert_multiline(self, index, text, bg=None):
        lines = text.split("\n")
        for line in lines:
            self.insert(index, line)
            if bg:
                self.itemconfig(index, bg=bg)
            index += 1
        self.insert(index, "")
        index += 1
        return index

def edit_scenes(scenes):
    def on_scene_select(event, scenes):
        widget = event.widget
        index = int(widget.curselection()[0])
        selected_scene = scenes[index // (len(selected_scene) + 1)]
        print("Selected scene: ", selected_scene)

    root = tk.Tk()
    root.title("Scene Editor")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    scenes_label = ttk.Label(main_frame, text="Scenes:")
    scenes_label.grid(row=0, column=0, sticky=tk.W)

    scenes_listbox = MultiLineListbox(main_frame, height=10, width=50)
    scenes_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    index = 0
    for scene in scenes:
        text = f"Scene {index + 1}: {scene['heading']}\n"
        for key, value in scene.items():
            if key != 'heading':
                if isinstance(value, list):
                    value = "\n".join(value)
                text += f"{key}:\n{value}\n"
        index = scenes_listbox.insert_multiline(index, text, bg=get_color_code(scene['heading']))

    scenes_listbox.bind("<<ListboxSelect>>", lambda event: on_scene_select(event, scenes))

    root.mainloop()



# Example usage:
# scenes = parse_fdx(input_fdx)
# edit_scenes(scenes)
