import re
import csv
import xml.etree.ElementTree as ET
from scenesEditr import edit_scenes

def parse_fdx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    scenes = []
    current_scene = None
    characters = set()

    for element in root.iter('Paragraph'):
        paragraph_type = element.get('Type')

        text_element = element.find('Text')

        if text_element is not None:
            text = text_element.text.strip() if text_element.text else ''

            if paragraph_type == 'Scene Heading':
                if current_scene:
                    current_scene['characters'] = list(characters)
                    scenes.append(current_scene)
                    characters = set()

                scene_number = element.get('Number') if element.get('Number') else ''
                current_scene = {'number': scene_number, 'heading': text, 'actions': [], 'dialogues': [], 'shots': [], 'characters': [], 'scene_properties': {}, 'raw_script': []}
            else:
                if current_scene:
                    if paragraph_type not in current_scene:
                        current_scene[paragraph_type] = []
                    current_scene[paragraph_type].append(text)

            if paragraph_type == 'Character':
                character_name = text
                characters.add(character_name)
            elif paragraph_type == 'Dialogue':
                if current_scene and characters:
                    current_scene['dialogues'].append(text)
            elif paragraph_type == 'Action':
                if current_scene:
                    current_scene['actions'].append(text)
            elif paragraph_type == 'Shot':
                if current_scene:
                    current_scene['shots'].append(text)

            # Append raw screenplay text to the current scene
            if current_scene:
                current_scene['raw_script'].append(text)
                    
    if current_scene:
        current_scene['characters'] = list(characters)
        scenes.append(current_scene)

    return scenes


def write_to_csv(scenes, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['number', 'heading', 'characters', 'actions', 'dialogues', 'shots']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for scene in scenes:
            writer.writerow({
                'number': scene['number'],
                'heading': scene['heading'],
                'characters': ', '.join(scene['characters']),
                'actions': '\n'.join(scene['actions']),
                'dialogues': '\n'.join(scene['dialogues']),
                'shots': ', '.join(scene['shots']),
            })


if __name__ == "__main__":
    input_file = 'input_screenplay.fdx'
    output_file = 'output.csv'

    scenes = parse_fdx(input_file)
    edit_scenes(scenes)
    #write_to_csv(scenes, output_file)
