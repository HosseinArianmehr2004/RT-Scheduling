from Subsystem import *
from Task import *
import threading

# For threads and locks
condition = threading.Condition()
current_thread = 1


class Resource:
    def __init__(self, name, total_units):
        self.name = name
        self.total_units = total_units
        self.available_units = total_units


def run_subsystem(subsystem, tasks, time_range, subsystem_file, thread_id):
    global current_thread
    for time in range(time_range):
        with condition:
            # Waiting for this thread to come to its turn
            while current_thread != thread_id:
                condition.wait()

            # Create a new file for the current time unit
            with open(f"./output/time_{time}.txt", "a") as time_file:
                time_file.write(f"Time: {time}\n")
                subsystem_file.write(f"Time: {time}\n")
                subsystem.set_time(time)

                # Check for task arrivals for each subsystem and log them
                for task in tasks:
                    if time == task.arrival_time:
                        time_file.write(f"Task [{task.name}] arrived !\n")
                        subsystem_file.write(f"Task [{task.name}] arrived !\n")
                        subsystem.add_task(task)

                # Execute tasks in each subsystem
                subsystem.execute()

                # Log the status of each subsystem in the respective files
                status_info = str(subsystem.get_status())
                time_file.write(f"{status_info}\n")
                subsystem_file.write(f"{status_info}\n")

            # Increment the current thread number and notify other threads
            current_thread += 1
            if current_thread > 4:
                current_thread = 1
            condition.notify_all()

    if subsystem.id == "Subsystem 3":
        subsystem.drawGantt()


def main():
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
    subsystem1 = Subsystem_1(
        "Subsystem 1",
        3,
        {
            "R1": Resource("R1", int(resources[0])),
            "R2": Resource("R2", int(resources[1])),
        },
    )
    subsystem2 = Subsystem_2(
        "Subsystem 2",
        2,
        {
            "R1": Resource("R1", int(resources[2])),
            "R2": Resource("R2", int(resources[3])),
        },
    )
    subsystem3 = Subsystem_3(
        "Subsystem 3",
        1,
        {
            "R1": Resource("R1", int(resources[4])),
            "R2": Resource("R2", int(resources[5])),
        },
    )
    subsystem4 = Subsystem_4(
        "Subsystem 4",
        2,
        {
            "R1": Resource("R1", int(resources[6])),
            "R2": Resource("R2", int(resources[7])),
        },
    )

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
                        int(line[6]),
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
    for task in task3:
        tasks3.append(
            Task(
                name=task[0],
                execution_time=task[1],
                resources_needed={"R1": task[2], "R2": task[3]},
                arrival_time=task[4],
                destination_CPU_number=None,
                period=task[5],
                number_of_repeat_times=task[6],
                prerequisite_task_name=None,
            )
        )
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

    subsystem_files = {
        1: open(f"./output/subsystem1_log.txt", "w"),
        2: open(f"./output/subsystem2_log.txt", "w"),
        3: open(f"./output/subsystem3_log.txt", "w"),
        4: open(f"./output/subsystem4_log.txt", "w"),
    }

    subsystem1.set_file(subsystem_files[1])
    subsystem2.set_file(subsystem_files[2])
    subsystem3.set_file(subsystem_files[3])
    subsystem4.set_file(subsystem_files[4])

    time_range = 20
    
    for time in range(time_range):
        with open(f"./output/time_{time}.txt", "w"):
            pass

    # Create threads for each subsystem
    threads = []
    threads.append(
        threading.Thread(
            target=run_subsystem, args=(subsystem1, tasks1, time_range, subsystem_files[1], 1)
        )
    )
    threads.append(
        threading.Thread(
            target=run_subsystem, args=(subsystem2, tasks2, time_range, subsystem_files[2], 2)
        )
    )
    threads.append(
        threading.Thread(
            target=run_subsystem, args=(subsystem3, tasks3, time_range, subsystem_files[3], 3)
        )
    )
    threads.append(
        threading.Thread(
            target=run_subsystem, args=(subsystem4, tasks4, time_range, subsystem_files[4], 4)
        )
    )

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Close all subsystem log files
    for file in subsystem_files.values():
        file.close()


if __name__ == "__main__":
    main()
