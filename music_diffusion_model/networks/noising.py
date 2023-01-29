from typing import Tuple

import torch as th
import torch.nn as nn


class Noiser(nn.Module):
    def __init__(self, steps: int, beta_1: float, beta_t: float) -> None:
        super().__init__()

        self.__steps = steps

        betas = th.linspace(beta_1, beta_t, steps=self.__steps)

        alphas = 1 - betas
        alphas_cum_prod = th.cumprod(alphas, dim=0)
        sqrt_alphas_cum_prod = th.sqrt(alphas_cum_prod)
        sqrt_minus_one_alphas_cum_prod = th.sqrt(1 - alphas_cum_prod)

        self.sqrt_alphas_cum_prod: th.Tensor
        self.sqrt_minus_one_alphas_cum_prod: th.Tensor

        self.register_buffer(
            "sqrt_alphas_cum_prod",
            sqrt_alphas_cum_prod,
        )
        self.register_buffer(
            "sqrt_minus_one_alphas_cum_prod",
            sqrt_minus_one_alphas_cum_prod,
        )

    def forward(
        self, x: th.Tensor, t: th.Tensor
    ) -> Tuple[th.Tensor, th.Tensor]:
        assert len(x.size()) == 4
        assert len(t.size()) == 2
        assert x.size(0) == t.size(0)

        b, c, w, h = x.size()
        nb_steps = t.size(1)

        device = "cuda" if next(self.buffers()).is_cuda else "cpu"

        eps = th.randn(t.size(0), t.size(1), c, w, h, device=device)

        t = t.flatten()

        sqrt_alphas_cum_prod, sqrt_minus_one_alphas_cum_prod = (
            th.index_select(
                self.sqrt_alphas_cum_prod,
                dim=0,
                index=t,
            ),
            th.index_select(
                self.sqrt_minus_one_alphas_cum_prod,
                dim=0,
                index=t,
            ),
        )

        x_t = sqrt_alphas_cum_prod.view(b, nb_steps, 1, 1, 1) * x.unsqueeze(
            1
        ) + eps * sqrt_minus_one_alphas_cum_prod.view(b, nb_steps, 1, 1, 1)

        return x_t, eps
