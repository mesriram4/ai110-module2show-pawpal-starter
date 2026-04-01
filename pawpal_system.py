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
        return {pet.pet_name: len(pet.tasks) for pet in self.pets}


class Scheduler:  #THE BRAIN

    def __init__(self, owner): 
        self.owner = owner 
        self.pets = owner.pets
        self.tasks = owner.tasks

    
    def create_schedule(self):
        """Builds a schedule dict mapping each pet's name to a list of (task_name, time_slot) tuples.

        Tasks with a time slot already set use it directly. Tasks without one are
        assigned a default slot based on priority: High -> Morning, Medium -> Afternoon,
        Low -> Evening. Completed tasks are excluded.

        Returns:
            dict: { pet_name: [(task_name, time_slot), ...] }

        Raises:
            ValueError: If the owner has no pets or no tasks assigned.
        """
        # Guard: require at least one pet and one task before building the schedule
        if not self.pets or not self.tasks:
            raise ValueError("Pets and/or Tasks were not included. Please include proper inputs")

        schedule = {}
        for pet in self.pets:
            pet_entries = []  # collect this pet's scheduled tasks before adding to schedule

            for task in pet.tasks:
                if not task.mark_complete:
                    continue  # only schedule completed tasks

                # Use the task's assigned time slot, or fall back to priority-based default
                if task.task_time_slot:
                    time_slot = task.task_time_slot
                elif task.task_priority == "high":
                    time_slot = "Morning"
                elif task.task_priority == "medium":
                    time_slot = "Afternoon"
                else:
                    time_slot = "Evening"

                pet_entries.append((task.task_name, time_slot))

            schedule[pet.pet_name] = pet_entries

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


    def organize_schedule(self, schedule, filter_pet=None, completed=None): #Asked Claude Agent to simplify code for human readability, returned this formatted method. 
        """Filters and sorts each pet's task list in the schedule.

        Optionally narrows results by pet name and/or completion status,
        then sorts remaining tasks Morning -> Afternoon -> Evening.

        Args:
            schedule (dict): Output of create_schedule() — maps pet name to
                             a list of (task_name, time_slot) tuples.
            filter_pet (str, optional): If given, only include this pet in the result.
            completed (bool, optional): True = completed tasks only,
                                        False = incomplete tasks only,
                                        None = all tasks (default).

        Returns:
            dict: Filtered and sorted schedule in the same format as the input.
        """
        TIME_ORDER = {"Morning": 0, "Afternoon": 1, "Evening": 2}

        # Step 1: Build a lookup so we can check each task's completion status by name.
        # Structure: { "Bosco": { "Walk Bosco": <task object>, ... }, "Leo": { ... } }
        task_lookup = {}
        for pet in self.pets:
            task_lookup[pet.pet_name] = {task.task_name: task for task in pet.tasks}

        # Step 2: Walk through the schedule, apply filters, then sort each pet's entries.
        filtered_schedule = {}
        for pet_name, entries in schedule.items():

            # Skip this pet if a specific pet was requested and it doesn't match
            if filter_pet is not None and pet_name != filter_pet:
                continue

            # Remove entries that don't match the requested completion status
            if completed is not None:
                entries = [
                    entry for entry in entries
                    if task_lookup.get(pet_name, {}).get(entry[0]) is not None
                    and task_lookup[pet_name][entry[0]].mark_complete == completed
                ]

            # Sort remaining entries Morning -> Afternoon -> Evening
            filtered_schedule[pet_name] = sorted(entries, key=lambda t: TIME_ORDER.get(t[1], 3))

        return filtered_schedule


            
            


        



