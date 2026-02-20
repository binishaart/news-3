import requests
import os

API_TOKEN = "YOUR_HUGGINGFACE_API_TOKEN"

def generate_room(width, length, style):
    prompt = f"A {style} style room, {width}x{length} feet, 3D realistic interior design"
    url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(url, headers=headers, json={"inputs": prompt})
    output_path = f"outputs/room_{width}x{length}_{style}.png"
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path
