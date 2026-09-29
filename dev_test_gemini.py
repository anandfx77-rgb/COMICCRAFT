import sys
import types
import json
import os
from pathlib import Path

# Create fake google.genai module before importing app modules
fake_google = types.ModuleType("google")
fake_genai = types.ModuleType("google.genai")

class FakeResponse:
    def __init__(self, text=None, candidates=None):
        self.text = text
        self.candidates = candidates

class FakeClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.models = self

    def generate_content(self, model, contents, config=None):
        # Simple heuristics to decide which response to return
        if "Create exactly five comic panels" in contents:
            panels = [
                {"panel_number": 1, "title": "Introduction", "scene_description": "A young cartographer discovers an enchanted map.", "image_generation_prompt": "A young cartographer holding a glowing map at twilight, painterly"},
                {"panel_number": 2, "title": "Discovery", "scene_description": "The map redraws itself overnight, pointing to a distant star.", "image_generation_prompt": "Close-up of a map with moving lines and tiny stars, moody lighting"},
                {"panel_number": 3, "title": "Pursuit", "scene_description": "A rival seeks the map's secret, creating tension.", "image_generation_prompt": "Shadowy rival in a candlelit study, cinematic"},
                {"panel_number": 4, "title": "Climax", "scene_description": "The map reveals a hidden doorway beneath the city.", "image_generation_prompt": "Ancient stone doorway revealed by lantern light, high detail"},
                {"panel_number": 5, "title": "Resolution", "scene_description": "A new map appears, promising another journey.", "image_generation_prompt": "Cartographer smiling as a fresh map unfurls, warm tones"},
            ]
            # Wrap with a markdown code-fence to simulate real LLM outputs
            return FakeResponse(text="```json\n" + json.dumps(panels) + "\n```")

        if "Expand the five comic panel outlines" in contents:
            # Attempt to parse the outline included in contents; fallback to simple mapping
            try:
                outline_raw = contents.split("Outline:", 1)[1].strip()
                outline_list = json.loads(outline_raw)
            except Exception:
                outline_list = []

            panels = []
            for idx, o in enumerate(outline_list, start=1):
                panels.append({
                    "panel_number": idx,
                    "title": o.get("title", f"Panel {idx}"),
                    "scene_description": o.get("scene_description", ""),
                    "narration": f"Narration for panel {idx}.",
                    "dialogue": f"\"Line {idx}\" says the main character."
                })
            return FakeResponse(text="```json\n" + json.dumps({"panels": panels}) + "\n```")

        return FakeResponse(text="{}")

# Install fake modules
fake_genai.Client = FakeClient
fake_google.genai = fake_genai
sys.modules["google"] = fake_google
sys.modules["google.genai"] = fake_genai

# Provide a fake API key for local testing
os.environ["GEMINI_API_KEY"] = "test"

# Now import the app modules and run the flow
from app import gemini_flash, gemini_pro, layout_builder

prompt = "A young cartographer finds a map that redraws itself each night."
print("=== Generating outline ===")
outline = gemini_flash.generate_outline(prompt)
print(json.dumps(outline, indent=2))

print("\n=== Generating story ===")
story = gemini_pro.generate_story(prompt, outline)
print(story)

print("\n=== Building layout ===")
# Create fake image paths (no files needed for layout building)
image_paths = [Path(f"static/panels/panel{i}.png") for i in range(1, 6)]
layout = layout_builder.build_comic_layout(image_paths, story)
print(json.dumps(layout, indent=2))

print('\nAll tests passed (local simulation).')
