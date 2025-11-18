import torch
import torch.nn as nn
from torchvision import models


class MidFusionNet(nn.Module):
    def __init__(self, num_classes=5, dropout=0.4):
        super(MidFusionNet, self).__init__()
        
        # MobileNetV2
        mobilenet = models.mobilenet_v2(weights="IMAGENET1K_V1")
        mnv2_block1 = mobilenet.features[:7]
        mnv2_block2 = mobilenet.features[7:14]
        
        # ConvNeXt-Tiny
        convnext = models.convnext_tiny(weights="IMAGENET1K_V1")
        cnx_block1 = nn.Sequential(*convnext.features[:3])
        cnx_block2 = nn.Sequential(*convnext.features[3:6])
        
        # 8 Branches (4 features × 2 backbones)
        self.branches = nn.ModuleDict({
            "mnv2_dct": nn.Sequential(mnv2_block1, mnv2_block2),
            "mnv2_stft": nn.Sequential(mnv2_block1, mnv2_block2),
            "mnv2_wave": nn.Sequential(mnv2_block1, mnv2_block2),
            "mnv2_learn": nn.Sequential(mnv2_block1, mnv2_block2),
            "cnx_dct": nn.Sequential(cnx_block1, cnx_block2),
            "cnx_stft": nn.Sequential(cnx_block1, cnx_block2),
            "cnx_wave": nn.Sequential(cnx_block1, cnx_block2),
            "cnx_learn": nn.Sequential(cnx_block1, cnx_block2),
        })
        
        # Dynamic fused_dim calculation
        with torch.no_grad():
            dummy = torch.randn(1, 3, 224, 224)
            feats = []
            feats.append(self.branches["mnv2_dct"](dummy))
            feats.append(self.branches["mnv2_stft"](dummy))
            feats.append(self.branches["mnv2_wave"](dummy))
            feats.append(self.branches["mnv2_learn"](dummy))
            feats.append(self.branches["cnx_dct"](dummy))
            feats.append(self.branches["cnx_stft"](dummy))
            feats.append(self.branches["cnx_wave"](dummy))
            feats.append(self.branches["cnx_learn"](dummy))
            fused_dim = torch.cat(feats, dim=1).shape[1]
        
        # Fusion layer
        self.fusion_encoder = nn.Sequential(
            nn.Conv2d(fused_dim, 512, kernel_size=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(dropout),
            nn.Linear(512, num_classes)
        )

    def forward(self, inputs):
        feats = []
        feats.append(self.branches["mnv2_dct"](inputs["dct"]))
        feats.append(self.branches["mnv2_stft"](inputs["stft"]))
        feats.append(self.branches["mnv2_wave"](inputs["wavelet"]))
        feats.append(self.branches["mnv2_learn"](inputs["learn"]))
        feats.append(self.branches["cnx_dct"](inputs["dct"]))
        feats.append(self.branches["cnx_stft"](inputs["stft"]))
        feats.append(self.branches["cnx_wave"](inputs["wavelet"]))
        feats.append(self.branches["cnx_learn"](inputs["learn"]))
        
        fused = torch.cat(feats, dim=1)
        fused = self.fusion_encoder(fused)
        out = self.classifier(fused)
        return out