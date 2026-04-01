
from pawpal_system import Tasks, Pets, Owner, Scheduler 

#Add Owner 

def create_owner(): 
    Matt = Owner("Matt")
    return Matt

def create_pets(): 
    Bosco = Pets("Bosco", "Dog")
    Leo = Pets("Leo", "Fish")
    return Bosco, Leo
    
def create_tasks():
    walk_bosco = Tasks("Walk Bosco", "Walk around park", "1.5 hours", "Daily", "high", "Morning")
    feed_leo = Tasks("Feed Leo", "Give Leo 3 fish flakes", "5 minutes", "Daily", "medium", "Afternoon")
    chew_toy = Tasks("Chew Toy", "Give Bosco a new chew toy", "10 minutes", "Monthly", "low", "Evening")
    return walk_bosco, feed_leo, chew_toy

def schedule_tasks(owner):
    scheduler = Scheduler(owner)
    raw_schedule = scheduler.create_schedule()
    return scheduler.organize_schedule(raw_schedule)


if __name__ == "__main__":
    Matt = create_owner()
    Bosco, Leo = create_pets()
    walk_bosco, feed_leo, chew_toy = create_tasks()

    # Assign tasks to the correct pets
    Bosco.add_task(walk_bosco)
    Bosco.add_task(chew_toy)
    Leo.add_task(feed_leo)

    # Add pets to owner
    Matt.add_pet(Bosco)
    Matt.add_pet(Leo)

    # Aggregate all pet tasks into owner.tasks so Scheduler can see them
    Matt.tasks = [task for pet in Matt.pets for task in pet.tasks]

    # Generate and print the organized schedule
    schedule = schedule_tasks(Matt)

    print(f"\n=== Daily Schedule for {Matt.name} ===")
    for pet_name, tasks in schedule.items():
        print(f"\n  {pet_name}:")
        for task in tasks:
            print(f"    [{task[1]}] {task[0]}")
