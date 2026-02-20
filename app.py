from flask import Flask, render_template, request
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import os

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        article = request.form.get("article")
        if not article:
            return "Please enter a news article"

        # 1️⃣ Voice-over
        tts = gTTS(article, lang="en")
        audio_path = os.path.join("outputs", "news_audio.mp3")
        tts.save(audio_path)

        # 2️⃣ Handle uploaded images
        uploaded_files = request.files.getlist("images")
        clips = []
        for file in uploaded_files:
            if file.filename:
                path = os.path.join("uploads", file.filename)
                file.save(path)
                clip = ImageClip(path).set_duration(3)  # 3 sec per image
                clips.append(clip)

        if not clips:
            return "No images uploaded"

        video = concatenate_videoclips(clips)

        # 3️⃣ Add audio
        audio_clip = AudioFileClip(audio_path)
        video = video.set_audio(audio_clip)

        # 4️⃣ Add subtitles (simplified: first 100 chars)
        txt_clip = TextClip(article[:100]+"...", fontsize=24, color="white", bg_color="black",
                            method="caption", size=(video.w, 50))
        txt_clip = txt_clip.set_position(("center","bottom")).set_duration(video.duration)
        final = CompositeVideoClip([video, txt_clip])

        output_path = os.path.join("outputs", "news_video.mp4")
        final.write_videofile(output_path, fps=24)

        return render_template("index.html", output_video=output_path)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


