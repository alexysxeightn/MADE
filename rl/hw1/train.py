from gym import make
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.optim import Adam, lr_scheduler
from collections import deque
import random
import copy

GAMMA = 0.99
INITIAL_STEPS = 1024
TRANSITIONS = 2_000_000
STEPS_PER_UPDATE = 4
STEPS_PER_TARGET_UPDATE = STEPS_PER_UPDATE * 1000
BATCH_SIZE = 128
LEARNING_RATE = 5e-4
RANDOM_SEED = 42
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
BUFFER_SIZE = 150_000


class QModel(nn.Module):
    def __init__(self, state_dim, action_dim, fc1=512, fc2=512, p=0.2):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, fc1),
            nn.BatchNorm1d(fc1),
            nn.ReLU(),
            nn.Dropout(p),
            nn.Linear(fc1, fc2),
            nn.BatchNorm1d(fc2),
            nn.ReLU(),
            nn.Dropout(p),
            nn.Linear(fc2, action_dim),
        )

    def forward(self, x):
        return self.fc(x)


class ExperienceReplay(deque):
    def sample(self, size):
        batch = random.sample(self, size)
        return list(zip(*batch))


class DQN:
    def __init__(self, state_dim, action_dim):
        self.steps = 0 # Do not change
        self.model = QModel(state_dim, action_dim).to(DEVICE) # Torch model

        self.optimizer = Adam(self.model.parameters(), lr=LEARNING_RATE)
        self.scheduler = lr_scheduler.StepLR(
            self.optimizer,
            step_size=10_000,
            gamma=0.9
        )
        self.loss = nn.MSELoss()

        self.target_model = QModel(state_dim, action_dim).to(DEVICE)
        self.update_target_network()
        
        self.buffer = ExperienceReplay(maxlen=BUFFER_SIZE)

    def consume_transition(self, transition):
        # Add transition to a replay buffer.
        # Hint: use deque with specified maxlen. It will remove old experience automatically.
        self.buffer.append(transition)

    def sample_batch(self):
        # Sample batch from a replay buffer.
        # Hints:
        # 1. Use random.randint
        # 2. Turn your batch into a numpy.array before turning it to a Tensor. It will work faster
        batch = self.buffer.sample(BATCH_SIZE)
        state, action, next_state, reward, done = batch

        state      = torch.tensor(np.array(state,      dtype=np.float32)).to(DEVICE) 
        action     = torch.tensor(np.array(action,     dtype=np.int64  )).to(DEVICE)
        next_state = torch.tensor(np.array(next_state, dtype=np.float32)).to(DEVICE)
        reward     = torch.tensor(np.array(reward,     dtype=np.float32)).to(DEVICE)
        done       = torch.tensor(np.array(done,       dtype=np.int32  )).to(DEVICE)

        return state, action, next_state, reward, done
        
    def train_step(self, batch):
        # Use batch to update DQN's network.
        if not self.model.training:
            self.model.train()
        self.optimizer.zero_grad()

        state, action, next_state, reward, done = batch

        Q = self.model(state)
        next_action = torch.argmax(Q, 1)
        Q = Q.gather(1, action.view(-1, 1)).squeeze(1)

        target_Q = self.target_model(next_state)
        target_Q = target_Q.gather(1, next_action.view(-1, 1)).squeeze(1)
        target_Q = (1 - done) * target_Q

        loss = self.loss(Q, reward + GAMMA * target_Q)
        loss.backward()
        self.optimizer.step()
        if self.steps > 1_000_000:
            self.scheduler.step(loss)
        
    def update_target_network(self):
        # Update weights of a target Q-network here. You may use copy.deepcopy to do this or 
        # assign a values of network parameters via PyTorch methods.
        self.target_model.load_state_dict(self.model.state_dict())

    def act(self, state, target=False):
        # Compute an action. Do not forget to turn state to a Tensor and then turn an action to a numpy array.
        if self.model.training:
            self.model.eval()
        state = torch.tensor(np.array(state)).view(1, -1).to(DEVICE)
        network = self.target_model if target else self.model
        rewards = network(state).squeeze(0).detach().cpu().numpy()
        return np.argmax(rewards)

    def update(self, transition):
        # You don't need to change this
        self.consume_transition(transition)
        if self.steps % STEPS_PER_UPDATE == 0:
            batch = self.sample_batch()
            self.train_step(batch)
        if self.steps % STEPS_PER_TARGET_UPDATE == 0:
            self.update_target_network()
        self.steps += 1

    def save(self):
        torch.save(self.model.state_dict(), "agent.pkl")


def evaluate_policy(agent, episodes=5):
    env = make("LunarLander-v2")
    returns = []
    for _ in range(episodes):
        done = False
        state = env.reset()
        total_reward = 0.
        
        while not done:
            state, reward, done, _ = env.step(agent.act(state))
            total_reward += reward
        returns.append(total_reward)
    return returns


if __name__ == "__main__":
    
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)

    env = make("LunarLander-v2")
    dqn = DQN(state_dim=env.observation_space.shape[0], action_dim=env.action_space.n)
    eps, min_eps, eps_step = 0.1, 0.005, 50_000
    state = env.reset()
    
    for _ in range(INITIAL_STEPS):
        action = env.action_space.sample()

        next_state, reward, done, _ = env.step(action)
        dqn.consume_transition((state, action, next_state, reward, done))
        
        state = next_state if not done else env.reset()
        
    
    for i in range(TRANSITIONS):
        #Epsilon-greedy policy

        if i % eps_step == 0:
            eps = max(eps / 2, min_eps)

        if random.random() < eps:
            action = env.action_space.sample()
        else:
            action = dqn.act(state)

        next_state, reward, done, _ = env.step(action)
        dqn.update((state, action, next_state, reward, done))
        
        state = next_state if not done else env.reset()
        
        if (i + 1) % (TRANSITIONS//100) == 0:
            rewards = evaluate_policy(dqn, 5)
            print(f"Step: {i+1}, Reward mean: {np.mean(rewards)}, Reward std: {np.std(rewards)}")
            dqn.save()