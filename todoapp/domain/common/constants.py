from enum import Enum, auto


class Empty(Enum):
    UNSET = "UNSET"


class Operation(Enum):
    read = auto()
    update_task_list = auto()
    delete_task_list = auto()

    update_task = auto()

    add_task_to_list = auto()
    delete_task_from_list = auto()
