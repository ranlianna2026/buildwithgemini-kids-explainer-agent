import os
import uuid
import asyncio
import google.auth
import google.auth.transport.requests
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.exception_handler(Exception)
async def _json_errors(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={
            "parts": [{"kind": "text", "text": f"Error: {type(exc).__name__}: {exc}"}]
        },
    )

@app.post("/upload_mom_voice")
async def upload_mom_voice(request: Request):
    form = await request.form()
    file = form.get("file")
    if file:
        os.makedirs("static", exist_ok=True)
        content = await file.read()
        save_path = "static/mom_voice_sample.webm"
        with open(save_path, "wb") as f:
            f.write(content)
        # Convert to WAV with ffmpeg if needed
        os.system(f"ffmpeg -y -i static/mom_voice_sample.webm -ar 24000 -ac 1 static/mom_voice_sample.wav")
        return JSONResponse({"status": "SUCCESS", "message": "Mom's voice saved successfully! All generated videos will now use Mom's warm vocal pitch!"})
    return JSONResponse({"status": "ERROR", "message": "No file uploaded"}, status_code=400)

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    message = body.get("message", "")
    user_id = body.get("user_id") or "web-user"
    parts: list[dict] = []

    from app.agent import generate_kids_mp4_video

    # Directly synthesize dynamic 3D MP4 video tailored for 6-year-old child!
    video_res = generate_kids_mp4_video(topic=message, child_name="Daughter", child_age=6)
    parts.append({"kind": "text", "text": video_res["html5_embed"]})

    return JSONResponse({"parts": parts})

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


