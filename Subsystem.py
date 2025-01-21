import heapq
from Task import *
from Core import *


class Subsystem:
    def __init__(self, id, resources):
        self.id = id
        self.resources = resources
        self.ready_queue = []

    def get_status(self):
        status = f"Sub{self.id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += (
            f"        Waiting Queue {[task.name for task in self.waiting_queue]}\n"
        )
        for core in self.cores:
            status += f"        Core{core.core_id + 1}:\n"
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
        return True

    def release_resources(self, task):
        for resource, needed in task.resources_needed.items():
            self.resources[resource].available_units += needed

    def execute(self, time):
        pass

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

    def execute(self, time):
        for core in self.cores:
            core.execute(time)

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
        self.waiting_queue = []
        self.cores = [Core_2(i, self) for i in range(num_cores)]

    def get_status(self):
        status = f"Sub{self.id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += f"        Ready Queue: {[task.name for task in self.ready_queue]}\n"
        for core in self.cores:
            status += f"        Core{core.core_id + 1}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else 'idle'}"
            status += f", remaining time: {core.current_task.remaining_time if core.current_task else '-'}\n"
        return status

    def execute(self, time):
        for core in self.cores:
            core.execute(time)

    def add_task(self, task):
        task.state = Task_State.READY
        heapq.heappush(self.ready_queue, task)

        for core in self.cores:
            # if core.current_task is None and len(self.ready_queue) > 0:
            if len(self.ready_queue) > 0:
                if (
                    core.current_task is None
                    or core.current_task.remaining_time > task.execution_time
                ):
                    core.assign_task()


class Subsystem_3(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.cores = [Core_3(i, self) for i in range(num_cores)]


class Subsystem_4(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.cores = [Core_4(i, self) for i in range(num_cores)]
