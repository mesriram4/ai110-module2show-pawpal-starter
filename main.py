
from sched import scheduler

from pawpal_system import Tasks, Pets, Owner, Scheduler 

#Add Owner 

def create_owner(): 
    Matt = Owner("Matt")
    print(f'Information about Owner: {Matt.basic_info()}')
    print(f'Pets: {Matt.owner_pets()}')
    print(f'Number of pet tasks: {Matt.num_pet_tasks()}')
    return Matt

def create_pets(): 
    Bosco = Pets("Bosco", "Dog")
    Leo = Pets("Leo", "Fish")
    print(f'Information about Bosco: {Bosco.pet_info()}')
    print(f'Tasks for Bosco: {Bosco.tasks}')
    print(f'Information about Leo: {Leo.pet_info()}')
    print(f'Tasks for Leo: {Leo.tasks}')
    return Bosco, Leo
    
def create_tasks(): 
    walk_bosco = Tasks("Walk Bosco", "Walk around park", "1.5 hours", "Daily", "High", "Morning")
    feed_leo = Tasks("Feed Leo", "Give Leo 3 fish flakes", "5 minutes", "Daily", "Medium", "Afternoon")
    chew_toy = Tasks("Chew Toy", "Give Bosco a new chew toy", "10 minutes", "Monthly", "Low")
    return walk_bosco, feed_leo, chew_toy

def schedule_tasks(owner): 
    scheduler = Scheduler(owner)
    raw_schedule = scheduler.create_schedule()
    filtered_schedule = scheduler.filter_tasks(raw_schedule)
    return scheduler.organize_schedule(filtered_schedule)

def mark_complete(scheduler, pet_name, task_name): 
    result = scheduler.mark_complete(pet_name, task_name)
    return result


if __name__ == "__main__":
    Matt = create_owner()
    Bosco, Leo = create_pets() 
    walk_bosco, feed_leo, chew_toy = create_tasks()

    Bosco.add_task(walk_bosco) 
    Bosco.add_task(chew_toy)
    Leo.add_task(feed_leo)

    Matt.add_pet(Bosco) 
    Matt.add_pet(Leo)

    Matt.tasks = [task for pet in Matt.pets for task in pet.tasks] #Claude-recommended inclusion to aggregate all tasks at owner level

    schedule = schedule_tasks(Matt)

    print(f"\n=== Daily Schedule for {Matt.name} ===") #Claude-recommended script. 
    for pet_name, tasks in schedule.items():
        print(f"\n  {pet_name}:")
        for task in tasks:
            print(f"    [{task[1]}] {task[0]}")
    
    result = mark_complete(schedule, "Bosco", "Walk Bosco")
    print(result)
