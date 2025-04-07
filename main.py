# main.py
from core.scheduler import Scheduler
from core.generator import generate_task, generate_events
from core.event_manager import EventManager
from core.task import ExtendedTask, TaskState
import time
import random


def main():
    NUM_TASKS = 3  # Кол-во случайно сгенерированных задач
    scheduler = Scheduler()
    event_manager = EventManager()

    # 1. Генерация задач
    tasks = generate_task("Task", NUM_TASKS)

    # 1.5 Назначаем события расширенным задачам и переводим в WAITING
    events = generate_events(tasks)
    used_events = set()

    # 2. Добавление задач в планировщик
    for task in tasks:
        task_type = type(task).__name__
        print(f"[{task.name} (Type={task_type}, P={task.priority.value})] SUSPENDED -> READY")
        scheduler.add_task(task)

    # 3. Основной цикл: обработка событий и выполнение задач
    cycle = 0
    while any(task.state != TaskState.SUSPENDED for task in tasks):
        cycle += 1
        print(f"\nЦикл {cycle}:")
        time.sleep(0.5)

        # Если нет активной задачи — запускаем следующую
        if not scheduler.running_task or scheduler.running_task.state != TaskState.RUNNING:
            scheduler.run_next()

        current = scheduler.running_task

        # Если текущая задача — Extended и не в WAITING, переводим её
        if current and isinstance(current, ExtendedTask):
            if current.event is not None and not current.waiting_for_event:
                current.wait(current.event)
                scheduler.running_task = None
                continue


        # Подаем событие, если есть ожидающие задачи
        for event_name, waiting_tasks in events.items():
            still_waiting = [t for t in waiting_tasks if t.state == TaskState.WAITING]
            if still_waiting and event_name not in used_events:
                print(f"Подаем событие: {event_name}")
                for task in still_waiting:
                    task.release()
                    scheduler.add_task(task)
                used_events.add(event_name)
                break

        # Завершаем задачу, если она RUNNING
        if current and current.state == TaskState.RUNNING:
            scheduler.terminate_current()
            print(f"Завершена задача: {current.name}")

        time.sleep(0.3)

    print("\nВсе задачи завершены. Симуляция окончена.")


if __name__ == "__main__":
    main()
