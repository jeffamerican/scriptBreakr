import openai
import os
import re
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# Replace 'your_api_key' with your actual API key
openai.api_key = os.getenv('OPENAI_API_KEY')


def find_closest_day_night(scenes, current_index):
    # Search for the closest non-continuous day_night tag in previous scenes
    for i in range(current_index - 1, -1, -1):
        if 'day_night' not in scenes[i]:
            scenes[i]['day_night'] = None
        if scenes[i]['day_night'] not in ['CONTINUOUS', 'MOMENTS LATER']:
            return scenes[i]['day_night']
    return None


def analyze(scenes):
    int_ext_pattern = re.compile(r'(INT\.|EXT\.)')
    day_night_pattern = re.compile(r'(DAY|NIGHT|DUSK|DAWN|CONTINUOUS|MOMENTS LATER|GOLDEN HOUR|SUNSET|MAGIC HOUR)', re.IGNORECASE)
    location_pattern = re.compile(r'(INT\.|EXT\.)\s+([^-]+)')
    AI_engine = "text-davinci-003"

    prev_int_ext = None
    prev_day_night = None
    prev_location = None

    for scene in tqdm(scenes, desc="Analyzing scenes", ncols=100):
        heading = scene['heading']
        actions = ' '.join(scene['actions'])

        # Extract INT./EXT.
        int_ext_match = int_ext_pattern.search(heading)
        if int_ext_match:
            scene['int_ext'] = int_ext_match.group(0)
            prev_int_ext = int_ext_match.group(0)
        else:
            scene['int_ext'] = prev_int_ext

        # Extract DAY/NIGHT/DUSK/DAWN
        day_night_match = day_night_pattern.search(heading)
        if day_night_match:
            match = day_night_match.group(0).upper()
            if match in ['GOLDEN HOUR', 'SUNSET', 'MAGIC HOUR']:
                match = 'DUSK'
            elif match in ['CONTINUOUS', 'MOMENTS LATER']:
                closest_day_night = find_closest_day_night(scenes, scenes.index(scene))  # Use the current scene index
                if closest_day_night is not None:
                    match = closest_day_night
            scene['day_night'] = match
            prev_day_night = match
        else:
            scene['day_night'] = prev_day_night


        # Extract Location
        location_match = location_pattern.search(heading)
        if location_match:
            scene['location'] = location_match.group(2).strip()
            prev_location = location_match.group(2).strip()
        else:
            scene['location'] = prev_location

        # Extract Characters from Actions using GPT-3
        prompt = f"Please extract character names from the following actions in a screenplay scene:\n\n{actions}\n\nCharacter names:"
        
        response = openai.Completion.create(
            engine=AI_engine,
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )

        characters_from_actions = response.choices[0].text.strip().split(", ")

        # Combine characters extracted from actions with the existing character list
        scene['characters'] = list(set(scene['characters'] + characters_from_actions))

        # Normalize character names, remove (CONT'D) and make sure there are no duplicates
        scene['characters'] = list(set([re.sub(r'\([^)]*\)', '', name).strip().upper() for name in scene['characters']]))

        # Extract Stunts from Actions using GPT-3
        stunt_prompt = f"Please determine if there are any dangerous stunts in this scene and provide a short description if there are:\n\n{actions}\n\nNote that physical combat and skateboarding in traffic are to be considered stunts. \n\nStunt description (or 'None' if no stunts present):"

        stunt_response = openai.Completion.create(
            engine=AI_engine,
            prompt=stunt_prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )

        stunt_description = stunt_response.choices[0].text.strip()
        scene['stunts'] = stunt_description if stunt_description.lower() != 'none' else None


        # Extract Extras information using GPT-3
        extras_prompt = f"Please determine the number of extras needed and provide a short description for the following scene action:\n\n{actions}\n\n Note that Extras are always unnamed in scripts so if the character has a name do not include them.\nExtras needed (number and description):"

        extras_response = openai.Completion.create(
            engine=AI_engine,
            prompt=extras_prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5)

        extras_info = extras_response.choices[0].text.strip()
        scene['extras'] = extras_info
        
    return scenes
