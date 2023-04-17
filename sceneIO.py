import json

def save_scenes_to_disk(scenes, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(scenes, f, ensure_ascii=False, indent=4)


def load_scenes_from_disk(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    return scenes
