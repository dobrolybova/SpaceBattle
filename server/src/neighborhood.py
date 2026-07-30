from server.src.exceptions import OutOfGrid
from server.src.interfaces import IMovable, Obj


class SimpleNeighborhoodSystem:
    def __init__(self, grid: int):
        self.grid: int = grid
        # just to make it simple
        self.neighbor_size: float = grid / 2
        self.neighbor_nums = 4
        self.neighborhood: dict = {1: [], 2: [], 3: [], 4: []}
        self.obj_neighborhood: dict = {}
        self.cur_neighbor_num = 0
        """
                         Y        neighbor_size
                  grid   ___________________________
                        |     3      |       4       |
          neighbor_size |____________|_______________| neighbor_size
                        |     1      |       2       |
                        |____________|_______________| X
                        0       neighbor_size        grid
        
        """

    def update_neighborhood(self, obj: IMovable | Obj) -> None:
        self.neighborhood.get(self.cur_neighbor_num).append(obj)
        self.obj_neighborhood.update({obj.get_id(): self.cur_neighbor_num})

    def define_neighborhood(self, obj: IMovable | Obj) -> int:
        if 0 <= obj.get_location().x < self.neighbor_size:
            if 0 <= obj.get_location().y < self.neighbor_size:
                return 1
            if self.neighbor_size <= obj.get_location().y <= self.grid:
                return 3
        elif self.neighbor_size <= obj.get_location().x <= self.grid:
            if 0 <= obj.get_location().y < self.neighbor_size:
                return 2
            if self.neighbor_size <= obj.get_location().y <= self.grid:
                return 4
        raise OutOfGrid(obj=obj)

    def delete_obj_from_neighborhood(self, obj: IMovable | Obj) -> None:
        neighbor_num = self.obj_neighborhood.get(obj.get_id())
        del self.obj_neighborhood[obj.get_id()]
        self.neighborhood.get(neighbor_num).remove(obj)



class ComplexNeighborhoodSystem:
    def __init__(self, grid: int):
        self.grid: int = grid
        # just to make it simple
        self.neighbor_size: float = grid / 3
        self.neighbor_nums = 9
        self.neighborhood: dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
        self.obj_neighborhood: dict = {}
        self.cur_neighbor_num = 0
        """
                         Y   neighbor_size   neighbor_size
                  grid   ______________________________________
                        |     7      |       8     |      9    |
          neighbor_size |____________|_____________|___________| neighbor_size
                        |     4      |       5     |     6     |
          neighbor_size |____________|_____________|___________| neighbor_size
                        |     1      |       2     |    3      |
                        |____________|_____________|___________| X
                        0   neighbor_size    neighbor_size    grid

        """

    def update_neighborhood(self, obj: IMovable | Obj) -> None:
        self.neighborhood.get(self.cur_neighbor_num).append(obj)
        self.obj_neighborhood.update({obj.get_id(): self.cur_neighbor_num})

    def define_neighborhood(self, obj: IMovable | Obj) -> int:      # pylint: disable=R0911
        if 0 <= obj.get_location().x < self.neighbor_size:
            if 0 <= obj.get_location().y < self.neighbor_size:
                return 1
            if self.neighbor_size <= obj.get_location().y < self.neighbor_size * 2:
                return 4
            if self.neighbor_size * 2 <= obj.get_location().y <= self.grid:
                return 7
        elif self.neighbor_size <= obj.get_location().x < self.neighbor_size * 2:
            if 0 <= obj.get_location().y < self.neighbor_size:
                return 2
            if self.neighbor_size <= obj.get_location().y < self.neighbor_size * 2:
                return 5
            if self.neighbor_size * 2 <= obj.get_location().y <= self.grid:
                return 8
        elif self.neighbor_size * 2 <= obj.get_location().x <= self.grid:
            if 0 <= obj.get_location().y < self.neighbor_size:
                return 3
            if self.neighbor_size <= obj.get_location().y < self.neighbor_size * 2:
                return 6
            if self.neighbor_size * 2 <= obj.get_location().y <= self.grid:
                return 9
        raise OutOfGrid(obj=obj)

    def delete_obj_from_neighborhood(self, obj: IMovable | Obj) -> None:
        neighbor_num = self.obj_neighborhood.get(obj.get_id())
        del self.obj_neighborhood[obj.get_id()]
        self.neighborhood.get(neighbor_num).remove(obj)
