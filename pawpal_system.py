#pawpal_system.py


class Tasks:
    def __init__(self, task_name, task_description, task_duration, task_frequency, task_priority, task_time_slot=None):
        self.task_name = task_name
        self.task_description = task_description
        self.task_duration = task_duration
        self.task_frequency = task_frequency
        self.task_time_slot = task_time_slot
        self.task_priority = task_priority
        self.mark_complete = False
    
    def description(self):
        """Returns the task name and description as a formatted string."""
        return f"Task name: {self.task_name}, Description: {self.task_description}"

    def duration(self):
        """Returns the task duration as a formatted string."""
        return f"Task Duration: {self.task_duration}"

    def frequency(self):
        """Returns how often the task recurs as a formatted string."""
        return f"Task Frequency: {self.task_frequency}"

    def priority(self):
        """Returns the task priority level as a formatted string."""
        return f"Task Priority: {self.task_priority}"

    def time_slot(self):
        """Returns the assigned time slot, or a message if none has been set."""
        if self.task_time_slot:
            return f"Task Time Slot: {self.task_time_slot}"
        return "No time slot assigned."

        

class Pets:
    def __init__(self, pet_name, pet_species):
        self.pet_name = pet_name
        self.pet_species = pet_species
        self.tasks = [] #Claude-recommended inclusion

    def pet_info(self):
        """Returns the pet's name and species as a formatted string."""
        return f"Pet name: {self.pet_name}, Species: {self.pet_species}"

    def add_task(self, tasks):
        """Appends a Tasks object to this pet's task list."""
        self.tasks.append(tasks)


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = [] #Claude-recommended inclusion
        self.tasks = [] #Claude-recommended inclusion


    def basic_info(self):
        """Returns the owner's name as a formatted string."""
        return f"Owner name: {self.name}"

    def owner_pets(self):
        """Returns the owner's list of pets as a formatted string."""
        return f'List of Pets: {self.pets}'

    def add_pet(self, pet):
        """Appends a Pets object to the owner's pet list."""
        self.pets.append(pet)

    def num_pet_tasks(self):
        """Returns the total number of tasks across all pets as a formatted string."""
        return f"Number of pet tasks: {len(self.tasks)}"


class Scheduler:  #THE BRAIN

    def __init__(self, owner): 
        self.owner = owner 
        self.pets = owner.pets
        self.tasks = owner.tasks

    
    def create_schedule(self):
        """Builds a schedule dict mapping each pet's name to a list of (task_name, time_slot) tuples."""
        schedule = {} #Keys are pets, values are lists of tasks with time slots

        #Let's check and see if task.time_slot is not None, and if so, we can directly assign it to the schedule. If it is None, we can use the priority and duration to determine where to place it in the schedule.

        #RECOMMENDED BY COPILOT: Helped generate this script to organize tasks from previous classes into the dictionary schedule created for this function.
         
        if self.pets and self.tasks:
            for pet in self.pets: #For list of pets Owner has...
                schedule[pet.pet_name] = [] #Creates an entry within the dictionary with pet name as the key and empty list as the value
                for task in self.tasks: #For each task in the list of every task the owner has
                    if task.task_time_slot: 
                        schedule[pet.pet_name].append((task.task_name, task.task_time_slot))
                    else: 
                        #For simplicity, let's just assign it to a default time slot based on priority. In a real implementation, you'd want a more sophisticated scheduling algorithm.
                        if task.task_priority == "high":
                            schedule[pet.pet_name].append((task.task_name, "Morning"))
                        elif task.task_priority == "medium":
                            schedule[pet.pet_name].append((task.task_name, "Afternoon"))
                        else:
                            schedule[pet.pet_name].append((task.task_name, "Evening"))
        else: 
            raise ValueError("Pets and/or Tasks were not included. Please include proper inputs")
        
        return schedule

    def organize_schedule(self, schedule):
        """Reorders each pet's task list so Morning tasks come first, then Afternoon, then Evening."""
        #With help of Claude --> Asked for method for organization based on time slot, gave this recommendation.
        for pet_name in schedule:
            list_of_tasks = schedule[pet_name]

            morning   = [task for task in list_of_tasks if task[1] == "Morning"]
            afternoon = [task for task in list_of_tasks if task[1] == "Afternoon"]
            evening   = [task for task in list_of_tasks if task[1] == "Evening"]

            schedule[pet_name] = morning + afternoon + evening

        return schedule
    
    def mark_complete(self, pet_name, task_name): #Automatically generated code from copilot
        """Finds the named task for the given pet and sets its mark_complete attribute to True."""
        for pet in self.pets:
            if pet.pet_name == pet_name:
                for task in pet.tasks:
                    if task.task_name == task_name:
                        task.mark_complete = True
                        return f"{task_name} for {pet_name} has been completed"
        return "Task or pet not found."
            
            


        



