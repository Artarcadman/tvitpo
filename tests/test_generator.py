from core.generator import generate_task, generate_events
from core.task import BasicTask, ExtendedTask, Priority

def test_generate_task_creates_correct_number():
    tasks = generate_task("T", 10)
    assert len(tasks) == 10
    for i, task in enumerate(tasks):
        assert task.name == f"T_{i}"
        assert isinstance(task.priority, Priority)
        assert isinstance(task, (BasicTask, ExtendedTask))
        assert task.state.name == "READY"

def test_generate_task_contains_extended_and_basic():
    found_basic = found_extended = False
    for _ in range(50):  # Генерим много раз для уверенности
        tasks = generate_task("Mix", 10)
        for task in tasks:
            if isinstance(task, BasicTask):
                found_basic = True
            if isinstance(task, ExtendedTask):
                found_extended = True
        if found_basic and found_extended:
            break
    assert found_basic
    assert found_extended

def test_generate_events_only_assigns_to_extended_tasks():
    tasks = generate_task("Evt", 10)
    events = generate_events(tasks)

    for event_name, task_list in events.items():
        for task in task_list:
            assert isinstance(task, ExtendedTask)
            assert task.event == event_name

def test_generate_events_empty_if_no_extended_tasks():
    # Принудительно создаем только BasicTask
    tasks = [BasicTask(f"basic_{i}", Priority.LOW) for i in range(5)]
    for t in tasks:
        t.activate()
    events = generate_events(tasks)
    assert events == {}
