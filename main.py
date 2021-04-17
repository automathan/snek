import sys
import random
from agent import Agent
from snek.environment import Snek

if '--novid' in sys.argv:
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"

def main():
    env = Snek()
    agent = Agent(env)

    if '--test' not in sys.argv:
        state = env.reset()

        while True:
            state, _, done, _ = env.step(agent.act(state))

            env.render() # Comment out this call to train faster

            if done:
                state = env.reset()

if __name__ == '__main__':
    main()
