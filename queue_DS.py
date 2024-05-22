class history_queue:
    def __init__(self):
        self.queue = list()

    def modify(self, add):
        if add not in self.queue:
            if len(self.queue) < 20:
                self.queue.insert(0, add)
            else:
                self.queue.insert(0, add)
                self.queue.pop()