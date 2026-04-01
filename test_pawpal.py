# test_pawpal.py
from pawpal_system import Tasks, Pets, Owner, Scheduler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_scheduler():
    """Single pet (Bosco) with two Daily tasks."""
    owner = Owner("Matt")
    bosco = Pets("Bosco", "Dog")
    walk  = Tasks("Walk Bosco", "Walk around park", "1.5 hours", "Daily", "high", "Morning")
    feed  = Tasks("Feed Bosco", "Give kibble", "10 minutes", "Daily", "medium", "Afternoon")

    bosco.add_task(walk)
    bosco.add_task(feed)
    owner.add_pet(bosco)
    owner.tasks = [task for pet in owner.pets for task in pet.tasks]

    return Scheduler(owner), bosco, walk, feed


def make_multi_pet_scheduler():
    """Two pets: Bosco has one Daily + one Monthly task; Leo has one Daily task."""
    owner = Owner("Matt")

    bosco = Pets("Bosco", "Dog")
    leo   = Pets("Leo", "Fish")

    walk  = Tasks("Walk Bosco", "Walk around park", "1.5 hours", "Daily",   "high",   "Morning")
    chew  = Tasks("Chew Toy",   "Give chew toy",    "10 minutes","Monthly", "low",    "Evening")
    feed  = Tasks("Feed Leo",   "Give 3 fish flakes","5 minutes", "Daily",   "medium", "Afternoon")

    bosco.add_task(walk)
    bosco.add_task(chew)
    leo.add_task(feed)

    owner.add_pet(bosco)
    owner.add_pet(leo)
    owner.tasks = [task for pet in owner.pets for task in pet.tasks]

    return Scheduler(owner), bosco, leo, walk, chew, feed


# ---------------------------------------------------------------------------
# Existing tests (mark_complete basic behaviour)
# ---------------------------------------------------------------------------

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
    """Daily tasks should return a message that mentions repeating tomorrow."""
    scheduler, _, _, _ = make_scheduler()
    result = scheduler.mark_complete("Bosco", "Walk Bosco")
    assert result == "Walk Bosco for Bosco has been completed and will repeat tomorrow."


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
    assert feed.mark_complete == False


# ---------------------------------------------------------------------------
# Task count tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Schedule filtering — filter_pet and completed
# ---------------------------------------------------------------------------

def test_filter_by_pet_returns_only_that_pet():
    """organize_schedule with filter_pet should exclude all other pets."""
    scheduler, _, _, _, _, _ = make_multi_pet_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    scheduler.mark_complete("Bosco", "Chew Toy")
    scheduler.mark_complete("Leo", "Feed Leo")

    raw = scheduler.create_schedule()
    result = scheduler.organize_schedule(raw, filter_pet="Bosco")

    assert "Bosco" in result
    assert "Leo" not in result


def test_filter_by_pet_unknown_name_returns_empty():
    """filter_pet with a name that doesn't exist should return an empty dict."""
    scheduler, _, _, _, _, _ = make_multi_pet_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")

    raw = scheduler.create_schedule()
    result = scheduler.organize_schedule(raw, filter_pet="Rex")

    assert result == {}


def test_filter_completed_true_returns_only_done_tasks():
    """completed=True should return only tasks whose mark_complete is True."""
    scheduler, _, _, _, _, _ = make_multi_pet_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")  # mark one done, leave chew incomplete

    raw = scheduler.create_schedule()
    result = scheduler.organize_schedule(raw, completed=True)

    bosco_task_names = [entry[0] for entry in result.get("Bosco", [])]
    assert "Walk Bosco" in bosco_task_names
    assert "Chew Toy" not in bosco_task_names


def test_filter_completed_false_returns_no_entries():
    """completed=False on a schedule built from completed tasks should return empty lists.

    create_schedule only includes completed tasks, so filtering that result
    for incomplete (completed=False) should yield nothing.
    """
    scheduler, _, _, _ = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    scheduler.mark_complete("Bosco", "Feed Bosco")

    raw = scheduler.create_schedule()
    result = scheduler.organize_schedule(raw, completed=False)

    assert all(len(entries) == 0 for entries in result.values())


def test_filter_by_pet_and_completed_combined():
    """Combining filter_pet and completed=True should narrow to one pet's done tasks."""
    scheduler, _, _, _, _, _ = make_multi_pet_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    scheduler.mark_complete("Leo", "Feed Leo")

    raw = scheduler.create_schedule()
    result = scheduler.organize_schedule(raw, filter_pet="Leo", completed=True)

    assert "Leo" in result
    assert "Bosco" not in result
    leo_task_names = [entry[0] for entry in result["Leo"]]
    assert "Feed Leo" in leo_task_names


