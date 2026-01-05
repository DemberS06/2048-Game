# IA.py
import os
import random
from typing import List, Sequence

from IA.buffer import Buffer
from objects.board import Board
from settings import layers_size, GAMMA, LR, BATCH_SIZE, BUFFER_SIZE, EPSILON_START, EPSILON_MIN, EPSILON_DECAY, TARGET_UPDATE, NORM
import torch
import torch.nn

class IA_DQN:
    def __init__(self):
        self.layers_size = list(layers_size)
        if len(self.layers_size) < 2:
            raise ValueError("layers_size debe contener al menos input y output")
        modules = []
        for i in range(len(self.layers_size) - 1):
            n_in = self.layers_size[i]
            n_out = self.layers_size[i + 1]
            modules.append(torch.nn.Linear(n_in, n_out))
            if i < len(self.layers_size) - 2:
                modules.append(torch.nn.ReLU())
        self.model = torch.nn.Sequential(*modules)
        modules_t = []
        for i in range(len(self.layers_size) - 1):
            n_in = self.layers_size[i]
            n_out = self.layers_size[i + 1]
            modules_t.append(torch.nn.Linear(n_in, n_out))
            if i < len(self.layers_size) - 2:
                modules_t.append(torch.nn.ReLU())
        self.target_model = torch.nn.Sequential(*modules_t)
        self.target_model.load_state_dict(self.model.state_dict())
        self.device = torch.device("cpu")
        self.model.to(self.device)
        self.target_model.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=LR)
        self.Buff = []
        self.steps = 0
        self.epsilon = EPSILON_START

    def load_from_path(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No existe el archivo: {path}")
        data = torch.load(path, map_location="cpu")
        if isinstance(data, dict) and "model_state" in data:
            state = data["model_state"]
        else:
            state = data
        self.model.load_state_dict(state)
        self.target_model.load_state_dict(self.model.state_dict())
    def save_to_path(self, path: str):
        dirp = os.path.dirname(path)
        if dirp:
            os.makedirs(dirp, exist_ok=True)
        torch.save({"model_state": self.model.state_dict()}, path)

    def remember(self, item):
        self.Buff.append(item)
        if len(self.Buff) > BUFFER_SIZE:
            del self.Buff[0]

    def forward(self, inputs: Sequence[float]) -> List[float]:
        if len(inputs) != self.layers_size[0]:
            raise ValueError(f"inputs length {len(inputs)} != expected {self.layers_size[0]}")
        t = torch.tensor([list(inputs)], dtype=torch.float32, device=self.device)
        with torch.no_grad():
            out = self.model(t)
        return out.squeeze(0).tolist()

    def board_to_input(self, board) -> List[float]:
        input = []
        for v in board.board:
            for u in v:
                input.append(u/NORM)
        return input

    def query(self, board) -> int:
        if random.random() < self.epsilon:
            return random.randrange(self.layers_size[-1])
        inp = self.board_to_input(board)
        q = self.forward(inp)
        return int(max(range(len(q)), key=lambda i: q[i]))

    def train_step(self):
        if len(self.Buff) < BATCH_SIZE:
            return None
        batch = random.sample(self.Buff, BATCH_SIZE)
        states = [self.board_to_input(x.A) for x in batch]
        next_states = [self.board_to_input(x.B) for x in batch]
        actions = [int(x.mov) for x in batch]
        rewards = [float(x.R) for x in batch]
        dones = [1.0 if x.done else 0.0 for x in batch]
        state_batch = torch.tensor(states, dtype=torch.float32, device=self.device)
        next_batch = torch.tensor(next_states, dtype=torch.float32, device=self.device)
        action_batch = torch.tensor(actions, dtype=torch.long, device=self.device).unsqueeze(1)
        reward_batch = torch.tensor(rewards, dtype=torch.float32, device=self.device).unsqueeze(1)
        done_batch = torch.tensor(dones, dtype=torch.float32, device=self.device).unsqueeze(1)
        q_values = self.model(state_batch).gather(1, action_batch)
        with torch.no_grad():
            next_q = self.target_model(next_batch)
            max_next_q = next_q.max(dim=1, keepdim=True)[0]
            target = reward_batch + (1.0 - done_batch) * GAMMA * max_next_q
        loss = torch.nn.functional.mse_loss(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        self.optimizer.step()
        self.steps += 1
        if self.steps % TARGET_UPDATE == 0:
            self.target_model.load_state_dict(self.model.state_dict())
        if self.epsilon > EPSILON_MIN:
            self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)
        return float(loss.item())
