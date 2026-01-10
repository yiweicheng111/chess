"""# main.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import cv2
import matplotlib.pyplot as plt
z_dim = 64
image_dim = 32*32*3
batch_size = 32
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((32,32))
])
dataset = datasets.CIFAR100(
    root = "./data",
    train=True,
    download=True,
    transform=transform
)
dataloader = DataLoader(dataset,batch_size=batch_size,shuffle=True)
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(image_dim,128),
            nn.LeakyReLU(0.1),
            nn.Linear(128,1),
            nn.Sigmoid()
        )
    def forward(self,x):
        return self.fc(x)
class GAN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(z_dim,32),
            nn.ReLU(True),
            nn.Linear(32,image_dim),
            nn.Tanh()
        )
    def forward(self,x):
        return self.fc(x)
disc = Discriminator()
gen = GAN()
fixed_noise = torch.randn(batch_size,z_dim)
opt_disc = optim.Adam(disc.parameters(),lr=0.02)
opt_gen = optim.Adam(gen.parameters(),lr=0.02)
criterion = nn.BCELoss()
step = 0
for epoch in range(50):
    for batch_idx, (real, _) in enumerate(dataloader):
        print(1)"""
from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
api = FastAPI()
api.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")
@api.get("/",response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse("index.html",{
        "request":request
    })
@api.post("/g")
def getnum(data:dict):
    return (data["a"]+data["b"])