from pathlib import Path

import pandas as pd
import torch
import torchvision as T
from hydra.utils import get_original_cwd
from omegaconf import DictConfig

class CIFAR10(torch.utils.data.Dataset):
    def __init__(self, cfg: DictConfig):
        super().__init__()
        self.cfg = cfg
        self.train = T.datasets.CIFAR10(
            root=str(Path(get_original_cwd()) / "data"),
            download=True,
            train=True,
            transform=T.transforms.ToTensor(),
        )
        self.test = T.datasets.CIFAR10(
            root=str(Path(get_original_cwd()) / "data"),
            download=True,
            train=False,
            transform=T.transforms.ToTensor(),
        )

class HotDogNotHotDog(torch.utils.data.Dataset):
    def __init__(self, cfg: DictConfig):
        super().__init__()
        self.cfg = cfg
        self.train = T.datasets.ImageFolder(
            root=self.cfg.datamodule.params.train_dir,
            transform=T.transforms.Compose(
                [
                    T.transforms.Resize((224, 224)),
                    T.transforms.ToTensor(),
                ]
            ),
        )
        self.test = T.datasets.ImageFolder(
            root=self.cfg.datamodule.params.test_dir,
            transform=T.transforms.Compose(
                [
                    T.transforms.Resize((224, 224)),
                    T.transforms.ToTensor(),
                ]
            ),
        )