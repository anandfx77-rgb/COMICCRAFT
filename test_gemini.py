import os
os.environ['GEMINI_API_KEY'] = 'AIzaSyBHG_5LNrgwX_dSh6X2Z86HxS5Dw9HlbLg'
from google import genai

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

prompt = """Create exactly five comic panels from this story prompt. Return a JSON array only, with one object per panel and these fields: "panel_number" (1 through 5), "title", "scene_description", and "image_generation_prompt". Make titles concise, scenes coherent, and image prompts visually specific.

Story prompt: test"""

try:
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt,
        config={'response_mime_type': 'application/json'}
    )
    print('Success!')
    print(response.text[:200])
except Exception as e:
    print('Error:', type(e).__name__)
    print(str(e)[:300])