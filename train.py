import sys
from agent import Agent
from stable_baselines3 import DQN
from stable_baselines3.common.logger import configure
from snek.environment import Snek

if '--novid' in sys.argv:
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"

def main():
    env = Snek()
    #agent = Agent(env)
    
    new_logger = configure('./results', ["stdout", "csv", "json", "log"])
    model = DQN("MlpPolicy", env, verbose=1)
    model.set_logger(new_logger)
    model.learn(total_timesteps=400000, log_interval=4)
    #model.save("dqn_snek")

    if '--test' not in sys.argv:
        total_len = 0
        num_episodes = 0
        obs = env.reset()

        while True:
            action, _states = model.predict(obs, deterministic=False)
            obs, _, done, _ = env.step(action)
            
            env.render() # Comment out this call to train faster

            if done:
                total_len += env.player.len
                num_episodes += 1
                obs = env.reset()
                print('Average len: {:.1f}'.format(total_len / num_episodes))

if __name__ == '__main__':
    main()
