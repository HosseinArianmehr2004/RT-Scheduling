from enum import Enum


class Task_State(Enum):
    READY = 1
    WAITING = 2
    RUNNING = 3


class Task:
    def __init__(
        self, name, execution_time, resources_needed, period, deadline, priority
    ):
        self.name = name
        self.execution_time = execution_time
        self.resources_needed = resources_needed
        self.period = period
        self.deadline = deadline
        self.priority = priority
        self.state = Task_State.READY
        self.remaining_time = execution_time

    # for sub 2
    def __init__(self, name, execution_time, resources_needed, arrival_time):
        self.name = name
        self.execution_time = execution_time
        self.resources_needed = resources_needed
        self.arrival_time = arrival_time

        self.state = Task_State.READY
        self.remaining_time = execution_time

    # for sub 2
    def __lt__(self, other):
        return self.remaining_time < other.remaining_time

    def __str__(self):
        return f"Task name: {self.name}, execution time: {self.execution_time}, remaining_time: {self.remaining_time}"
