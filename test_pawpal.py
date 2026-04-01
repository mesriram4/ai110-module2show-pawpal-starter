# test_pawpal.py
from pawpal_system import Tasks, Pets, Owner, Scheduler


# --- Helpers ---
# Builds a minimal owner + pet + task setup so each test doesn't repeat boilerplate.

def make_scheduler():
    owner = Owner("Matt")
    bosco = Pets("Bosco", "Dog")
    walk  = Tasks("Walk Bosco", "Walk around park", "1.5 hours", "Daily", "high", "Morning")
    feed  = Tasks("Feed Bosco", "Give kibble", "10 minutes", "Daily", "medium", "Afternoon")

    bosco.add_task(walk)
    bosco.add_task(feed)
    owner.add_pet(bosco)
    owner.tasks = [task for pet in owner.pets for task in pet.tasks]

    return Scheduler(owner), bosco, walk, feed


# --- Tests ---

def test_task_starts_incomplete():
    """A new task should have mark_complete set to False by default."""
    _, _, walk, _ = make_scheduler()
    assert walk.mark_complete == False


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip the task's mark_complete to True."""
    scheduler, _, walk, _ = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    assert walk.mark_complete == True


def test_mark_complete_returns_success_message():
    """mark_complete() should return a confirmation string when task is found."""
    scheduler, _, _, _ = make_scheduler()
    result = scheduler.mark_complete("Bosco", "Walk Bosco")
    assert result == "Walk Bosco for Bosco has been completed"


def test_mark_complete_wrong_pet_name():
    """mark_complete() should return 'not found' if the pet name doesn't exist."""
    scheduler, _, _, _ = make_scheduler()
    result = scheduler.mark_complete("Leo", "Walk Bosco")
    assert result == "Task or pet not found."


def test_mark_complete_wrong_task_name():
    """mark_complete() should return 'not found' if the task name doesn't exist."""
    scheduler, _, _, _ = make_scheduler()
    result = scheduler.mark_complete("Bosco", "Nonexistent Task")
    assert result == "Task or pet not found."


def test_mark_complete_only_affects_target_task():
    """Completing one task should not change the status of other tasks."""
    scheduler, _, walk, feed = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    assert walk.mark_complete == True
    assert feed.mark_complete == False  # untouched task must stay False


# --- Task Count Tests ---

def test_pet_starts_with_no_tasks():
    """A newly created pet should have an empty task list."""
    bosco = Pets("Bosco", "Dog")
    assert len(bosco.tasks) == 0


def test_adding_one_task_increases_count():
    """Adding one task should bring the pet's task count from 0 to 1."""
    bosco = Pets("Bosco", "Dog")
    walk = Tasks("Walk Bosco", "Walk around park", "1.5 hours", "Daily", "high", "Morning")
    bosco.add_task(walk)
    assert len(bosco.tasks) == 1


def test_adding_multiple_tasks_increases_count():
    """Each add_task() call should increase the count by exactly one."""
    bosco = Pets("Bosco", "Dog")
    walk = Tasks("Walk Bosco", "Walk around park", "1.5 hours", "Daily", "high", "Morning")
    feed = Tasks("Feed Bosco", "Give kibble", "10 minutes", "Daily", "medium", "Afternoon")
    chew = Tasks("Chew Toy", "Give chew toy", "10 minutes", "Monthly", "low", "Evening")

    bosco.add_task(walk)
    assert len(bosco.tasks) == 1

    bosco.add_task(feed)
    assert len(bosco.tasks) == 2

    bosco.add_task(chew)
    assert len(bosco.tasks) == 3


def test_tasks_not_shared_between_pets():
    """Adding a task to one pet should not affect another pet's task count."""
    bosco = Pets("Bosco", "Dog")
    leo   = Pets("Leo", "Fish")
    walk  = Tasks("Walk Bosco", "Walk around park", "1.5 hours", "Daily", "high", "Morning")

    bosco.add_task(walk)
    assert len(bosco.tasks) == 1
    assert len(leo.tasks) == 0
