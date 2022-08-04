import numpy as np
from gym.spaces import Box

class RandomTeacher():
    def __init__(self, mins, maxs, seed=None):
        self.seed = seed
        if not seed:
            self.seed = np.random.randint(42,424242)
        np.random.seed(self.seed)

        self.mins = mins
        self.maxs = maxs

        self.random_task_generator = Box(np.array(mins), np.array(maxs), dtype=np.int64)

    def update(self, task, competence):
        pass

    def sample_task(self):
        v1 = self.random_task_generator.sample()
        mins = [0, 0, 1, 1, 0]
        maxs = [v1[0]-1, v1[1]-1, v1[2]-2, v1[2]-2, 3]
        
        for _ in range(0,18):
            mins.append(-1)
            maxs.append(v1[0]-1)
            mins.append(0)
            maxs.append(v1[1]-1)
            mins.append(5)
            maxs.append(7)
            mins.append(0)
            maxs.append(5)
            mins.append(1)
            maxs.append(v1[2]-2)
            mins.append(1)
            maxs.append(v1[2]-2)
        
        for i in range(0,12):
            if i == 0 and v1[1] > 1:
                mins.append(-1)
                maxs.append(5)
            elif i == 1 and v1[0] > 1:
                mins.append(-1)
                maxs.append(5)
            elif i == 2 and v1[1] > 1 and v1[0] > 1:
                mins.append(-1)
                maxs.append(5)
            elif i == 3 and v1[0] > 2:
                mins.append(-1)
                maxs.append(5)
            elif i == 4 and v1[0] > 2 and v1[1] > 1:
                mins.append(-1)
                maxs.append(5)
            elif i == 5 and v1[1] > 2:
                mins.append(-1)
                maxs.append(5)
            elif i == 6 and v1[1] > 1 and v1[0] > 1:
                mins.append(-1)
                maxs.append(5)
            elif i == 7 and v1[1] > 1 and v1[0] > 2:
                mins.append(-1)
                maxs.append(5)
            elif i == 8 and v1[0] > 2 and v1[1] > 1:
                mins.append(-1)
                maxs.append(5)
            elif i == 9 and v1[1] > 2 and v1[0] > 2:
                mins.append(-1)
                maxs.append(5)
            elif i == 10 and v1[1] > 1 and v1[0] > 2:
                mins.append(-1)
                maxs.append(5)
            elif i == 11 and v1[1] > 2 and v1[0] > 2:
                mins.append(-1)
                maxs.append(5)
            else:  
                mins.append(-1)
                maxs.append(-1)
                
                
            mins.append(0)
            maxs.append(1)
            mins.append(1)
            maxs.append(v1[2]-3)
        
        mins.append(-1)
        maxs.append(18)
        mins.append(-1)
        maxs.append(18)
        
        mins.append(0)
        maxs.append(5)
        
        v2 = Box(np.array(mins), np.array(maxs), dtype=np.int64)
        
        return np.concatenate([v1, v2.sample()])
   

    def dump(self, dump_dict):
        return dump_dict