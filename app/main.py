from fastapi import FastAPI, UploadFile, File
from PIL import Image
import pytesseract
import numpy as np
import os
import cv2
from gtts import gTTS
from tempfile import NamedTemporaryFile
import uvicorn

app = FastAPI()

def extract_frames_from_video(video_path, output_folder):
    try:
        os.remove(output_folder)
    except OSError:
        pass

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    src_vid = cv2.VideoCapture(video_path)
    index = 0
    while src_vid.isOpened():
        ret, frame = src_vid.read()
        if not ret:
            break

        name = os.path.join(output_folder, 'frame' + str(index) + '.png')

        if index % 1 == 0:
            print('Extracting frames...' + name)
            cv2.imwrite(name, frame)
        index = index + 1

    src_vid.release()


def extract_text_from_frames(input_folder, output_file):
    try:
        os.remove(output_file)
    except OSError:
        pass
    file = open(output_file, "x")
    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        my_example = Image.open(image_path)
        text = pytesseract.image_to_string(my_example, lang='eng')
        file.write(text)

def convert_text_to_audio(input_file):
    with open(input_file, 'r') as file:
        text = file.read()

    tts = gTTS(text=text, lang='en')
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.close()
    tts.save(temp_file.name)
    return temp_file.name

@app.post("/convert")
async def convert_video_to_audio(video_file: UploadFile = File(...)):
    video_path = "uploaded_video.mp4"
    image_frames_folder = "image_frames"
    text_file = "extracted_text.txt"
    audio_output = "output.mp3"

    # Save the uploaded video file
    with open(video_path, "wb") as buffer:
        buffer.write(await video_file.read())

    # Extract frames from video
    extract_frames_from_video(video_path, image_frames_folder)

    # Extract text from frames
    extract_text_from_frames(image_frames_folder, text_file)

    # Convert text to audio
    audio_file = convert_text_to_audio(text_file)

    return {"audio_file": audio_file}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
