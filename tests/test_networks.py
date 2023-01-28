from typing import Tuple

import pytest
import torch as th

from music_diffusion_model.networks import Denoiser, Noiser


@pytest.mark.parametrize("steps", [10, 20])
@pytest.mark.parametrize("step_batch_size", [1, 2])
@pytest.mark.parametrize("batch_size", [1, 2])
@pytest.mark.parametrize("channels", [1, 2])
@pytest.mark.parametrize("img_sizes", [(32, 32), (32, 64)])
def test_noiser(
    steps: int,
    step_batch_size: int,
    batch_size: int,
    channels: int,
    img_sizes: Tuple[int, int],
) -> None:
    noiser = Noiser(steps, 1e-4, 2e-1)

    x = th.randn(batch_size, channels, img_sizes[0], img_sizes[1])
    t = th.randint(0, steps, (batch_size, step_batch_size))

    x_noised, eps = noiser(x, t)

    assert len(x_noised.size()) == 5
    assert x_noised.size(0) == batch_size
    assert x_noised.size(1) == step_batch_size
    assert x_noised.size(2) == channels
    assert x_noised.size(3) == img_sizes[0]
    assert x_noised.size(4) == img_sizes[1]

    assert len(eps.size()) == 5
    assert eps.size(0) == batch_size
    assert eps.size(1) == step_batch_size
    assert eps.size(2) == channels
    assert eps.size(3) == img_sizes[0]
    assert eps.size(4) == img_sizes[1]


@pytest.mark.parametrize("steps", [10, 20])
@pytest.mark.parametrize("step_batch_size", [1, 2])
@pytest.mark.parametrize("batch_size", [1, 2])
@pytest.mark.parametrize("channels", [1, 2])
@pytest.mark.parametrize("img_sizes", [(32, 32), (32, 64)])
@pytest.mark.parametrize("time_size", [2, 3])
def test_denoiser(
    steps: int,
    step_batch_size: int,
    batch_size: int,
    channels: int,
    img_sizes: Tuple[int, int],
    time_size: int,
) -> None:
    denoiser = Denoiser(channels, steps, time_size, 1e-4, 2e-1)

    x = th.randn(
        batch_size,
        step_batch_size,
        channels,
        img_sizes[0],
        img_sizes[1],
    )
    t = th.randint(0, steps, (batch_size, step_batch_size))

    o = denoiser(x, t)

    assert len(o.size()) == 5
    assert o.size(0) == batch_size
    assert o.size(1) == step_batch_size
    assert o.size(2) == channels
    assert o.size(3) == img_sizes[0]
    assert o.size(4) == img_sizes[1]

    x = th.randn(batch_size, channels, *img_sizes)

    o = denoiser.sample(x)

    assert len(o.size()) == 4
    assert o.size(0) == batch_size
    assert o.size(1) == channels
    assert o.size(2) == img_sizes[0]
    assert o.size(3) == img_sizes[1]

    s = denoiser.loss_scale(t)

    assert len(s.size()) == 5
    assert s.size(0) == batch_size
    assert s.size(1) == step_batch_size
    assert s.size(2) == 1
    assert s.size(3) == 1
    assert s.size(4) == 1
