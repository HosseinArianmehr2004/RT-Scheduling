from Subsystem import *
from Task import *


class Resource:
    def __init__(self, name, total_units):
        self.name = name
        self.total_units = total_units
        self.available_units = total_units


def main():
    # Initialize resources
    resources = {"R1": Resource("R1", 10), "R2": Resource("R2", 10)}

    # Initialize subsystems
    # subsystem1 = Subsystem(1, 3, resources)
    subsystem2 = Subsystem_2(2, 2, resources)
    # subsystem3 = Subsystem(3, 1, resources)
    # subsystem4 = Subsystem(4, 2, resources)

    # Create some tasks
    # tasks = [
    #     Task("T11", 4, {"R1": 1}, 0, 0, 1),
    #     Task("T12", 10, {"R2": 1}, 0, 0, 2),
    #     Task("T13", 20, {"R1": 2}, 0, 0, 3),
    #     Task("T21", 4, {"R1": 2, "R2": 3}, 5, 0, 1),
    #     Task("T31", 2, {"R1": 2, "R2": 3}, 10, 0, 1),
    #     Task("T41", 2, {"R1": 2, "R2": 3}, 5, 0, 1),
    #     Task("T42", 4, {"R1": 2, "R2": 2}, 7, 0, 2),
    # ]

    tasks = [
        Task("T1", 4, {"R1": 1}, 0),
        Task("T2", 6, {"R2": 1}, 1),
        Task("T3", 8, {"R1": 2}, 1),
        Task("T4", 3, {"R1": 2, "R2": 3}, 2),
    ]

    for time in range(10):
        for task in tasks:
            if time == task.arrival_time:
                print(f"task name = {task.name} arrived at time: {time}")
                subsystem2.add_task(task)
                # tasks.remove(task)

        subsystem2.execute()
        print(subsystem2.get_status(time))
        for t in subsystem2.ready_queue:
            print(
                f"Task name: {t.name}, execution time: {t.execution_time}, remaining_time: {t.remaining_time}"
            )
        print()


if __name__ == "__main__":
    main()
