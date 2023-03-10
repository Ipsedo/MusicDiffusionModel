from typing import Literal

from torch import nn


class ChannelProjBlock(nn.Sequential):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
    ) -> None:
        super().__init__(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=(1, 1),
                stride=(1, 1),
                padding=(0, 0),
            ),
            nn.ELU(),
            nn.InstanceNorm2d(out_channels),
        )


class EndConvBlock(nn.Sequential):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
    ) -> None:
        super().__init__(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=(1, 1),
            ),
        )


class StrideConvBlock(nn.Sequential):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        scale: Literal["up", "down"],
    ) -> None:
        conv_constructor = {
            "up": nn.ConvTranspose2d,
            "down": nn.Conv2d,
        }

        super().__init__(
            conv_constructor[scale](
                in_channels,
                out_channels,
                kernel_size=(4, 4),
                stride=(2, 2),
                padding=(1, 1),
            ),
            nn.ELU(),
            nn.InstanceNorm2d(out_channels),
        )


class ConvBlock(nn.Sequential):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
    ) -> None:
        super().__init__(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=(1, 1),
            ),
            nn.ELU(),
            nn.InstanceNorm2d(out_channels),
        )
