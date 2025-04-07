from core.task import ExtendedTask
from typing import List

class EventManager:
    def __init__(self):
        self.waiting_tasks: dict[str, List[ExtendedTask]] = {}
        
    def wait_for_event(self, task: ExtendedTask, event_name: str):
        if event_name not in self.waiting_tasks:
            self.waiting_tasks[event_name] = []
        self.waiting_tasks[event_name].append(task)
        task.wait(event_name)
        
    def fire_event(self, event_name: str):
        if event_name in self.waiting_tasks:
            for task in self.waiting_tasks[event_name]:
                task.release()
            self.waiting_tasks[event_name] = []