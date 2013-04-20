class UpdateMixin:

    def subscribe(self, subscriber):
        if not hasattr(self, 'subscribers'):
            self.subscribers = set()
        if not subscriber in self.subscribers:
            self.subscribers.add(subscriber)

    def get_subscribers(self):
        if hasattr(self, 'subscribers'):
            return self.subscribers
        return set()
