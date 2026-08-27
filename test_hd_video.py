import os
from PIL import Image, ImageDraw, ImageFont

def render_hd_video():
    output_dir = "frontend/static/generated_videos"
    os.makedirs(output_dir, exist_ok=True)
    
    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 46)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    
    scenes = [
        {"title": "Hi Daughter! Let's Learn AI! 🤖", "bg": "#FF4757", "sub": "AI is a super smart computer helper!"},
        {"title": "How Does AI Learn? 🐶🐱", "bg": "#FFA502", "sub": "It looks at thousands of dog & cat photos!"},
        {"title": "AI Helps Us Every Day! 🎨🎮", "bg": "#2ED573", "sub": "Drawing pictures, playing games & music!"},
        {"title": "You Are The Boss Of AI! ✨🌟", "bg": "#1E90FF", "sub": "Human creativity makes AI amazing!"}
    ]
    
    for i, s in enumerate(scenes):
        img = Image.new("RGB", (1280, 720), color=s["bg"])
        draw = ImageDraw.Draw(img)
        
        # White background card with shadow
        draw.rectangle([70, 110, 1210, 610], fill="#FFFFFF", outline="#2F3542", width=6)
        
        # Header banner
        draw.rectangle([70, 110, 1210, 220], fill="#2F3542")
        draw.text((640, 165), "MOM'S KIDS VIDEO EXPLAINER 🎈", fill="#FFD700", anchor="mm", font=font_bold)
        
        # Title text
        draw.text((640, 340), s["title"], fill="#2F3542", anchor="mm", font=font_bold)
        
        # Subtitle text
        draw.text((640, 480), s["sub"], fill="#57606F", anchor="mm", font=font_sub)
        
        frame_path = f"{output_dir}/frame_{i}.png"
        img.save(frame_path)

    mp4_path = f"{output_dir}/kids_explainer_5yo.mp4"
    
    # Generate MP4 with video AND audio stream
    cmd = (
        f"ffmpeg -y "
        f"-loop 1 -t 4 -i {output_dir}/frame_0.png "
        f"-loop 1 -t 4 -i {output_dir}/frame_1.png "
        f"-loop 1 -t 4 -i {output_dir}/frame_2.png "
        f"-loop 1 -t 4 -i {output_dir}/frame_3.png "
        f"-f lavfi -t 16 -i anullsrc=channel_layout=stereo:sample_rate=44100 "
        f"-filter_complex \"[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[outv]\" "
        f"-map \"[outv]\" -map 4:a -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest {mp4_path}"
    )
    os.system(cmd)
    print("✅ Successfully synthesized HD MP4 video file!")

if __name__ == "__main__":
    render_hd_video()
