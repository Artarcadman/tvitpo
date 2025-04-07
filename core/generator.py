from core.task import BasicTask, ExtendedTask, Priority
from core.scheduler import Scheduler
from core.event_manager import EventManager

if __name__ == "__main__":
    scheduler = Scheduler()
    event_manager = EventManager()

    t1 = BasicTask("LowTask", Priority.LOW)
    t2 = BasicTask("HighTask", Priority.HIGH)
    t3 = ExtendedTask("ExtTask", Priority.MEDIUM)

    t1.activate()
    t2.activate()
    t3.activate()

    scheduler.preempt_if_needed(t1)
    scheduler.preempt_if_needed(t2)
    scheduler.preempt_if_needed(t3)

    scheduler.run_next()  # должен запустить HighTask
    scheduler.terminate_current()  # завершить HighTask

    scheduler.run_next()  # запустит ExtTask
    event_manager.wait_for_event(t3, "io_done")

    scheduler.run_next()  # запустит LowTask

    event_manager.fire_event("io_done")
    scheduler.preempt_if_needed(t3)