import random
from core.task import BasicTask, ExtendedTask, Priority
from typing import List

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
        if isinstance(task, ExtendedTask):
            event_name = f"event_{random.randint(0, 2)}"
            task.wait(event_name)
            events.setdefault(event_name, []).append(task)
    return events