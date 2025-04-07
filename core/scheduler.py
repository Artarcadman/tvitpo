from core.task import Task, Priority, TaskState
from typing import Optional, List


    
class Scheduler:
    # Queues by priority: 0 - 3
    def __init__(self):
        self.ready_queues = {p: [] for p in Priority}
        self.running_task: Optional[Task] = None
        
    def add_task(self, task: Task):
        if task.state == TaskState.READY:
            self.ready_queues[task.priority].append(task)
            
    def get_next_task(self) -> Optional[Task]:
        for priority in reversed(Priority):  # от HIGH к LOW
            queue = self.ready_queues[priority]
            while queue:
                candidate = queue.pop(0)
                if candidate.state == TaskState.READY:
                    return candidate
        return None

    
    def run_next(self):
        if self.running_task:
            print(f"Running task: {self.running_task.name}")
            return

        next_task = self.get_next_task()
        if next_task:
            next_task.start()
            self.running_task = next_task
        else:
            print("No tasks to start")

    def terminate_current(self):
        if self.running_task:
            self.running_task.terminate()
            self.running_task = None
            self.run_next()
        else:
            print("No task to finish")

    def preempt_if_needed(self, new_task: Task):
        if (self.running_task and 
            new_task.priority.value > self.running_task.priority.value):
            
            print(f"Preempt: {self.running_task.name} -> {new_task.name}")
            self.running_task.preempt()
            self.add_task(self.running_task)
            self.running_task = None
            
            self.add_task(new_task)
            self.run_next()
        else:
            self.add_task(new_task)

    
    def tick(self):
        pass
    
