from Subsystem import *
from Task import *
import tkinter as tk
from tkinter import scrolledtext


class Resource:
    def __init__(self, name, total_units):
        self.name = name
        self.total_units = total_units
        self.available_units = total_units


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Scheduler Output")
        self.geometry("1500x800")
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill="both")

    def log_output(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)


def run_simulation(gui):
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

    # Main simulation loop
    for time in range(10):
        # Create a new file for the current time unit
        with open(f"./output/time_{time}.txt", "w") as time_file:
            time_file.write(f"Time: {time}\n\n")

            # Check for task arrivals for each subsystem and log them
            for task in tasks1:
                if time == task.arrival_time:
                    message = f"{task.name} arrived at time: {time}"
                    gui.log_output(message)  # Log to GUI
                    time_file.write(message + "\n")
                    subsystem1.add_task(task)
                    subsystem_files[1].write(message + "\n")

            for task in tasks2:
                if time == task.arrival_time:
                    message = f"{task.name} arrived at time: {time}"
                    gui.log_output(message)  # Log to GUI
                    time_file.write(message + "\n")
                    subsystem2.add_task(task)
                    subsystem_files[2].write(message + "\n")

            for task in tasks3:
                if time == task.arrival_time:
                    message = f"{task.name} arrived at time: {time}"
                    gui.log_output(message)  # Log to GUI
                    time_file.write(message + "\n")
                    subsystem3.add_task(task)
                    subsystem_files[3].write(message + "\n")

            for task in tasks4:
                if time == task.arrival_time:
                    message = f"{task.name} arrived at time: {time}"
                    gui.log_output(message)  # Log to GUI
                    time_file.write(message + "\n")
                    subsystem4.add_task(task)
                    subsystem_files[4].write(message + "\n")

            # Execute tasks in each subsystem
            subsystem1.execute()
            subsystem2.execute()
            subsystem3.execute()
            subsystem4.execute()

            # Log the status of each subsystem in the respective files
            subsystem_status = {
                1: subsystem1.get_status(),
                2: subsystem2.get_status(),
                3: subsystem3.get_status(),
                4: subsystem4.get_status(),
            }

            for i in range(1, 5):
                status_info = str(subsystem_status[i])
                gui.log_output(status_info)  # Log to GUI
                time_file.write(f"{status_info}\n")
                subsystem_files[i].write(f"Time: {time}\n{status_info}\n")

    # Close all subsystem log files
    for file in subsystem_files.values():
        file.close()


def main():
    gui = GUI()  # Create the GUI application instance
    gui.after(100, run_simulation, gui)  # Run the simulation after the GUI initializes
    gui.mainloop()


if __name__ == "__main__":
    main()
