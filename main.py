from Subsystem import *
from Task import *


class Resource:
    def __init__(self, name, total_units):
        self.name = name
        self.total_units = total_units
        self.available_units = total_units


def main():
    # Initialize all resources
    all_resources = {
        "R1": Resource("R1", 10),
        "R2": Resource("R2", 10),
        "Core": Resource("Core", 0),
    }

    # Reading information from the file
    filename = "in.txt"
    lines = []
    with open(filename, "r") as file:
        lines = file.readlines()

    # Getting the number of subsystem resources from file
    resources = []
    for line in lines[:4]:
        split_values = line.split()
        resources.extend(split_values)

    # Initialize subsystems
    # subsystem1 = Subsystem_1(int(resources[0]), int(resources[1]), all_resources)
    subsystem2 = Subsystem_2(int(resources[2]), int(resources[3]), all_resources)
    # subsystem3 = Subsystem_3(int(resources[4]), int(resources[5]), all_resources)
    # subsystem4 = Subsystem_4(int(resources[6]), int(resources[7]), all_resources)

    # Getting tasks from the file
    count = 0
    line_index = 4
    task1 = []
    task2 = []
    task3 = []
    task4 = []
    while count < 4:
        line = lines[line_index].split()
        if line[0] == "$":
            count += 1
        else:
            if count == 0:
                task1.append(
                    [
                        line[0],
                        int(line[1]),
                        int(line[2]),
                        int(line[3]),
                        int(line[4]),
                        int(line[5]),
                    ]
                )
            elif count == 1:
                task2.append(
                    [
                        line[0],
                        int(line[1]),
                        int(line[2]),
                        int(line[3]),
                        int(line[4]),
                    ]
                )
            elif count == 2:
                task3.append(
                    [
                        line[0],
                        int(line[1]),
                        int(line[2]),
                        int(line[3]),
                        int(line[4]),
                        int(line[5]),
                    ]
                )
            elif count == 3:
                task4.append(
                    [
                        line[0],
                        int(line[1]),
                        int(line[2]),
                        int(line[3]),
                        int(line[4]),
                        line[5],
                    ]
                )
        line_index += 1

    # Create tasks
    tasks1 = []
    tasks2 = []
    tasks3 = []
    tasks4 = []
    for task in task1:
        tasks1.append(
            Task(
                name=task[0],
                execution_time=task[1],
                resources_needed={"R1": task[2], "R2": task[3]},
                arrival_time=task[4],
                destination_CPU_number=task[5],
                period=None,
                number_of_repeat_times=None,
                prerequisite_task_name=None,
            )
        )
    for task in task2:
        tasks2.append(
            Task(
                name=task[0],
                execution_time=task[1],
                resources_needed={"R1": task[2], "R2": task[3]},
                arrival_time=task[4],
                destination_CPU_number=None,
                period=None,
                number_of_repeat_times=None,
                prerequisite_task_name=None,
            )
        )
    # for task in task3:
    #     tasks3.append(
    #         Task(
    #             name=task[0],
    #             execution_time=task[1],
    #             resources_needed={"R1": task[2], "R2": task[3]},
    #             arrival_time=task[4],
    #             destination_CPU_number=None,
    #             period=task[5],
    #             number_of_repeat_times=task[5],
    #             prerequisite_task_name=None,
    #         )
    #     )
    for task in task4:
        tasks4.append(
            Task(
                name=task[0],
                execution_time=task[1],
                resources_needed={"R1": task[2], "R2": task[3]},
                arrival_time=task[4],
                destination_CPU_number=None,
                period=None,
                number_of_repeat_times=None,
                prerequisite_task_name=task[5],
            )
        )

    for time in range(10):
        for task in tasks2:
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
