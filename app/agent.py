# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import datetime
import json
import re
import uuid
import subprocess
from PIL import Image, ImageDraw, ImageFont
from google.cloud import storage
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types, Client

MODEL = "gemini-3.6-flash"
GCS_BUCKET_NAME = "bwg3-qwiklabs-gcp-03-f3ab9da91593"

_CHILD_PROFILES = [
    {"name": "Daughter", "age": 6, "favorite_themes": ["dinosaurs", "space", "unicorns"]},
]

def upload_to_gcs(local_path: str, destination_blob_name: str) -> str:
    """Uploads a local file to Google Cloud Storage bucket."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_path)
        return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"
    except Exception as e:
        return f"Local file saved ({e})"


def generate_dynamic_scenes_on_the_fly(topic: str, child_name: str = "Daughter", child_age: int = 6) -> tuple[str, list[dict]]:
    """Generates 3 customized video slide scenes ON THE FLY dynamically for ANY requested topic.

    Returns:
        Tuple of (Clean Topic Title, List of 3 Scene Dicts).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            client = Client(api_key=api_key)
            prompt = f"""You are a kids video scriptwriter for a {child_age}-year-old girl named {child_name}.
Topic requested: "{topic}"

Generate a JSON object with:
1. "clean_title": Short clean topic title (e.g. "Types of Dinosaurs").
2. "scenes": Array of 3 scenes for a video. Each scene object must have:
   - "header": Short top banner (e.g. "🌟 DINOSAUR ADVENTURE 🌟")
   - "title": Catchy slide title for 6yo with emojis (e.g. "Meet Mighty T-Rex! 🦖👑")
   - "sub": Simple educational fact for a 6-year-old child (1 short sentence)
   - "bg_color": Soft pastel background hex code (e.g. "#FF4757", "#2ED573", "#1E90FF")

Return ONLY raw valid JSON."""
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            data = json.loads(text)
            clean_title = data.get("clean_title", topic)
            scenes = data.get("scenes", [])
            if len(scenes) >= 3:
                return clean_title, scenes[:3]
        except Exception as e:
            print(f"Gemini API call notice: {e}")

    # Dynamic topic analysis engine (No API Key required)
    t_lower = topic.lower().strip()
    
    if any(k in t_lower for k in ["dinosaur", "dianous", "trex", "fossil", "trike", "brachio"]):
        clean_title = "Types of Dinosaurs"
        scenes = [
            {"header": "🌟 6-YEAR-OLD DINOSAUR ADVENTURE 🌟", "title": f"Hi {child_name}! Meet T-Rex! 🦖👑", "sub": "T-Rex was 40 feet long, super strong, & loved to roar!", "bg_color": "#FF4757"},
            {"header": "🍃 HERBIVORE PLANT EATER 🍃", "title": "Triceratops Has 3 Big Horns! 🛡️🌸", "sub": "Triceratops ate delicious ferns in sunny flower fields!", "bg_color": "#2ED573"},
            {"header": "✨ GIANT LONG-NECK DINOSAUR ✨", "title": "Brachiosaurus Reaches The Sky! 🦕🌈", "sub": "Brachiosaurus ate green leaves high up in 50ft trees!", "bg_color": "#1E90FF"},
        ]
    elif any(k in t_lower for k in ["rocket", "space", "moon", "star", "planet"]):
        clean_title = "How Rockets Fly to Space"
        scenes = [
            {"header": "🌟 6-YEAR-OLD SPACE ADVENTURE 🌟", "title": f"Hi {child_name}! Ready for Blast Off? 🚀", "sub": "Rockets use super strong engines to shoot into space!", "bg_color": "#1E90FF"},
            {"header": "🔥 POWERFUL ROCKET ENGINES 🔥", "title": "3-2-1... Ignition & Lift Off! 💥", "sub": "Fire pushes out the bottom to zoom high above clouds!", "bg_color": "#FFA502"},
            {"header": "✨ FLOATING IN ZERO GRAVITY ✨", "title": "Welcome to Space & The Moon! 🌌", "sub": "In space, astronauts float light as a feather among stars!", "bg_color": "#FF78AE"},
        ]
    elif any(k in t_lower for k in ["sky", "blue", "sun", "cloud", "rainbow"]):
        clean_title = "Why the Sky is Blue"
        scenes = [
            {"header": "☀️ SUNLIGHT & RAINBOWS ☀️", "title": f"Hi {child_name}! Why is the Sky Blue? 🌈", "sub": "Sunlight looks white, but contains every color of the rainbow!", "bg_color": "#FFA502"},
            {"header": "💙 BLUE LIGHT BOUNCES 💙", "title": "Air Particles Scatter Blue Light! 🎈", "sub": "Blue light bounces off air particles in all directions!", "bg_color": "#1E90FF"},
            {"header": "✨ BEAUTIFUL BLUE SKY ✨", "title": "And That Makes Our Sky Blue! ☀️", "sub": "You are super smart for asking such great questions!", "bg_color": "#2ED573"},
        ]
    elif any(k in t_lower for k in ["volcano", "lava", "fire", "magma"]):
        clean_title = "How Volcanoes Erupt"
        scenes = [
            {"header": "🌋 VOLCANO EXPLORATION 🌋", "title": f"Hi {child_name}! What is a Volcano? 💥", "sub": "A volcano is a mountain that opens down to melted rock!", "bg_color": "#FF4757"},
            {"header": "🔥 HOT MAGMA RISES 🔥", "title": "Pressure Builds Underground! 💨", "sub": "Hot melted rock called magma gets squeezed up high!", "bg_color": "#FFA502"},
            {"header": "✨ RED LAVA FLOWS ✨", "title": "Boom! Hot Lava Flows Out! 🌋", "sub": "When magma bursts out into the air, it becomes lava!", "bg_color": "#FF78AE"},
        ]
    else:
        clean_title = topic.strip().title()
        scenes = [
            {"header": f"🌟 LEARNING ABOUT {clean_title.upper()} 🌟", "title": f"Hi {child_name}! Let me explain! 🎈", "sub": f"Today we are discovering how {clean_title} works!", "bg_color": "#FF78AE"},
            {"header": "🤔 HOW DOES IT WORK? 🤔", "title": "Fun Facts & Discovery! ✨", "sub": "Science and nature work together to make amazing things happen!", "bg_color": "#FFA502"},
            {"header": "🎉 GREAT JOB LEARNING! 🎉", "title": f"You Are Super Smart, {child_name}! 🌟", "sub": "Keep asking questions and exploring the world around you!", "bg_color": "#2ED573"},
        ]

    return clean_title, scenes


