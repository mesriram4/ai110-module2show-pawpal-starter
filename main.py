from pawpal_system import Tasks, Pets, Owner, Scheduler


def create_owner():
    Matt = Owner("Matt")
    print(f'Information about Owner: {Matt.basic_info()}')
    print(f'Pets: {Matt.owner_pets()}')
    return Matt

def create_pets():
    Bosco = Pets("Bosco", "Dog")
    Leo = Pets("Leo", "Fish")
    print(f'Information about Bosco: {Bosco.pet_info()}')
    print(f'Information about Leo: {Leo.pet_info()}')
    return Bosco, Leo

def create_tasks():
    walk_bosco = Tasks("Walk Bosco", "Walk around park", "1.5 hours", "Daily", "High", "Morning")
    feed_leo   = Tasks("Feed Leo", "Give Leo 3 fish flakes", "5 minutes", "Daily", "Medium", "Afternoon")
    chew_toy   = Tasks("Chew Toy", "Give Bosco a new chew toy", "10 minutes", "Monthly", "Low")
    return walk_bosco, feed_leo, chew_toy

def schedule_tasks(scheduler):
    """Builds and returns an organized schedule using the given Scheduler instance."""
    raw_schedule = scheduler.create_schedule()
    return scheduler.organize_schedule(raw_schedule)

def mark_complete(scheduler, pet_name, task_name):
    """Delegates to Scheduler.mark_complete and returns the result message."""
    return scheduler.mark_complete(pet_name, task_name)


if __name__ == "__main__":
    # --- Setup ---
    Matt = create_owner()
    Bosco, Leo = create_pets()
    walk_bosco, feed_leo, chew_toy = create_tasks()

    Bosco.add_task(walk_bosco)
    Bosco.add_task(chew_toy)
    Leo.add_task(feed_leo)

    Matt.add_pet(Bosco)
    Matt.add_pet(Leo)
    Matt.tasks = [task for pet in Matt.pets for task in pet.tasks]  # aggregate for Scheduler

    # --- Create the Scheduler (single instance reused throughout) ---
    scheduler = Scheduler(Matt)

    # --- Mark tasks complete (only completed tasks appear in the schedule) ---
    print("\n--- Completing Tasks ---")
    print(mark_complete(scheduler, "Bosco", "Walk Bosco"))
    print(mark_complete(scheduler, "Leo", "Feed Leo"))

    # --- Build and display the schedule ---
    schedule = schedule_tasks(scheduler)

    print(f"\n=== Daily Schedule for {Matt.name} ===")
    for pet_name, tasks in schedule.items():
        print(f"\n  {pet_name}:")
        for task_name, time_slot, frequency in tasks:  # 3-tuple: name, slot, frequency
            recur_label = " [Daily]" if frequency.lower() == "daily" else f" [{frequency}]"
            print(f"    [{time_slot}] {task_name}{recur_label}")

    # --- End of day: Daily tasks reset automatically for tomorrow ---
    print(f"\n--- End of Day ---")
    print(scheduler.next_day())
