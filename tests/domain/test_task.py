# from unittest import TestCase
#
#
# class TestTask(TestCase):
#     def test_is_have_access(self):
#         self.fail()
from uuid import UUID

import pytest

from todoapp.domain.access import Operation
from todoapp.domain.task.entities import Task
from todoapp.domain.task.exceptions import MoveTaskToRestrictedList
from todoapp.domain.task_list.entities import TaskList
from todoapp.domain.task_list.value_objects import SharingRule
from todoapp.domain.user.entities import UserId

OWNER = UserId(UUID("0191458a-6e2f-72e7-9033-9a32f34cf1b0"))
COLLABORATOR = UserId(UUID("0191458a-6e2f-7256-988d-5723efec373a"))


def test_is_have_access_owner():
    task = Task.create("Test", OWNER)
    for op in Operation:
        assert task.is_have_access(OWNER, op)

    assert not task.is_have_access(COLLABORATOR, Operation.read)


def test_is_have_access_delete_creator():
    """
    The user created a task in the general list, then he was removed from access.
    He should have read access to the task.
    """
    task_list = TaskList.create("Test", OWNER)
    task_list.set_sharing_rule(COLLABORATOR, SharingRule(manage_tasks_allowed=True))

    task = Task.create(
        "Owner deleted from access",
        COLLABORATOR,
        task_list=task_list,
    )

    assert task.is_have_access(COLLABORATOR, Operation.read)
    task_list.delete_collaborator(COLLABORATOR)
    assert task.is_have_access(COLLABORATOR, Operation.read)
    assert not task.is_have_access(COLLABORATOR, Operation.update_task)

def test_is_have_access_after_restrict():
    """
    The user created a task in the list, then he was restricted.
    He should have update access to the task.
    """
    task_list = TaskList.create("Test", OWNER)
    task_list.set_sharing_rule(COLLABORATOR, SharingRule(manage_tasks_allowed=True))

    task = Task.create(
        "Owner deleted from access",
        COLLABORATOR,
        task_list=task_list,
    )
    # Test update yourself task, without update_task_allowed
    assert task.is_have_access(COLLABORATOR, Operation.update_task)

    task_list.set_sharing_rule(COLLABORATOR, SharingRule(update_task_allowed=False))
    assert task.is_have_access(COLLABORATOR, Operation.read)
    assert task.is_have_access(COLLABORATOR, Operation.update_task)


def test_move_task_without_owner_access():
    task_list = TaskList.create("Test", OWNER)
    task = Task.create("Test", COLLABORATOR)

    with pytest.raises(MoveTaskToRestrictedList):
        task.set_list(task_list)

