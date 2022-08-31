import gym
from collections import OrderedDict

from gym_minigrid.envs import Key, Ball, Box, Door, IDX_TO_COLOR, IDX_TO_OBJECT
from babyai.levels.verifier import *
from babyai.levels.levelgen import *

from teachers import *
from teachers.random_teacher import RandomTeacher

min_vector = [1, 1, 6]
max_vector = [1, 1, 8]

class Level_parametrized(LevelGen):
    """
    Create a level based on a vector of dimension 155
    """
    def __init__(self, vector = None, **kwargs):
        if (self.data is None):
            if (vector is None):
                with open('vector_config.json') as json_file:
                    self.data = np.array(json.load(json_file))
            else:
                self.data = vector
        
        super().__init__( 
            num_cols = self.data[0],
            num_rows = self.data[1],
            room_size = self.data[2], 
            **kwargs
        )
        
    def gen_mission(self):
        room = self.get_room(self.data[3],self.data[4])
        
        self.agent_pos = room.top + np.array([self.data[5], self.data[6]])
        self.agent_dir = self.data[7]
        
        self.grid.set(*self.agent_pos, None)
        
        objs = []
        for i in range(8, 116, 6):
            if self.data[i] == -1:
                continue

            kind = IDX_TO_OBJECT[self.data[i+2]]
            color=IDX_TO_COLOR[self.data[i+3]]
            pos=np.array([self.data[i+4], self.data[i+5]])
            
            assert kind in ['key', 'ball', 'box']
            if kind == 'key':
                obj = Key(color)
            elif kind == 'ball':
                obj = Ball(color)
            elif kind == 'box':
                obj = Box(color)
            
            assert kind in ['key', 'ball', 'box']
            if kind == 'key':
                obj = Key(color)
            elif kind == 'ball':
                obj = Ball(color)
            elif kind == 'box':
                obj = Box(color)
            
            room = self.get_room(self.data[i], self.data[i+1])
            top = room.top

            pos = pos + top
            
            if self.grid.get(*pos) != None or np.array_equal(pos, self.agent_pos):
                continue
            
            self.put_obj(obj, pos[0], pos[1])
            
            room.objs.append(obj)
            
            objs.append([IDX_TO_OBJECT[self.data[i+2]], IDX_TO_COLOR[self.data[i+3]], pos[0], pos[1]])

        doors = []
        k = 0
        for i in range(116, 152, 3):
            if self.data[i] == -1:
                k += 1
                continue
            
            if k == 0:
                room = self.get_room(0, 0)
                door_idx = 1
            elif k == 1:
                room = self.get_room(0, 0)
                door_idx = 0
            elif k == 2 and self.num_cols > 1:
                room = self.get_room(1, 0)
                door_idx = 1
            elif k == 3 and self.num_cols > 2:
                room = self.get_room(2, 0)
                door_idx = 2
            elif k == 4 and self.num_cols > 2:
                room = self.get_room(2, 0)
                door_idx = 1
            elif k == 5 and self.num_rows > 1:
                room = self.get_room(0, 1)
                door_idx = 1
            elif k == 6 and self.num_rows > 1:
                room = self.get_room(0, 1)
                door_idx = 0
            elif k == 7 and self.num_rows > 1 and self.num_cols > 1:
                room = self.get_room(1, 1)
                door_idx = 1
            elif k == 8 and self.num_rows > 1 and self.num_cols > 2:
                room = self.get_room(2, 1)
                door_idx = 2
            elif k == 9 and self.num_rows > 1 and self.num_cols > 2:
                room = self.get_room(2, 1)
                door_idx = 1
            elif k == 10 and self.num_rows > 2 and self.num_cols > 1:
                room = self.get_room(1, 2)
                door_idx = 2
            elif k == 11  and self.num_rows > 2 and self.num_cols > 1:
                room = self.get_room(1, 2)
                door_idx = 0
            else:
                k += 1
                continue

            color = IDX_TO_COLOR[self.data[i]]
            locked = self.data[i+1]
            pos = self.data[i+2]
            
            assert room.doors[door_idx] is None, "door already exists"

            room.locked = locked
            door = Door(color, is_locked=locked)          

            x_l, y_l = (room.top[0], room.top[1])
            x_m, y_m = (room.top[0] + room.size[0] - 1, room.top[1] + room.size[1] - 1)
            
            if door_idx == 0:
                pos = (x_m, room.top[1] + pos)
            if door_idx == 1:
                pos = (room.top[0] + pos, y_m)
            if door_idx == 2:
                pos = (x_l, room.top[1] + pos)
            if door_idx == 3:
                pos = (room.top[0] + pos, y_l)
                
            neighbor = room.neighbors[door_idx]
            if neighbor is None:
                k += 1
                continue
            
            to_remove = []
            found = False
            if locked:
                for o in objs:
                    if "key" in o and color in o:
                        to_remove.append(o)
                        found = True
            
            for o in to_remove:
                objs.remove(o)
            
            if not found and locked:
                # Until we find a room to put the key
                while True:
                    i = self._rand_int(0, self.num_cols)
                    j = self._rand_int(0, self.num_rows)
                    key_room = self.get_room(i, j)

                    if key_room is self.locked_room:
                        continue

                    self.add_object(i, j, 'key', color)
                    break
            
            room.door_pos[door_idx] = pos

            self.grid.set(*pos, door)
            door.cur_pos = pos
            
            room.doors[door_idx] = door
            neighbor.doors[(door_idx+2) % 4] = door
            k += 1

            doors.append(color)
        
        if self.data[154] == 0 and len(objs) > 0:
            if (self.data[152] == -1 or self.data[152] >= len(objs)):
                obj = self._rand_elem(objs)
            else:
                obj = objs[self.data[152]]
            self.instrs = GoToInstr(ObjDesc(obj[0], obj[1]))
        elif self.data[154] == 1 and len(objs) > 0:
            if (self.data[152] == -1 or self.data[152] >= len(objs)):
                obj = self._rand_elem(objs)
            else:
                obj = objs[self.data[152]]
            self.instrs =  PickupInstr(ObjDesc(obj[0], obj[1]))
        elif self.data[154] == 2 and len(doors) > 0:
            if (self.data[152] == -1 or self.data[152] >= len(doors)):
                color = self._rand_elem(doors)
            else:
                color = doors[self.data[152]]
            self.instrs = OpenInstr(ObjDesc("door", color))
        elif self.data[154] == 3  and len(objs) > 1:
            o1, o2 = self._rand_subset(objs, 2)

            if self.data[152] != -1 and self.data[152] < len(objs):
                o1 = objs[self.data[152]]
            if self.data[153] != -1 and self.data[153] < len(objs) and self.data[152] != self.data[153]:
                o2 = objs[self.data[153]]
            
            max = 10000
            k = 0
            while o1[0] == o2[0] and o1[1] == o2[1]:
                o2 = self._rand_elem(objs)
                k += 1
                if k > max:
                    o1 = self._rand_elem(objs)
            
            k = 0
            while(True):
                next_to = False
                o1s, pos1 = (ObjDesc(o1[0], o1[1])).find_matching_objs(self)
                o2s, pos2 = (ObjDesc(o2[0], o2[1])).find_matching_objs(self)
            
                for p1 in pos1:
                    for p2 in pos2:
                        if pos_next_to(p1, p2):
                            o2 = self._rand_elem(objs)
                            next_to = True
                            break
                if not next_to:
                    break
                k += 1
                if k > max:
                    o1 = self._rand_elem(objs)

            self.instrs = PutNextInstr(
            ObjDesc(o1[0], o1[1]),
            ObjDesc(o2[0], o2[1])
            )

        elif self.data[154] == 4 and len(objs) > 1:
            self.instrs = self.rand_instr(
            action_kinds= ['goto'],
            instr_kinds=self.instr_kinds
            )
        elif self.data[154] == 5 and len(objs) > 0 and len(doors) > 0:
            self.instrs = self.rand_instr(
            action_kinds= self.action_kinds,
            instr_kinds=self.instr_kinds
            )
        else:
            obj, _ = self.add_object(0, 0, 'ball', 'red')
            self.instrs = GoToInstr(ObjDesc('ball', 'red'))
                
class Level_vector(Level_parametrized):
    """
    Create a level based on a vector of dimension 155
    """
    def __init__(self, teacher = RandomTeacher(min_vector, max_vector), **kwargs):
        self.teacher = teacher
        print(type(teacher))
        
        self.data = self.teacher.sample_task()
        self.data[0] = 3
        self.data[1] = 3
        self.data[2] = 8
        
        super().__init__(
            **kwargs
        )
    
    def reset(self, **kwargs):
        self.data = self.teacher.sample_task()
        #print(self.data)
        self.num_cols = self.data[0]
        self.num_rows = self.data[1]
        self.room_size = self.data[2]
        
        return super().reset(**kwargs)

for name, level in list(globals().items()):
    if name.startswith('Level_'):
        level.is_bonus = True
        
# Register the levels in this file
register_levels(__name__, globals())
