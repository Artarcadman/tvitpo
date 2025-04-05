from enum import Enum, auto
from typing import Optional, List
import uuid


# Task Type: BASIC and EXTENDED
class TaskType(Enum):
    BASIC = 'basic'
    EXTENDED = 'extended'
    
    
# Task State
class TaskState(Enum):
    SUSPENDED = 'suspended'
    READY = 'ready'
    RUNNING = 'running'
    WAITING = 'waiting'
    

# Priority
class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3
    
    
class Task:
    def __init__(self, name: str, priority: Priority, task_type: TaskType):
        self.id = str(uuid.uuid4()) #Unique ID
        self.name = name
        self.priority = priority
        self.type = task_type
        self.state = TaskState.SUSPENDED # SUSPENDED is default state
        self.waiting_for_event = False # For EXTENDED tasks only
        self.event = None # Event name if task is waiting
        
    def activate(self):
        if self.state == TaskState.SUSPENDED:
            self.state = TaskState.READY
    
    def start(self):
        if self.state == TaskState.READY:
            self.state = TaskState.RUNNING
            
    def preempt(self):
        if self.state == TaskState.RUNNING:
            self.state = TaskState.READY
            
    def terminate(self):
        if self.state == TaskState.READY:
            self.state = TaskState.SUSPENDED

class BasicTask(Task):
    def __init__(self, name:str, priority: Priority):
        super().__init__(name, priority, TaskType.BASIC)
        
class ExtendedTask(Task):
    def __init__(self, name:str, priotity: Priority):
        super().__init__(name, priotity, TaskType.EXTENDED)
        
    def wait(self, event_name: str):
        if self.state == TaskState.RUNNING:
            self.state = TaskState.WAITING
            self.waiting_for_event = True
            self.event = event_name
    
    def release(self):
        if self.state == TaskState.WAITING and self.waiting_for_event == True:
            self.state = TaskState.READY
            self.waiting_for_event = False
            self.event = None
            
class Scheduler:
    def __init__(self):
        self.ready_queues = {p for p in Priority}
        self.running_task: Optional[Task] = None
        
    def add_task(self, task: Task):
        if task.state == TaskState.READY:
            self.ready_queues[task.priority].append(task)
            
    def get_next_task(self) -> Optional[Task]:
        return None
    
    def tick(self):
        pass