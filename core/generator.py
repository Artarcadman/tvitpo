import random
from core.task import BasicTask, ExtendedTask, Priority, TaskState
from typing import List, Dict

def generate_task(name_prefix: str, count: int) -> List:
    tasks = []
    for i in range(count):
        name = f"{name_prefix}_{i}"
        priority = random.choice(list(Priority))
        task_type = random.choice([BasicTask, ExtendedTask])
        task = task_type(name, priority)
        task.activate()
        tasks.append(task)
    return tasks

def generate_events(tasks: List):
    events = {}
    for task in tasks:
        if isinstance(task, ExtendedTask) and task.state == TaskState.READY:
            task.start()  # Переводим в RUNNING
            event_name = f"event_{random.randint(0, 2)}"
            task.event = event_name  # <== вот это важно
            task.wait(event_name)   # теперь событие задано
            events.setdefault(event_name, []).append(task)
    return events

