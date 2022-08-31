import numpy as np
from gym.spaces import Box

DIR_TO_VEC = [
    # Pointing right (positive X)
    np.array((1, 0)),
    # Down (positive Y)
    np.array((0, 1)),
    # Pointing left (negative X)
    np.array((-1, 0)),
    # Up (negative Y)
    np.array((0, -1)),
]

def distance(p1, p2):
        xa, ya = p1
        xb, yb = p2
        return abs(xa - xb) + abs(ya - yb)

def is_in_front(p1, p2, dir):
    pos = p1+ DIR_TO_VEC[dir]
    return pos[0] == p2[0] and pos[1] == p2[1]
    
class RedBallTeacher():
    def __init__(self, min = 5, threshold = 0.01, seed=None):
        self.seed = seed
        if not seed:
            self.seed = np.random.randint(42,424242)
        np.random.seed(self.seed)
        
        self.min = min
        self.threshold = threshold
        
        self.d = 1
        
        self.rewards = []
    
    def update(self, logs):
        self.rewards.append(logs["return_per_episode"])
        
        if len(self.rewards) > 1:
            if abs(np.mean(self.rewards[-1]) - np.mean(self.rewards[-2])) < self.threshold:
                self.d += 1
                print(abs(np.mean(self.rewards[-1]) - np.mean(self.rewards[-2])))
                print("Distance increased to: " + str(self.d))
                

    def sample_task(self):
        vector = [1, 1, self.min+self.d, 0, 0]
        
        box = Box(np.array([1, 1]), np.array([self.min+self.d-2, self.min+self.d-2]), dtype=np.int64)
        
        pos_agent = [1,1]
        pos_ball = [1,1]

        while distance(pos_agent, pos_ball) != self.d:
            pos_agent = box.sample()
            pos_ball = box.sample()
        
        dir = np.random.randint(0, 4)
        
        while is_in_front(pos_agent, pos_ball, dir):
            dir = np.random.randint(0, 4)
            
        vector.append(pos_agent[0])
        vector.append(pos_agent[1])
        vector.append(dir)
        
        vector.append(0)
        vector.append(0)
        vector.append(6)
        vector.append(0)
        vector.append(pos_ball[0])
        vector.append(pos_ball[1])
        
        for _ in range(0,140):
            vector.append(-1)
        
        vector.append(0)
        
        return vector
   