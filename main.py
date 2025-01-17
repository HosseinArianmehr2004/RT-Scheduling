import heapq
from enum import Enum


class TaskState(Enum):
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
        self.state = TaskState.READY
        self.remaining_time = execution_time

    def __lt__(self, other):
        return self.priority < other.priority


class Resource:
    def __init__(self, name, total_units):
        self.name = name
        self.total_units = total_units
        self.available_units = total_units


class Core:
    def __init__(self, core_id):
        self.core_id = core_id
        self.current_task = None
        self.ready_queue = []

    def assign_task(self, task):
        if self.current_task is None:
            self.current_task = task
            task.state = TaskState.RUNNING
        else:
            heapq.heappush(self.ready_queue, task)
            task.state = TaskState.READY

    def execute(self):
        if self.current_task is not None:
            self.current_task.remaining_time -= 1
            if self.current_task.remaining_time == 0:
                self.current_task.state = TaskState.READY
                self.current_task = None
                if self.ready_queue:
                    next_task = heapq.heappop(self.ready_queue)
                    self.assign_task(next_task)


class Subsystem:
    def __init__(self, subsystem_id, num_cores, resources):
        self.subsystem_id = subsystem_id
        self.cores = [Core(i) for i in range(num_cores)]
        self.resources = resources
        self.waiting_queue = []

    def allocate_resources(self, task):
        for resource, needed in task.resources_needed.items():
            if self.resources[resource].available_units < needed:
                return False
        for resource, needed in task.resources_needed.items():
            self.resources[resource].available_units -= needed
        return True

    def release_resources(self, task):
        for resource, needed in task.resources_needed.items():
            self.resources[resource].available_units += needed

    def add_task(self, task):
        if self.allocate_resources(task):
            core = self.cores[0]  # Simple core selection, can be improved
            core.assign_task(task)
        else:
            self.waiting_queue.append(task)
            task.state = TaskState.WAITING

    def execute(self):
        for core in self.cores:
            core.execute()
        # Check waiting queue and try to assign tasks
        for task in self.waiting_queue[:]:
            if self.allocate_resources(task):
                core = self.cores[0]  # Simple core selection, can be improved
                core.assign_task(task)
                self.waiting_queue.remove(task)


def main():
    # Initialize resources
    resources = {"R1": Resource("R1", 10), "R2": Resource("R2", 10)}

    # Initialize subsystems
    subsystem1 = Subsystem(1, 3, resources)
    subsystem2 = Subsystem(2, 2, resources)
    subsystem3 = Subsystem(3, 1, resources)

    # Create some tasks
    tasks = [
        Task("T11", 4, {"R1": 1}, 0, 0, 1),
        Task("T12", 10, {"R2": 1}, 0, 0, 2),
        Task("T13", 20, {"R1": 2}, 0, 0, 3),
        Task("T21", 4, {"R1": 2, "R2": 3}, 5, 0, 1),
        Task("T31", 2, {"R1": 2, "R2": 3}, 10, 0, 1),
        Task("T41", 2, {"R1": 2, "R2": 3}, 5, 0, 1),
        Task("T42", 4, {"R1": 2, "R2": 2}, 7, 0, 2),
    ]

    # Assign tasks to subsystems
    subsystem1.add_task(tasks[0])
    subsystem1.add_task(tasks[1])
    subsystem1.add_task(tasks[2])
    subsystem2.add_task(tasks[3])
    subsystem3.add_task(tasks[4])
    subsystem3.add_task(tasks[5])
    subsystem3.add_task(tasks[6])

    # Simulate execution for 10 time units
    for time_unit in range(10):
        print(f"Time: {time_unit}")
        subsystem1.execute()
        subsystem2.execute()
        subsystem3.execute()


if __name__ == "__main__":
    main()
