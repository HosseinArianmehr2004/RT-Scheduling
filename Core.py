import heapq
from Task import *


class Core:
    def __init__(self, core_id):
        self.core_id = core_id
        self.current_task = None

    def assign_task(self, task):
        if self.current_task is None:
            self.current_task = task
            task.state = Task_State.RUNNING
        else:
            heapq.heappush(self.ready_queue, task)
            task.state = Task_State.READY

    def execute(self):
        if self.current_task is not None:
            self.current_task.remaining_time -= 1
            if self.current_task.remaining_time == 0:
                self.current_task.state = Task_State.READY
                self.current_task = None
                if self.ready_queue:
                    next_task = heapq.heappop(self.ready_queue)
                    self.assign_task(next_task)


class Core_1(Core):
    def __init__(self, core_id):
        super().__init__(core_id)
        self.ready_queue = []


class Core_2(Core):
    def __init__(self, core_id, ready_queue):
        super().__init__(core_id)
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


class Core_3(Core):
    def __init__(self, core_id):
        super().__init__(core_id)
        self.ready_queue = []


class Core_4(Core):
    def __init__(self, core_id, ready_queue):
        super().__init__(core_id)
        self.ready_queue = ready_queue
