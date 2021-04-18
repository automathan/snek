import sys
import random
from agent import Agent
import agent_tailchaser
from snek.environment import Snek

if '--novid' in sys.argv:
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"

def main():
    env = Snek()
    agent = Agent(env)

    if '--test' not in sys.argv:
        total_len = 0
        num_episodes = 0
        state = env.reset()

        while True:
            state, _, done, _ = env.step(agent.act(state))

            env.render() # Comment out this call to train faster

            if done:
                total_len += env.player.len
                num_episodes += 1
                state = env.reset()
                print('Average len: {:.1f}'.format(total_len / num_episodes))

if __name__ == '__main__':
    main()
