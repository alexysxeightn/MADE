import random
import numpy as np
import os
import torch
from torch import nn
from torch.distributions import Normal

STATE_DIM = 22
ACTION_DIM = 6


class Agent(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(STATE_DIM, 256),
            nn.ELU(),
            nn.Linear(256, 256),
            nn.ELU(),
            nn.Linear(256, ACTION_DIM)
        )
        self.log_sigma = nn.Parameter(torch.zeros(1, 6))
        self.load_state_dict(torch.load(__file__[:-8] + "/agent.pkl"))

    def act(self, state):
        with torch.no_grad():
            state = torch.tensor(np.array(state)).float()
            action_means = self.model(state)
            p = Normal(action_means, torch.exp(self.log_sigma))
            return torch.tanh(p.sample()).squeeze(0)

    def reset(self):
        pass