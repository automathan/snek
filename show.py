import sys
from stable_baselines3 import DQN
from stable_baselines3 import PPO
from snek.environment import Snek

if '--novid' in sys.argv:
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"

def main():
    env = Snek(render_enabled=True)
    model = PPO.load("ppo_snek")
    obs = env.reset()

    while True:
        action, _ = model.predict(obs, deterministic=False)
        obs, _, done, _ = env.step(action)

        env.render() # Comment out this call to train faster

        if done:
            obs = env.reset()

if __name__ == '__main__':
    main()
