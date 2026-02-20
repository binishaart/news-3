# model.py
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

# Simple Generator network
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=9, stride=1, padding=4),
            nn.ReLU(),
            nn.Conv2d(64, 3, kernel_size=5, stride=1, padding=2),
            nn.Tanh()
        )
    def forward(self, x):
        return self.main(x)

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
generator = Generator().to(device)
generator.load_state_dict(torch.load("generator.pth", map_location=device))
generator.eval()

# Image enhancement function
def enhance_image(img_path):
    image = Image.open(img_path).convert('RGB')
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((256, 256)),  # resize if needed
    ])
    input_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output_tensor = generator(input_tensor)
    output_image = transforms.ToPILImage()(output_tensor.squeeze(0).cpu())
    output_path = "outputs/enhanced_image.png"
    output_image.save(output_path)
    return output_path
