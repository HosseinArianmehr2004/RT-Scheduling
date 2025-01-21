class WeightedRoundRobin:
    def __init__(self, servers):
        self.servers = servers
        self.max_weight = max(weight for _, weight in servers)
        self.current_index = -1
        self.current_weight = 0

    def get_next_server(self):
        while True:
            self.current_index = (self.current_index + 1) % len(self.servers)
            if self.current_index == 0:
                self.current_weight = self.current_weight - 1
                if self.current_weight <= 0:
                    self.current_weight = self.max_weight
            server, weight = self.servers[self.current_index]
            if weight >= self.current_weight:
                return server

# مثال استفاده
servers = [("Server A", 3), ("Server B", 2), ("Server C", 1)]
wrr = WeightedRoundRobin(servers)

# درخواست‌ها را به صورت چرخشی با وزن توزیع می‌کنیم
for _ in range(10):
    print(wrr.get_next_server())