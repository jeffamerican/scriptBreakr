
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
