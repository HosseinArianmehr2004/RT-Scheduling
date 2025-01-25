from enum import Enum


class Task_State(Enum):
    READY = 1
    WAITING = 2
    RUNNING = 3
    COMPLETED = 4


class Task:
    def __init__(
        self,
        name,
        execution_time,
        resources_needed,
        arrival_time,
        destination_CPU_number,
        period,
        number_of_repeat_times,
        prerequisite_task_name,
    ):
        self.name = name
        self.execution_time = execution_time
        self.resources_needed = resources_needed
        self.arrival_time = arrival_time

        self.destination_CPU_number = destination_CPU_number

        self.period = period
        self.backup_period = period

        self.number_of_repeat_times = number_of_repeat_times
        self.prerequisite_task_name = prerequisite_task_name

        self.state = Task_State.READY
        self.remaining_time = execution_time

        self.has_all_resources = False
        self.has_Ri = {"R1": False, "R2": False}

        self.remaining_quantum = 0
        self.prerequisite = False

        # For final report
        self.start_execution_time = None
        self.start_time_bool = False
        self.finish_execution_time = None
        self.waiting_time = 0
        self.waiting_time = 0
        self.execution_cores = []

    # For sub 2
    def __lt__(self, other):
        return self.remaining_time < other.remaining_time

    def __str__(self):
        return f"{self.name}, execution time: {self.execution_time}, remaining_time: {self.remaining_time}"

    def __repr__(self):
        return f"[{self.name}, execution time: {self.execution_time}, remaining_time: {self.remaining_time}]"
