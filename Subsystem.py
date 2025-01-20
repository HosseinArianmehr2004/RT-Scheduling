import heapq
from Task import *


# for sub 1 and 3
# class Core:
#     def __init__(self, core_id, ready_queue):
#         self.core_id = core_id
#         self.current_task = None
#         # self.ready_queue = []
#         self.ready_queue = ready_queue

#     def assign_task(self, task):
#         if self.current_task is None:
#             self.current_task = task
#             task.state = Task_State.RUNNING
#         else:
#             heapq.heappush(self.ready_queue, task)
#             task.state = Task_State.READY

#     def execute(self):
#         if self.current_task is not None:
#             self.current_task.remaining_time -= 1
#             if self.current_task.remaining_time == 0:
#                 self.current_task.state = Task_State.READY
#                 self.current_task = None
#                 if self.ready_queue:
#                     next_task = heapq.heappop(self.ready_queue)
#                     self.assign_task(next_task)


# for sub 2
class Core:
    def __init__(self, core_id, ready_queue):
        self.core_id = core_id
        self.current_task = None
        # self.ready_queue = []
        self.ready_queue = ready_queue

    def assign_task(self):
        if self.current_task is None:
            self.current_task = heapq.heappop(self.ready_queue)
            self.current_task.state = Task_State.RUNNING
        else:
            print(f"Task {self.current_task.name} preemped")
            self.current_task.state = Task_State.READY
            heapq.heappush(self.ready_queue, self.current_task)
            self.current_task = heapq.heappop(self.ready_queue)
            self.current_task.state = Task_State.RUNNING
            print(f"Task {self.current_task.name} assigned to CPU")

    def execute(self):
        if self.current_task is not None:
            self.current_task.remaining_time -= 1
            if self.current_task.remaining_time == 0:
                self.current_task.state = Task_State.READY
                self.current_task = None
                if len(self.ready_queue) > 0:
                    self.assign_task()


class Subsystem:
    def __init__(self, subsystem_id, num_cores, resources):
        self.subsystem_id = subsystem_id
        self.resources = resources
        self.ready_queue = []
        # self.waiting_queue = []
        self.cores = [Core(i, self.ready_queue) for i in range(num_cores)]

    def release_resources(self, task):
        for resource, needed in task.resources_needed.items():
            self.resources[resource].available_units += needed

    def get_status(self, time):
        status = f"Time: {time}\n"
        status = f"Sub{self.subsystem_id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += (
            f"        Waiting Queue {[task.name for task in self.waiting_queue]}\n"
        )
        for core in self.cores:
            status += f"        Core{core.core_id + 1}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else 'idle'}\n"
            status += f"                Ready Queue: {[task.name for task in core.ready_queue]}\n"
        return status

    def allocate_resources(self, task):
        for resource, needed in task.resources_needed.items():
            if self.resources[resource].available_units < needed:
                return False
        for resource, needed in task.resources_needed.items():
            self.resources[resource].available_units -= needed
        return True

    def execute(self):
        for core in self.cores:
            core.execute()
        # Check waiting queue and try to assign tasks
        for task in self.waiting_queue[:]:
            if self.allocate_resources(task):
                core = self.select_core()
                core.assign_task(task)
                self.waiting_queue.remove(task)

    def add_task(self, task):
        if self.allocate_resources(task):
            core = self.select_core()
            core.assign_task(task)
        else:
            self.waiting_queue.append(task)
            task.state = Task_State.WAITING

    def select_core(self):
        return self.cores[0]  # Simple core selection, can be improved


class Subsystem_2(Subsystem):
    def get_status(self, time):
        status = f"Time: {time}\n"
        status += f"Sub{self.subsystem_id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += f"        Ready Queue: {[task.name for task in self.ready_queue]}\n"
        for core in self.cores:
            status += f"        Core{core.core_id + 1}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else 'idle'}"
            status += f", remaining time: {core.current_task.remaining_time if core.current_task else '-'}\n"
        return status

    def execute(self):
        for core in self.cores:
            core.execute()

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
