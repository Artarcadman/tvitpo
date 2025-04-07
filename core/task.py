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
        if self.state != TaskState.SUSPENDED:
            raise Exception (f'Can not activate task from {self.state}')
        print(f'[{self.name}] SUSPENDED -> READY')
        self.state = TaskState.READY
        
    def start(self):
        if self.state != TaskState.READY:
            raise Exception (f'Can not start task from {self.state}')
        print(f'[{self.name}] READY -> RUNNING')
        self.state = TaskState.RUNNING
            
    def preempt(self):
        if self.state != TaskState.RUNNING:
            raise Exception(f"Can not preempt task from {self.state}")
        print(f"[{self.name}] RUNNING → READY")
        self.state = TaskState.READY

    def terminate(self):
        if self.state != TaskState.RUNNING:
            raise Exception(f"Can not terminate task from {self.state}")
        print(f"[{self.name}] RUNNING → SUSPENDED")
        self.state = TaskState.SUSPENDED

class BasicTask(Task):
    def __init__(self, name:str, priority: Priority):
        super().__init__(name, priority, TaskType.BASIC)
        
class ExtendedTask(Task):
    def __init__(self, name:str, priority: Priority):
        super().__init__(name, priority, TaskType.EXTENDED)
        
    def wait(self, event_name: str):
        if self.state != TaskState.RUNNING:
            raise Exception(f"Can not wait event from {self.state}")
        print(f"[{self.name}] RUNNING → WAITING (event: {event_name})")
        self.state = TaskState.WAITING
        self.waiting_for_event = True
        self.event = event_name

    def release(self):
        if self.state != TaskState.WAITING or not self.waiting_for_event:
            raise Exception(f"Can not release task from {self.state}")
        print(f"[{self.name}] WAITING → READY (освобождено от события: {self.event})")
        self.state = TaskState.READY
        self.waiting_for_event = False
        self.event = None