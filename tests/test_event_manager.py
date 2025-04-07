from core.task import ExtendedTask, Priority, TaskState
from core.event_manager import EventManager

def test_event_wait_and_fire():
    manager = EventManager()
    task = ExtendedTask("Waiter", Priority.MEDIUM)
    task.activate()
    task.start()

    manager.wait_for_event(task, "data_ready")
    assert task.state == TaskState.WAITING

    manager.fire_event("data_ready")
    assert task.state == TaskState.READY