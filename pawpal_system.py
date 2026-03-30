#pawpal_system.py


class User:
    def __init__(self, name, num_pets,morning_time, afternoon_time, evening_time):
        self.name = name
        self.num_pets = num_pets
        self.morning_time = morning_time
        self.afternoon_time = afternoon_time
        self.evening_time = evening_time

    def basic_info(self):
        pass

    def availability(self):
        pass

    def owner_pet_overlap(self):
        pass


class Pets:
    def __init__(self, pet_name, pet_species, pet_eating_time, pet_walking_time):
        self.pet_name = pet_name
        self.pet_species = pet_species
        self.pet_eating_time = pet_eating_time
        self.pet_walking_time = pet_walking_time

    def pet_info(self):
        pass

    def pet_time_preferences(self):
        pass


class Tasks:
    def __init__(self, task_name, task_duration, task_priority):
        self.task_name = task_name
        self.task_duration = task_duration
        self.task_priority = task_priority

    def task_grouping(self):
        pass

    def organize_to_do_list(self):
        pass

