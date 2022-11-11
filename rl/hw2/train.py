import pybullet_envs
# Don't forget to install PyBullet!
from gym import make
import numpy as np
import torch
from torch import nn
from torch.distributions import Normal
from torch.nn import functional as F
from torch.optim import Adam
import random

ENV_NAME = "Walker2DBulletEnv-v0"

LAMBDA = 0.95
GAMMA = 0.98

ACTOR_LR = 3e-4
CRITIC_LR = 1e-3

CLIP = 0.2
NORM_GRAD_CLIP = 0.6
ENTROPY_COEF = 2e-2
BATCHES_PER_UPDATE = 64
BATCH_SIZE = 128
MAX_KL = 2e-2

MIN_TRANSITIONS_PER_UPDATE = 3000
MIN_EPISODES_PER_UPDATE = 4

ITERATIONS = 1000
RANDOM_SEED = 42

    
def compute_lambda_returns_and_gae(trajectory):
    lambda_returns = []
    gae = []
    last_lr = 0.
    last_v = 0.
    for _, _, r, _, v in reversed(trajectory):
        ret = r + GAMMA * (last_v * (1 - LAMBDA) + last_lr * LAMBDA)
        last_lr = ret
        last_v = v
        lambda_returns.append(last_lr)
        gae.append(last_lr - v)
    
    # Each transition contains state, action, old action probability, value estimation and advantage estimation
    return [(s, a, p, v, adv) for (s, a, _, p, _), v, adv in zip(trajectory, reversed(lambda_returns), reversed(gae))]
    


class Actor(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        # Advice: use same log_sigma for all states to improve stability
        # You can do this by defining log_sigma as nn.Parameter(torch.zeros(...))
        self.model = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ELU(),
            nn.Linear(256, 256),
            nn.ELU(),
            nn.Linear(256, action_dim)
        )
        self.log_sigma = nn.Parameter(0.1 * torch.ones(1, action_dim))
        
    def compute_proba(self, state, action):
        # Returns probability of action according to current policy and distribution of actions
        action_means = self.model(state)
        p = Normal(action_means, torch.exp(self.log_sigma))
        return p.log_prob(action).sum(-1), p.entropy()
        
    def act(self, state):
        # Returns an action (with tanh), not-transformed action (without tanh) and distribution of non-transformed actions
        # Remember: agent is not deterministic, sample actions from distribution (e.g. Gaussian)
        action_means = self.model(state)
        p = Normal(action_means, torch.exp(self.log_sigma))
        not_transformed_actions = p.sample()
        actions = torch.tanh(not_transformed_actions)
        return actions, not_transformed_actions, p
        
        
class Critic(nn.Module):
    def __init__(self, state_dim):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ELU(),
            nn.Linear(256, 256),
            nn.ELU(),
            nn.Linear(256, 1)
        )
        
    def get_value(self, state):
        return self.model(state)


class PPO:
    def __init__(self, state_dim, action_dim):
        self.actor = Actor(state_dim, action_dim)
        self.critic = Critic(state_dim)
        self.actor_optim = Adam(self.actor.parameters(), ACTOR_LR)
        self.critic_optim = Adam(self.critic.parameters(), CRITIC_LR)

    def update(self, trajectories):
        transitions = [t for traj in trajectories for t in traj] # Turn a list of trajectories into list of transitions
        state, action, old_prob, target_value, advantage = zip(*transitions)
        state = np.array(state)
        action = np.array(action)
        old_prob = np.array(old_prob)
        target_value = np.array(target_value)
        advantage = np.array(advantage)
        advnatage = (advantage - advantage.mean()) / (advantage.std() + 1e-8)
        
        
        for _ in range(BATCHES_PER_UPDATE):
            idx = np.random.randint(0, len(transitions), BATCH_SIZE) # Choose random batch
            s = torch.tensor(state[idx]).float()
            a = torch.tensor(action[idx]).float()
            op = torch.tensor(old_prob[idx]).float() # Probability of the action in state s.t. old policy
            v = torch.tensor(target_value[idx]).float() # Estimated by lambda-returns 
            adv = torch.tensor(advantage[idx]).float() # Estimated by generalized advantage estimation 
            
            # TODO: Update actor here            
            # TODO: Update critic here

            log_newp, entropy = self.actor.compute_proba(s, a)
            newp = torch.exp(log_newp)

            if F.kl_div(newp, op) > MAX_KL:
                break

            self.critic_optim.zero_grad()
            self.actor_optim.zero_grad()
            
            critic_v = self.critic.get_value(s).squeeze(1)
            critic_loss = F.l1_loss(critic_v, v)

            frac_p = newp / op
            clip_frac_p = torch.clamp(frac_p, 1-CLIP, 1+CLIP)
            actor_loss = -(torch.min(frac_p * adv, clip_frac_p * adv).mean() + ENTROPY_COEF * entropy.mean())

            critic_loss.backward()
            actor_loss.backward()

            torch.nn.utils.clip_grad_norm_(self.actor.parameters(), NORM_GRAD_CLIP)

            self.critic_optim.step()
            self.actor_optim.step()
            
    def get_value(self, state):
        with torch.no_grad():
            state = torch.tensor(np.array([state])).float()
            value = self.critic.get_value(state)
        return value.cpu().item()

    def act(self, state):
        with torch.no_grad():
            state = torch.tensor(np.array([state])).float()
            action, pure_action, distr = self.actor.act(state)
            prob = torch.exp(distr.log_prob(pure_action).sum(-1))
        return action.cpu().numpy()[0], pure_action.cpu().numpy()[0], prob.cpu().item()

    def save(self):
        torch.save(self.actor.state_dict(), "agent.pkl")


def evaluate_policy(env, agent, episodes=5):
    returns = []
    for _ in range(episodes):
        done = False
        state = env.reset()
        total_reward = 0.
        
        while not done:
            state, reward, done, _ = env.step(agent.act(state)[0])
            total_reward += reward
        returns.append(total_reward)
    return returns
   

def sample_episode(env, agent):
    s = env.reset()
    d = False
    trajectory = []
    while not d:
        a, pa, p = agent.act(s)
        v = agent.get_value(s)
        ns, r, d, _ = env.step(a)
        trajectory.append((s, pa, r, p, v))
        s = ns
    return compute_lambda_returns_and_gae(trajectory)


def set_seed(env, seed=RANDOM_SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    env.seed(seed)
    env.action_space.seed(seed)
    env.observation_space.seed(seed)


if __name__ == "__main__":
    env = make(ENV_NAME)
    set_seed(env)
    ppo = PPO(state_dim=env.observation_space.shape[0], action_dim=env.action_space.shape[0])
    state = env.reset()
    episodes_sampled = 0
    steps_sampled = 0
    
    for i in range(ITERATIONS):
        trajectories = []
        steps_ctn = 0
        
        while len(trajectories) < MIN_EPISODES_PER_UPDATE or steps_ctn < MIN_TRANSITIONS_PER_UPDATE:
            traj = sample_episode(env, ppo)
            steps_ctn += len(traj)
            trajectories.append(traj)
        episodes_sampled += len(trajectories)
        steps_sampled += steps_ctn

        ppo.update(trajectories)        
        
        if (i + 1) % (ITERATIONS//100) == 0:
            rewards = evaluate_policy(env, ppo, 5)
            print(f"Step: {i+1}, Reward mean: {np.mean(rewards)}, Reward std: {np.std(rewards)}, Episodes: {episodes_sampled}, Steps: {steps_sampled}")
            ppo.save()