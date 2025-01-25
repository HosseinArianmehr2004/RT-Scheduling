from Subsystem import *
from Task import *
import threading


class Resource:
    def __init__(self, name, total_units):
        self.name = name
        self.total_units = total_units
        self.available_units = total_units

    def __str__(self):
        return f"{self.name}, available units: {self.available_units}"

    def __repr__(self):
        return f"[{self.name}, available units: {self.available_units}]"


class MainSystem:
    def __init__(self, total_time):
        self.time = 0
        self.total_time = total_time
        self.condition = threading.Condition()

    # def run(self):
    #     for self.time in range(self.total_time):
    #         with self.condition:
    #             print(f"Main System Time: {self.time}")
    #             self.condition.notify_all()  # Notify all subsystems

    def run(self):
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
            "Subsystem_1",
            3,
            {
                "R1": Resource("R1", int(resources[0])),
                "R2": Resource("R2", int(resources[1])),
            },
            self,
        )
        subsystem2 = Subsystem_2(
            "Subsystem_2",
            2,
            {
                "R1": Resource("R1", int(resources[2])),
                "R2": Resource("R2", int(resources[3])),
            },
            self,
        )
        subsystem3 = Subsystem_3(
            "Subsystem_3",
            1,
            {
                "R1": Resource("R1", int(resources[4])),
                "R2": Resource("R2", int(resources[5])),
            },
            self,
        )
        subsystem4 = Subsystem_4(
            "Subsystem_4",
            2,
            {
                "R1": Resource("R1", int(resources[6])),
                "R2": Resource("R2", int(resources[7])),
            },
            self,
        )

        subsystem1.start()
        subsystem2.start()
        subsystem3.start()
        subsystem4.start()

        subsystem3.set_subsystems([subsystem1, subsystem4])

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

        for i in range(1, 5):
            with open(f"./output/subsystem{i}_log.txt", "w"):
                pass
        subsystem_files = {
            1: open(f"./output/subsystem1_log.txt", "a"),
            2: open(f"./output/subsystem2_log.txt", "a"),
            3: open(f"./output/subsystem3_log.txt", "a"),
            4: open(f"./output/subsystem4_log.txt", "a"),
        }

        subsystem1.set_file(subsystem_files[1])
        subsystem2.set_file(subsystem_files[2])
        subsystem3.set_file(subsystem_files[3])
        subsystem4.set_file(subsystem_files[4])

        for self.time in range(self.total_time + 1):
            with self.condition:
                print(f"Main System Time: {self.time}")

                # Create a new file for the current time unit
                with open(f"./output/time_{self.time}.txt", "w") as time_file:
                    time_file.write(f"Time: {self.time}\n\n")
                    subsystem_files[1].write(f"Time: {self.time}\n")
                    subsystem_files[2].write(f"Time: {self.time}\n")
                    subsystem_files[3].write(f"Time: {self.time}\n")
                    subsystem_files[4].write(f"Time: {self.time}\n")

                    subsystem1.set_time(self.time)
                    subsystem2.set_time(self.time)
                    subsystem3.set_time(self.time)
                    subsystem4.set_time(self.time)

                    # Check for task arrivals for each subsystem and log them
                    for task in tasks1:
                        if self.time == task.arrival_time:
                            time_file.write(f"Task [{task.name}] arrived !\n")
                            subsystem_files[1].write(f"Task [{task.name}] arrived !\n")
                            subsystem1.add_task(task)
                    for task in tasks2:
                        if self.time == task.arrival_time:
                            time_file.write(f"Task [{task.name}] arrived !\n")
                            subsystem_files[2].write(f"Task [{task.name}] arrived !\n")
                            subsystem2.add_task(task)
                    for task in tasks3:
                        if self.time == task.arrival_time:
                            time_file.write(f"Task [{task.name}] arrived !\n")
                            subsystem_files[3].write(f"Task [{task.name}] arrived !\n")
                            subsystem3.add_task(task)
                    for task in tasks4:
                        if self.time == task.arrival_time:
                            time_file.write(f"Task [{task.name}] arrived !\n")
                            subsystem_files[4].write(f"Task [{task.name}] arrived !\n")
                            subsystem4.add_task(task)

                    # # Execute tasks in each subsystem
                    # subsystem1.execute()
                    # subsystem2.execute()
                    # subsystem3.execute()
                    # subsystem4.execute()
                    self.condition.notify_all()  # Notify all subsystems
                    self.condition.wait(0.01)  # Wait for a maximum of 1 second

                    # Log the status of each subsystem in the respective files
                    subsystem_status = {
                        1: subsystem1.get_status(),
                        2: subsystem2.get_status(),
                        3: subsystem3.get_status(),
                        4: subsystem4.get_status(),
                    }

                    for i in range(1, 5):
                        status_info = str(subsystem_status[i])
                        time_file.write(f"{status_info}\n")
                        subsystem_files[i].write(f"{status_info}\n")

            # TTT.sleep(0.1)  # Simulate time passing

        subsystem1.draw_gantt_chart()
        subsystem2.draw_gantt_chart()
        subsystem3.draw_gantt_chart()
        subsystem4.draw_gantt_chart()

        # Close all subsystem log files
        for file in subsystem_files.values():
            file.close()

        # Writing to the file out.txt
        with open("out.txt", "w") as out_file:
            for time in range(self.total_time):
                with open(f"./output/time_{time}.txt", "r") as time_file:
                    content = time_file.read()
                    out_file.write(content)

        # Final report
        with open(f"./output/final_report.txt", "w"):
            pass
        with open(f"./output/final_report.txt", "a") as final_report_file:
            for task in tasks1:
                final_report_file.write(f"Task [{task.name}] :\n")
                final_report_file.write(
                    f"        Start of execution time is : [{task.start_execution_time}]\n"
                )
                final_report_file.write(
                    f"        Finish of execution time is : [{task.finish_execution_time}]\n"
                )
                final_report_file.write(
                    f"        Time spent in the waiting queue is : [{task.waiting_time}]\n"
                )
                final_report_file.write(
                    f"        The subsystem that executed the task is : [Subsystem 1]\n"
                )
                final_report_file.write(
                    f"        Cores that executed the task are : {task.execution_cores}\n\n"
                )
            for task in tasks2:
                final_report_file.write(f"Task [{task.name}] :\n")
                final_report_file.write(
                    f"        Start of execution time is : [{task.start_execution_time}]\n"
                )
                final_report_file.write(
                    f"        Finish of execution time is : [{task.finish_execution_time}]\n"
                )
                final_report_file.write(
                    f"        Time spent in the waiting queue is : [0]\n"
                )
                final_report_file.write(
                    f"        The subsystem that executed the task is : [Subsystem 2]\n"
                )
                final_report_file.write(
                    f"        Cores that executed the task are : {task.execution_cores}\n\n"
                )
            for task in tasks3:
                final_report_file.write(f"Task [{task.name}] :\n")
                final_report_file.write(
                    f"        Start of execution time is : [{task.start_execution_time}]\n"
                )
                final_report_file.write(
                    f"        Finish of execution time is : [{task.finish_execution_time}]\n"
                )
                final_report_file.write(
                    f"        Time spent in the waiting queue is : [{task.waiting_time}]\n"
                )
                final_report_file.write(
                    f"        The subsystem that executed the task is : [Subsystem 3]\n"
                )
                final_report_file.write(
                    f"        Cores that executed the task are : {task.execution_cores}\n\n"
                )
            for task in tasks4:
                final_report_file.write(f"Task [{task.name}] :\n")
                final_report_file.write(
                    f"        Start of execution time is : [{task.start_execution_time}]\n"
                )
                final_report_file.write(
                    f"        Finish of execution time is : [{task.finish_execution_time}]\n"
                )
                final_report_file.write(
                    f"        Time spent in the waiting queue is : [{task.waiting_time}]\n"
                )
                final_report_file.write(
                    f"        The subsystem that executed the task is : [Subsystem 4]\n"
                )
                final_report_file.write(
                    f"        Cores that executed the task are : {task.execution_cores}\n\n"
                )

        subsystem1.join()
        subsystem2.join()
        subsystem3.join()
        subsystem4.join()


if __name__ == "__main__":
    total_time = 19
    main_system = MainSystem(total_time)

    main_system.run()
