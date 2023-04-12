import pdfplumber
import re

scene_heading_pattern = re.compile(r'^(INT\.|EXT\.)')
character_name_pattern = re.compile(r'^\s{20,}([A-Z]+(\s[A-Z]+)*)\s*$')

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        full_text = ''
        for page in pdf.pages:
            full_text += page.extract_text()
    return full_text


def parse_screenplay(lines):
    scenes = []
    current_scene = None
    characters = set()
    
    for line in lines:
        if scene_heading_pattern.match(line):
            if current_scene:
                current_scene['characters'] = list(characters)
                scenes.append(current_scene)
                characters = set()
                
            current_scene = {'heading': line.strip(), 'actions': [], 'dialogues': []}
        elif character_name_pattern.match(line):
            character_name = character_name_pattern.match(line).group(1)
            characters.add(character_name)
        else:
            if current_scene:
                if characters:  # If there's a character name before the current line, it's a dialogue
                    current_scene['dialogues'].append(line.strip())
                else:  # Otherwise, it's an action
                    current_scene['actions'].append(line.strip())
    
    if current_scene:
        current_scene['characters'] = list(characters)
        scenes.append(current_scene)
    
    return scenes


