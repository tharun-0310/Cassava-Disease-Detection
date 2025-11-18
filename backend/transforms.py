import cv2
import pywt
import torch
import torch.nn as nn
import numpy as np
from scipy.signal import stft
from PIL import Image


class DCTTransform:
    def __call__(self, img):
        if isinstance(img, Image.Image):
            img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        dct = cv2.dct(np.float32(img))
        dct = cv2.resize(dct, (224, 224))
        dct = np.stack([dct, dct, dct], axis=-1)
        return torch.tensor(dct.transpose(2, 0, 1), dtype=torch.float32)


class STFTTransform:
    def __call__(self, img):
        if isinstance(img, Image.Image):
            img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # STFT
        f, t, Zxx = stft(img, nperseg=64)
        magnitude = np.abs(Zxx)
        
        # Ensure 2D always
        if magnitude.ndim > 2:
            magnitude = magnitude[:, :, 0]  # take first channel if extra dims
        
        # Resize to (224,224)
        magnitude = cv2.resize(magnitude, (224, 224))
        
        # Force shape (224,224,3)
        magnitude = np.repeat(magnitude[..., np.newaxis], 3, axis=-1)
        
        # Convert to CHW tensor
        return torch.tensor(magnitude.transpose(2, 0, 1), dtype=torch.float32)


class WaveletTransform:
    def __call__(self, img):
        if isinstance(img, Image.Image):
            img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        coeffs2 = pywt.dwt2(img, 'haar')
        LL, (LH, HL, HH) = coeffs2
        wavelet_img = np.abs(LL)
        wavelet_img = cv2.resize(wavelet_img, (224, 224))
        wavelet_img = np.stack([wavelet_img, wavelet_img, wavelet_img], axis=-1)
        return torch.tensor(wavelet_img.transpose(2, 0, 1), dtype=torch.float32)


class LearnableFrequencyTransform(nn.Module):
    def __init__(self):
        super(LearnableFrequencyTransform, self).__init__()
        self.freq_filter = nn.Parameter(torch.randn(1, 224, 224))

    def forward(self, img):
        if isinstance(img, torch.Tensor):
            img = img.squeeze().numpy()
        if isinstance(img, Image.Image):
            img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.resize(img, (224, 224))
        img_tensor = torch.tensor(img, dtype=torch.float32).unsqueeze(0)
        filtered = img_tensor * self.freq_filter
        filtered = filtered.squeeze(0).detach().numpy()
        filtered = np.stack([filtered, filtered, filtered], axis=-1)
        return torch.tensor(filtered.transpose(2, 0, 1), dtype=torch.float32)


def get_transforms():
    """Get all transform instances"""
    return {
        "dct": DCTTransform(),
        "stft": STFTTransform(),
        "wavelet": WaveletTransform(),
        "learn": LearnableFrequencyTransform()
    }