import os
from PIL import Image, ImageDraw, ImageFont

def generate_kids_mp4_video(topic="How AI Works", child_name="Daughter", duration_per_scene=3):
    output_dir = "static/generated_videos"
    os.makedirs(output_dir, exist_ok=True)
    
    scenes = [
        {"title": f"Hi {child_name}! Let's learn about AI!", "bg": "#FF4757", "sub": "AI is like a super smart computer friend! 🤖"},
        {"title": "How does AI learn?", "bg": "#FFA502", "sub": "It looks at lots of dog and cat pictures! 🐶🐱"},
        {"title": "AI helps us every day!", "bg": "#2ED573", "sub": "Drawing pictures, playing games, and making music! 🎨🎮"},
        {"title": "You are the Boss of AI!", "bg": "#1E90FF", "sub": "Human creativity makes AI amazing! ✨🌟"}
    ]
    
    frame_paths = []
    for i, s in enumerate(scenes):
        img = Image.new("RGB", (1280, 720), color=s["bg"])
        draw = ImageDraw.Draw(img)
        
        # Draw playful text boxes
        draw.rectangle([100, 150, 1180, 570], fill="#FFFFFF", outline="#2F3542", width=8)
        draw.text((640, 260), s["title"], fill="#2F3542", anchor="mm", font_size=48)
        draw.text((640, 420), s["sub"], fill="#57606F", anchor="mm", font_size=36)
        
        frame_path = f"{output_dir}/frame_{i}.png"
        img.save(frame_path)
        frame_paths.append(frame_path)
        
    # Generate MP4 using ffmpeg
    mp4_path = f"{output_dir}/kids_explainer_video.mp4"
    cmd = (
        f"ffmpeg -y -loop 1 -t {duration_per_scene} -i {output_dir}/frame_0.png "
        f"-loop 1 -t {duration_per_scene} -i {output_dir}/frame_1.png "
        f"-loop 1 -t {duration_per_scene} -i {output_dir}/frame_2.png "
        f"-loop 1 -t {duration_per_scene} -i {output_dir}/frame_3.png "
        f"-filter_complex \"[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[outv]\" "
        f"-map \"[outv]\" -c:v libx264 -pix_fmt yuv420p {mp4_path}"
    )
    os.system(cmd)
    print(f"✅ Generated real MP4 video at: {mp4_path}")
    return f"/generated_videos/kids_explainer_video.mp4"

if __name__ == "__main__":
    generate_kids_mp4_video()