def test_schedule_entries_sorted_morning_afternoon_evening():
    """Entries should come out in Morning -> Afternoon -> Evening order."""
    scheduler, _, _, _ = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    scheduler.mark_complete("Bosco", "Feed Bosco")

    raw = scheduler.create_schedule()
    result = scheduler.organize_schedule(raw)

    TIME_ORDER = {"Morning": 0, "Afternoon": 1, "Evening": 2}
    slots = [entry[1] for entry in result["Bosco"]]
    assert slots == sorted(slots, key=lambda s: TIME_ORDER.get(s, 3))


# ---------------------------------------------------------------------------
# 3-tuple format — frequency carried through create_schedule
# ---------------------------------------------------------------------------

def test_schedule_entry_is_three_tuple():
    """Each schedule entry should be a 3-tuple: (task_name, time_slot, frequency)."""
    scheduler, _, _, _ = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")

    schedule = scheduler.create_schedule()
    entry = schedule["Bosco"][0]

    assert len(entry) == 3


def test_schedule_entry_frequency_matches_task():
    """The third element of each entry should match the task's task_frequency."""
    scheduler, _, walk, _ = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")

    schedule = scheduler.create_schedule()
    _, _, frequency = schedule["Bosco"][0]

    assert frequency == walk.task_frequency


# ---------------------------------------------------------------------------
# Daily frequency — mark_complete interaction with pending_daily
# ---------------------------------------------------------------------------

def test_daily_task_queued_in_pending_daily():
    """Completing a Daily task should add it to pending_daily."""
    scheduler, _, walk, _ = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    assert walk in scheduler.pending_daily


def test_non_daily_task_not_in_pending_daily():
    """Completing a Monthly task should NOT add it to pending_daily."""
    scheduler, _, _, _, chew, _ = make_multi_pet_scheduler()
    scheduler.mark_complete("Bosco", "Chew Toy")
    assert chew not in scheduler.pending_daily


def test_non_daily_returns_standard_message():
    """A Monthly task should return the standard completion message, not the repeat message."""
    scheduler, _, _, _, _, _ = make_multi_pet_scheduler()
    result = scheduler.mark_complete("Bosco", "Chew Toy")
    assert "will repeat tomorrow" not in result
    assert "completed" in result


def test_pending_daily_starts_empty():
    """A fresh Scheduler should have an empty pending_daily list."""
    scheduler, _, _, _ = make_scheduler()
    assert scheduler.pending_daily == []


# ---------------------------------------------------------------------------
# next_day() — daily reset behaviour
# ---------------------------------------------------------------------------

def test_next_day_resets_daily_task_to_incomplete():
    """After next_day(), a completed Daily task should be incomplete again."""
    scheduler, _, walk, _ = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    assert walk.mark_complete == True

    scheduler.next_day()
    assert walk.mark_complete == False


def test_next_day_clears_pending_daily():
    """After next_day(), pending_daily should be empty."""
    scheduler, _, _, _ = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    scheduler.next_day()
    assert len(scheduler.pending_daily) == 0


def test_next_day_with_nothing_pending_returns_message():
    """next_day() with no completed Daily tasks should return the 'no tasks' message."""
    scheduler, _, _, _ = make_scheduler()
    result = scheduler.next_day()
    assert "No daily tasks to reschedule" in result


def test_next_day_does_not_reset_non_daily_tasks():
    """next_day() should leave Monthly (and other non-daily) tasks untouched."""
    scheduler, _, _, _, chew, _ = make_multi_pet_scheduler()
    chew.mark_complete = True   # manually set complete

    scheduler.next_day()       # should not affect chew — it was never in pending_daily

    assert chew.mark_complete == True


def test_next_day_resets_multiple_daily_tasks():
    """next_day() should reset every Daily task that was completed, not just the first."""
    scheduler, _, walk, feed = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    scheduler.mark_complete("Bosco", "Feed Bosco")

    scheduler.next_day()

    assert walk.mark_complete == False
    assert feed.mark_complete == False


def test_next_day_called_twice_second_call_finds_nothing():
    """Calling next_day() a second time in a row should report nothing to reschedule."""
    scheduler, _, _, _ = make_scheduler()
    scheduler.mark_complete("Bosco", "Walk Bosco")
    scheduler.next_day()                     # first call — resets walk
    result = scheduler.next_day()            # second call — nothing left
    assert "No daily tasks to reschedule" in result


def test_next_day_rescheduled_task_reappears_in_schedule():
    """After next_day(), a reset Daily task should be completable again the next cycle."""
    scheduler, _, walk, _ = make_scheduler()

    # Day 1: complete and reset
    scheduler.mark_complete("Bosco", "Walk Bosco")
    scheduler.next_day()

    # Day 2: mark complete again — should work cleanly
    result = scheduler.mark_complete("Bosco", "Walk Bosco")
    assert walk.mark_complete == True
    assert "will repeat tomorrow" in result
