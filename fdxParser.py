import re
import csv
import xml.etree.ElementTree as ET

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

                scene_properties_element = element.find('SceneProperties')
                scene_properties = {
                    'length': scene_properties_element.get('Length') if scene_properties_element is not None else '',
                    'page': scene_properties_element.get('Page') if scene_properties_element is not None else '',
                }
                current_scene = {'heading': text, 'actions': [], 'dialogues': [], 'shots': [], 'scene_properties': scene_properties, 'character_arc_beats': []}
            elif paragraph_type == 'Character':
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
                    
    if current_scene:
        current_scene['characters'] = list(characters)
        scenes.append(current_scene)

    # Extract Character Arc Beats
    for scene in scenes:
        scene_properties_element = scene['scene_properties']
        character_arc_beats = []
        temp_scene_properties_element = None
        for elem in root.iter('SceneProperties'):
            title_elem = elem.find('Title')
            if title_elem is not None and title_elem.text == scene['heading']:
                temp_scene_properties_element = elem
                break
        if temp_scene_properties_element:
            for character_arc_beat in temp_scene_properties_element.findall('SceneArcBeats/CharacterArcBeat'):
                character_arc_beats.append(character_arc_beat.get('Name'))
        scene['character_arc_beats'] = character_arc_beats

    return scenes


def write_to_csv(scenes, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['heading', 'characters', 'actions', 'dialogues', 'shots', 'scene_properties_length', 'scene_properties_page', 'character_arc_beats']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for scene in scenes:
            writer.writerow({
                'heading': scene['heading'],
                'characters': ', '.join(scene['characters']),
                'actions': '\n'.join(scene['actions']),
                'dialogues': '\n'.join(scene['dialogues']),
                'shots': ', '.join(scene['shots']),
                'scene_properties_length': scene['scene_properties']['length'],
                'scene_properties_page': scene['scene_properties']['page'],
                'character_arc_beats': ', '.join(scene['character_arc_beats'])
            })


if __name__ == "__main__":
    input_file = 'input_screenplay.fdx'
    output_file = 'output.csv'

    scenes = parse_fdx(input_file)
    write_to_csv(scenes, output_file)
