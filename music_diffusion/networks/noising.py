from typing import Tuple

import torch as th
from torch import nn


class Noiser(nn.Module):
    def __init__(self, steps: int, beta_1: float, beta_t: float) -> None:
        super().__init__()

        self.__steps = steps

        betas = th.linspace(beta_1, beta_t, steps=self.__steps)

        alphas = 1 - betas
        alphas_cum_prod = th.cumprod(alphas, dim=0)
        sqrt_alphas_cum_prod = th.sqrt(alphas_cum_prod)
        sqrt_one_minus_alphas_cum_prod = th.sqrt(1 - alphas_cum_prod)

        self.sqrt_alphas_cum_prod: th.Tensor
        self.sqrt_one_minus_alphas_cum_prod: th.Tensor

        self.register_buffer(
            "sqrt_alphas_cum_prod",
            sqrt_alphas_cum_prod,
        )
        self.register_buffer(
            "sqrt_one_minus_alphas_cum_prod",
            sqrt_one_minus_alphas_cum_prod,
        )

    def forward(
        self, x_0: th.Tensor, t: th.Tensor
    ) -> Tuple[th.Tensor, th.Tensor]:
        assert len(x_0.size()) == 4
        assert len(t.size()) == 2
        assert x_0.size(0) == t.size(0)

        b, c, w, h = x_0.size()
        nb_steps = t.size(1)

        device = "cuda" if next(self.buffers()).is_cuda else "cpu"

        eps = th.randn(b, nb_steps, c, w, h, device=device)

        t = t.flatten()

        sqrt_alphas_cum_prod = self.sqrt_alphas_cum_prod[t, None, None, None]
        sqrt_alphas_cum_prod = th.unflatten(
            sqrt_alphas_cum_prod, 0, (b, nb_steps)
        )

        sqrt_one_minus_alphas_cum_prod = self.sqrt_one_minus_alphas_cum_prod[
            t, None, None, None
        ]
        sqrt_one_minus_alphas_cum_prod = th.unflatten(
            sqrt_one_minus_alphas_cum_prod, 0, (b, nb_steps)
        )

        x_t = (
            sqrt_alphas_cum_prod * x_0.unsqueeze(1)
            + eps * sqrt_one_minus_alphas_cum_prod
        )

        return x_t, eps
