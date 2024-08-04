from enum import Enum, auto


class Operation(Enum):
    read = auto()
    update_list = auto()
    delete_list = auto()
    edit_sharing = auto()

    update_task = auto()

    add_task_to_list = auto()
    delete_task_from_list = auto()
