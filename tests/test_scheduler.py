from core.task import BasicTask, Priority
from core.scheduler import Scheduler

def test_scheduler_run_order():
    scheduler = Scheduler()
    low = BasicTask("Low", Priority.LOW)
    high = BasicTask("High", Priority.HIGH)

    low.activate()
    high.activate()

    scheduler.add_task(low)
    scheduler.add_task(high)

    scheduler.run_next()
    assert scheduler.running_task.name == "High"
    scheduler.terminate_current()
    assert scheduler.running_task.name == "Low"

def test_scheduler_preemption():
    scheduler = Scheduler()
    t1 = BasicTask("T1", Priority.LOW)
    t2 = BasicTask("T2", Priority.CRITICAL)

    t1.activate()
    t2.activate()

    scheduler.add_task(t1)
    scheduler.run_next()
    scheduler.preempt_if_needed(t2)

    assert scheduler.running_task.name == "T2"
