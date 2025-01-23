import heapq
from Task import *
from Core import *


class Subsystem:
    def __init__(self, id, resources):
        self.id = id
        self.resources = resources
        self.ready_queue = []

        self.file = None
        self.time = None

    def get_status(self):
        status = f"Sub{self.id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += (
            f"        Waiting Queue {[task.name for task in self.waiting_queue]}\n"
        )
        for core in self.cores:
            status += f"        Core{core.id}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else '---'}"
            status += f", remaining time: {core.current_task.remaining_time if core.current_task else '-'}"
            status += f", remaining quantum: {core.current_task.remaining_quantum if core.current_task else '-'}\n"
            status += f"                Ready Queue: {[task.name for task in core.ready_queue]}\n"
        return status

    def allocate_resources(self, task):
        for resource, needed in task.resources_needed.items():
            if self.resources[resource].available_units < needed:
                return False
        for resource, needed in task.resources_needed.items():
            self.resources[resource].available_units -= needed
        task.has_all_resources = True
        return True

    def release_resources(self, task):
        for resource, needed in task.resources_needed.items():
            self.resources[resource].available_units += needed

    def execute(self):
        pass

    def set_file(self, file):
        self.file = file

    def set_time(self, time):
        self.time = time

    # def add_task(self, task):
    #     if self.allocate_resources(task):
    #         core = self.select_core()
    #         core.assign_task(task)
    #     else:
    #         self.waiting_queue.append(task)
    #         task.state = Task_State.WAITING

    def add_task(self, task):
        pass


class Subsystem_1(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.cores = [Core_1(i, self) for i in range(num_cores)]

    def load_balancing(self):
        # Identify underloaded and overloaded cores
        underloaded_cores = [
            core
            for core in self.cores
            if not core.ready_queue and core.current_task is None
        ]
        overloaded_cores = [core for core in self.cores if len(core.ready_queue) > 1]

        # Perform pull migration
        for underloaded_core in underloaded_cores:
            for overloaded_core in overloaded_cores:
                if overloaded_core.ready_queue:
                    # Transfer a task from the overloaded core to the underloaded core
                    task = (
                        overloaded_core.ready_queue.pop()
                    )  # Take the last task from the ready queue
                    underloaded_core.assign_task(task)
                    task.state = Task_State.READY  # Update the task state
                    self.file.write(
                        f"{task.name} migrated from Core {overloaded_core.id} to Core {underloaded_core.id}\n"
                    )
                    break  # Move to the next underloaded core after transferring one task

    def execute(self):
        for core in self.cores:
            core.execute()

        if self.time % 4 == 0:
            self.load_balancing()

        # Check waiting queue and try to assign tasks
        for task in self.waiting_queue[:]:
            if self.allocate_resources(task):
                core = self.select_core(task)
                core.assign_task(task)
                self.waiting_queue.remove(task)

    def add_task(self, task):
        if self.allocate_resources(task):
            core = self.select_core(task)
            core.assign_task(task)
        else:
            self.waiting_queue.append(task)
            task.state = Task_State.WAITING

    def select_core(self, task):
        return self.cores[task.destination_CPU_number - 1]


class Subsystem_2(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.cores = [Core_2(i, self) for i in range(num_cores)]

    def get_status(self):
        status = f"Sub{self.id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += f"        Ready Queue: {[task.name for task in self.ready_queue]}\n"
        for core in self.cores:
            status += f"        Core{core.id}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else '---'}"
            status += f", remaining time: {core.current_task.remaining_time if core.current_task else '-'}\n"
        return status

    def execute(self):
        for core in self.cores:
            core.execute()

    def add_task(self, task):
        # Add a task to the ready queue
        task.state = Task_State.READY
        heapq.heappush(self.ready_queue, task)

        # Assign task to core
        assigned = False
        for core in self.cores:
            if self.ready_queue:
                if core.current_task is None:
                    core.assign_task()
                    assigned = True
                    break
        if not assigned:
            for core in self.cores:
                if self.ready_queue:
                    if core.current_task.remaining_time > task.remaining_time:
                        core.assign_task()
                        break

        # Deadlock detection
        count = 0
        for core in self.cores:
            if core.current_task is not None:
                if not core.current_task.has_all_resources:
                    count += 1

        if count == 2:  # Deadlock has occurred.
            self.file.write(f"Deadlock has occurred !!!!!\n")

            # Deadlock resolution
            for task in self.ready_queue:
                self.release_resources(task)
                task.has_all_resources = False
                task.remaining_time = task.execution_time


class Subsystem_3(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.cores = [Core_3(i, self) for i in range(num_cores)]


class Subsystem_4(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.completed_tasks = []
        self.cores = [Core_4(i, self) for i in range(num_cores)]

    def get_status(self):
        status = f"Sub{self.id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += (
            f"        Waiting Queue: {[task.name for task in self.waiting_queue]}\n"
        )
        status += f"        Ready Queue: {[task.name for task in self.ready_queue]}\n"
        for core in self.cores:
            status += f"        Core{core.id}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else '---'}"
            status += f", remaining time: {core.current_task.remaining_time if core.current_task else '-'}\n"
        return status

    def execute(self):

        # Moving tasks from waiting queue to ready queue
        if self.waiting_queue:
            for _ in self.waiting_queue:
                task = self.waiting_queue.pop(0)
                for completed_task in self.completed_tasks:
                    if task.prerequisite_task_name == completed_task.name:
                        task.prerequisite = True
                        break
                if task.prerequisite:
                    if self.allocate_resources(task):
                        task.arrival_time = self.time
                        self.ready_queue.append(task)
                    else:
                        self.waiting_queue.append(task)
                else:
                    self.waiting_queue.append(task)

        # Assign task to core
        for core in self.cores:
            if self.ready_queue:
                if core.current_task is None:
                    core.assign_task()
                    break

        for core in self.cores:
            core.execute()

    def add_task(self, task):
        # For prerequisite tasks
        if task.prerequisite_task_name == "-":
            task.prerequisite = True
        else:
            for completed_task in self.completed_tasks:
                if task.prerequisite_task_name == completed_task.name:
                    task.prerequisite = True
                    break

        # Append to the waiting queue or ready queue
        if task.prerequisite:
            if self.allocate_resources(task):
                task.state = Task_State.READY
                self.ready_queue.append(task)
                self.file.write(f"Task [{task.name}] appended to ready queue !\n")
            else:
                task.state = Task_State.WAITING
                self.waiting_queue.append(task)
                self.file.write(f"Task [{task.name}] appended to waiting queue !\n")
        else:
            task.state = Task_State.WAITING
            self.waiting_queue.append(task)
            self.file.write(f"Task [{task.name}] appended to waiting queue !\n")