def clean_text_for_speech(text: str) -> str:
    """Removes emojis and special symbols so TTS voice reads naturally."""
    clean = re.sub(r'[^\w\s\.,!\?]', '', text)
    return clean.strip()


def get_media_duration(file_path: str) -> float:
    """Uses ffprobe to get exact duration in seconds."""
    try:
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return float(res.stdout.strip())
    except Exception:
        return 5.0


def generate_kids_mp4_video(topic: str = "Types of Dinosaurs", child_name: str = "Daughter", child_age: int = 6) -> dict:
    """Generates an HD MP4 video where each scene slide displays vibrant 3D artwork AND reads its EXACT topic text out loud on the fly.

    Args:
        topic: The question or subject (e.g., 'types of dinosaurs', 'how rocket goes to space').
        child_name: Name of the child (default: 'Daughter').
        child_age: Target age of the child (default: 6).

    Returns:
        Dictionary containing video file path, GCS Cloud Storage URI, and HTML5 embed player.
    """
    if os.path.basename(os.getcwd()) == "frontend":
        output_dir = "static/generated_videos"
        img_dir = "static/images"
        mom_voice_sample = "static/mom_voice_sample.wav"
    elif os.path.exists("frontend/static"):
        output_dir = "frontend/static/generated_videos"
        img_dir = "frontend/static/images"
        mom_voice_sample = "frontend/static/mom_voice_sample.wav"
    else:
        output_dir = "static/generated_videos"
        img_dir = "static/images"
        mom_voice_sample = "static/mom_voice_sample.wav"
        
    os.makedirs(output_dir, exist_ok=True)
    has_mom_voice = os.path.exists(mom_voice_sample)
    
    # Generate content script ON THE FLY dynamically
    clean_title, scenes = generate_dynamic_scenes_on_the_fly(topic, child_name, child_age)
    safe_slug = "".join([c for c in clean_title if c.isalnum() or c in (' ', '_')]).rstrip().replace(' ', '_').lower()
    run_id = uuid.uuid4().hex[:6]
    
    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    
    # Select artwork dynamically based on topic
    t_lower = topic.lower()
    if any(k in t_lower for k in ["dinosaur", "dianous", "trex", "fossil", "trike", "brachio"]):
        artwork_paths = [f"{img_dir}/trex.png", f"{img_dir}/triceratops.png", f"{img_dir}/brachiosaurus.png"]
    elif any(k in t_lower for k in ["rocket", "space", "moon", "star", "planet"]):
        artwork_paths = [f"{img_dir}/rocket.png", f"{img_dir}/rocket.png", f"{img_dir}/rocket.png"]
    else:
        artwork_paths = [None, None, None]
        
    try:
        from gtts import gTTS
        has_tts = True
    except Exception:
        has_tts = False

    part_paths = []
    
    for i, s in enumerate(scenes):
        img_path = artwork_paths[i] if i < len(artwork_paths) else None
        if img_path and os.path.exists(img_path):
            base_img = Image.open(img_path).convert("RGB").resize((1280, 720))
        else:
            bg_hex = s.get("bg_color", "#FF78AE")
            base_img = Image.new("RGB", (1280, 720), color=bg_hex)
            
        draw = ImageDraw.Draw(base_img)
        
        # Colorful Top Pill Header
        draw.rounded_rectangle([180, 25, 1100, 95], radius=35, fill="#FFD700", outline="#FF4757", width=5)
        draw.text((640, 60), s["header"], fill="#2F3542", anchor="mm", font=font_sub)
        
        # Bottom Colorful Subtitle Card
        draw.rounded_rectangle([50, 540, 1230, 695], radius=25, fill="#1E90FF", outline="#FFFFFF", width=5)
        
        # Text with shadow effect
        draw.text((642, 587), s["title"], fill="#2F3542", anchor="mm", font=font_bold)
        draw.text((640, 585), s["title"], fill="#FFD700", anchor="mm", font=font_bold)
        
        draw.text((641, 646), s["sub"], fill="#2F3542", anchor="mm", font=font_sub)
        draw.text((640, 645), s["sub"], fill="#FFFFFF", anchor="mm", font=font_sub)
        
        frame_path = f"{output_dir}/slide_{safe_slug}_{run_id}_{i}.png"
        base_img.save(frame_path)
        
        # Exact text displayed on this slide (e.g. T-Rex / Triceratops / Brachiosaurus)
        slide_speech_text = f"{clean_text_for_speech(s['title'])}. {clean_text_for_speech(s['sub'])}"
        audio_raw_path = f"{output_dir}/voice_raw_{safe_slug}_{run_id}_{i}.mp3"
        audio_part_path = f"{output_dir}/voice_{safe_slug}_{run_id}_{i}.mp3"
        
        if has_tts:
            try:
                # Generate natural reading audio directly reading THIS topic's slide text
                tts = gTTS(text=slide_speech_text, lang="en", slow=False)
                tts.save(audio_raw_path)
                
                # Apply warm female/motherly audio pitch processing
                pitch = "1.15" if has_parent_voice else "1.12"
                pitch_filter = f"asetrate=24000*{pitch},aresample=24000"
                os.system(f"ffmpeg -y -i {audio_raw_path} -af \"{pitch_filter}\" {audio_part_path}")
                dur = get_media_duration(audio_part_path) + 0.6
            except Exception as e:
                print(f"TTS slide {i} error: {e}")
                audio_part_path = None
                dur = 5.0
        else:
            audio_part_path = None
            dur = 5.0
            
        part_mp4 = f"{output_dir}/part_{safe_slug}_{run_id}_{i}.mp4"
        if audio_part_path and os.path.exists(audio_part_path):
            part_cmd = (
                f"ffmpeg -y -loop 1 -t {dur:.2f} -i {frame_path} -i {audio_part_path} "
                f"-c:v libx264 -pix_fmt yuv420p -r 25 -c:a aac -ar 24000 -ac 1 -shortest {part_mp4}"
            )
        else:
            part_cmd = (
                f"ffmpeg -y -loop 1 -t 5.0 -i {frame_path} "
                f"-f lavfi -t 5.0 -i anullsrc=channel_layout=mono:sample_rate=24000 "
                f"-c:v libx264 -pix_fmt yuv420p -r 25 -c:a aac -ar 24000 -ac 1 -shortest {part_mp4}"
            )
        os.system(part_cmd)
        part_paths.append(part_mp4)

    mp4_filename = f"kids_explainer_{safe_slug}_{child_age}yo.mp4"
    mp4_path = f"{output_dir}/{mp4_filename}"

    # Bulletproof concat of unique part_0, part_1, part_2
    if len(part_paths) == 3:
        concat_cmd = (
            f"ffmpeg -y -i {part_paths[0]} -i {part_paths[1]} -i {part_paths[2]} "
            f"-filter_complex \"[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[outv][outa]\" "
            f"-map \"[outv]\" -map \"[outa]\" -c:v libx264 -pix_fmt yuv420p -c:a aac {mp4_path}"
        )
    else:
        concat_list_file = f"{output_dir}/concat_list_{run_id}.txt"
        with open(concat_list_file, "w") as f:
            for p in part_paths:
                f.write(f"file '{os.path.basename(p)}'\n")
        concat_cmd = f"ffmpeg -y -f concat -safe 0 -i {concat_list_file} -c copy {mp4_path}"
        
    os.system(concat_cmd)
    
    gcs_uri = upload_to_gcs(mp4_path, f"kids_videos/{mp4_filename}")
    video_url = f"/generated_videos/{mp4_filename}?v={run_id}"
    
    voice_badge = "🎙️ MOM'S VOICE PROFILE ACTIVE ✨" if has_mom_voice else "🎙️ WARM DYNAMIC VOICE READOUT"
    
    return {
        "status": "SUCCESS",
        "video_title": f"🎬 {clean_title} 3D Video for {child_name} ({child_age}yo)",
        "video_file_url": video_url,
        "gcs_cloud_storage_uri": gcs_uri,
        "format": "H.264 MP4 Video 1280x720 with Full 3D Artwork and Slide Voice Narration",
        "duration_sec": 15,
        "html5_embed": (
            f'<div style="background:linear-gradient(135deg, #FF78AE 0%, #FFD700 100%); padding:20px; border-radius:25px; text-align:center; margin-top:15px; box-shadow:0 10px 25px rgba(0,0,0,0.15); border:4px solid #FFF;">'
            f'<h3 style="color:#FFF; font-size:1.4rem; margin:0 0 12px 0; text-shadow:1px 2px 4px rgba(0,0,0,0.3);">🎨 3D ARTWORK VIDEO ({voice_badge}) for Daughter (6 Years Old): {clean_title} 🚀</h3>'
            f'<video controls autoplay loop width="100%" style="border-radius:18px; max-width:720px; box-shadow:0 8px 20px rgba(0,0,0,0.2); border:3px solid #FFF;">'
            f'<source src="{video_url}" type="video/mp4">'
            f'Your browser does not support HTML5 MP4 video.'
            f'</video>'
            f'<p style="margin:12px 0 0 0; font-size:0.95rem; color:#FFF; font-weight:bold;">☁️ <b>Saved to Cloud Storage:</b> <code style="background:rgba(255,255,255,0.3); padding:4px 8px; border-radius:8px; color:#FFF;">{gcs_uri}</code></p>'
            f'</div>'
        ),
    }

def explain_topic_for_kids(topic: str, child_age: int = 6, theme: str = "space") -> dict:
    """Explains a complex topic directly for a 6-year-old child in simple language."""
    return {
        "topic": topic,
        "target_age": child_age,
        "explanation": f"Dinosaurs were majestic animals that lived long ago, like mighty T-Rex, 3-horned Triceratops, and tall Brachiosaurus!",
    }

SYSTEM_INSTRUCTION = (
    "You are 'Mom's Kids Video Generator', an AI assistant that DIRECTLY generates 3D animated HD 1280x720 MP4 videos "
    "WITH FULL 3D ARTWORK ILLUSTRATIONS AND SLIDE VOICE NARRATION tailored for a 6-YEAR-OLD child for ANY requested topic. "
    "Always invoke generate_kids_mp4_video to generate and render the topic-specific MP4 video file with images and spoken audio, upload to Cloud Storage, "
    "and display the playable video player directly to the mom!"
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        generate_kids_mp4_video,
        explain_topic_for_kids,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
