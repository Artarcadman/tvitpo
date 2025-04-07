import pytest
from core.task import BasicTask, ExtendedTask, Priority, TaskState

def test_basic_task_lifecycle():
    task = BasicTask("TestBasic", Priority.MEDIUM)
    assert task.state == TaskState.SUSPENDED
    task.activate()
    assert task.state == TaskState.READY
    task.start()
    assert task.state == TaskState.RUNNING
    task.terminate()
    assert task.state == TaskState.SUSPENDED

def test_invalid_transitions():
    task = BasicTask("Invalid", Priority.LOW)
    with pytest.raises(Exception):
        task.start()
    with pytest.raises(Exception):
        task.preempt()


def test_extended_task_wait_release():
    task = ExtendedTask("ExtTask", Priority.HIGH)
    task.activate()
    task.start()
    task.wait("event_x")
    assert task.state == TaskState.WAITING
    task.release()
    assert task.state == TaskState.READY
