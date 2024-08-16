import torch
import torch.nn as nn
import torch.nn.functional as F

class ChessModel(nn.Module):
    def __init__(self):
        super(ChessModel, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=14, out_channels=32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * 1 * 1, 128)  # Adjust based on output size from conv layers
        self.fc2 = nn.Linear(128, 1)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 128 * 1 * 1)  # Flatten the tensor, adjust size as needed
        x = F.relu(self.fc1(x))
        x = torch.tanh(self.fc2(x))  # Using Tanh activation for the output
        return x




