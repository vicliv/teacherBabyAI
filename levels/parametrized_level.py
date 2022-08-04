import gym
from collections import OrderedDict

from gym_minigrid.envs import Key, Ball, Box, Door, IDX_TO_COLOR, IDX_TO_OBJECT
from babyai.levels.verifier import *
from babyai.levels.levelgen import *
from babyai.levels.bonus_levels import Level_parametrized

from teachers import *
from teachers.random_teacher import RandomTeacher

min_vector = [1, 1, 6]
max_vector = [3, 3, 8]
                
class Level_vector(Level_parametrized):
    """
    Create a level based on a vector of dimension 154
    """
    def __init__(self, teacher = None, **kwargs):
        if (teacher is None):
            self.teacher = RandomTeacher(min_vector, max_vector)
        else:
            self.teacher = teacher
        
        self.data = teacher.sample_task()
        self.data[0] = 3
        self.data[1] = 3
        self.data[2] = 8
        
        super().__init__(
            **kwargs
        )
    
    def reset(self, **kwargs):
        self.data = self.teacher.sample_task()
        
        self.num_cols = self.data[0]
        self.num_rows = self.data[1]
        self.room_size = self.data[2]
        
        return super().reset(**kwargs)

for name, level in list(globals().items()):
    if name.startswith('Level_'):
        level.is_bonus = True
        
# Register the levels in this file
register_levels(__name__, globals())
