from queue import PriorityQueue
import numpy as np
from snek.environment import Snek

class Agent:
    def __init__(self, env):
        self.env = env
        self.paths = []
        self.tailchase = False
        self.tc_steps = 0

    def act(self, env_state):
        smap = np.zeros((self.env.width, self.env.height))
        for pos in list(self.env.player.tail)[1:-1]:
            smap[pos[0]][pos[1]] = 1
        graph = GridGraph((self.env.width, self.env.height), smap)
        
        if self.tailchase:
            path = graph.get_shortest_path((self.env.player.pos_x, self.env.player.pos_y), 
                                           self.env.player.tail[-1])
            self.tc_steps += 1
            if path and path[-1] == self.env.player.tail[-1]:
                self.tailchase = False
            if self.tc_steps >= self.env.player.len:
                self.tailchase = False        
            if self.env.player.len < 11:
                self.tailchase = False      
        else:
            path = graph.get_shortest_path((self.env.player.pos_x, self.env.player.pos_y), 
                                           (self.env.food.pos_x, self.env.food.pos_y))
            self.tc_steps = 0
            if self.env.player.len >= 11 and path and len(path) < 2:
                self.tailchase = True
            
        
        action = Snek.NOP
        if path:
            action = self.follow_path(path, (self.env.player.pos_x, self.env.player.pos_y))
        
        return action if action else Snek.NOP

    def follow_path(self, path, bot_pos):
        if not path:
            return None
        pos = path[-1]

        action = Snek.NOP

        if pos[0] - bot_pos[0] == 1 or pos[0] - bot_pos[0] == -(self.env.width - 1):
            action = Snek.RIGHT
        if pos[0] - bot_pos[0] == -1 or pos[0] - bot_pos[0] == self.env.width - 1:
            action = Snek.LEFT
        if pos[1] - bot_pos[1] == 1 or pos[1] - bot_pos[1] == -(self.env.height - 1):
            action = Snek.DOWN
        if pos[1] - bot_pos[1] == -1 or pos[1] - bot_pos[1] == self.env.height - 1:
            action = Snek.UP

        return action

class GridGraph:
    def __init__(self, dimensions, solids):
        self.width, self.height = dimensions
        self.gdict = {}

        # Build graph
        for cell_x in range(self.width):
            for cell_y in range(self.height):
                if solids[cell_x][cell_y] == 0:
                    neighbors = []
                    if solids[(cell_x + 1) % self.width][cell_y] == 0:
                        neighbors.append(((cell_x + 1) % self.width, cell_y))
                    if solids[(cell_x - 1) % self.width][cell_y] == 0:
                        neighbors.append(((cell_x - 1) % self.width, cell_y))
                    if solids[cell_x][(cell_y + 1) % self.height] == 0:
                        neighbors.append((cell_x, (cell_y + 1) % self.height))
                    if solids[cell_x][(cell_y - 1) % self.height] == 0:
                        neighbors.append((cell_x, (cell_y - 1) % self.height))

                    self.gdict[(cell_x, cell_y)] = neighbors

    # Dijkstra, returns reverse path [dst is first element]
    def get_shortest_path(self, src, dst):
        
        if src not in self.gdict.keys() or \
           dst not in self.gdict.keys() or \
           src == dst:
            return None

        pbuf = PriorityQueue()
        pbuf.put((0, src))

        unex = list(filter(lambda x: x != src, self.gdict.keys()))
        parent = {}

        while not pbuf.empty():
            dist, pos = pbuf.get()
            if pos == dst:
                path = [pos] # reverse
                cnode = parent[pos]

                while cnode in parent.keys():
                    path.append(cnode)
                    cnode = parent[cnode]

                return path

            for npos in self.gdict[pos]:
                if npos in unex:
                    pbuf.put((dist + 1, npos))
                    unex.remove(npos)
                    parent[npos] = pos
        
        return None
