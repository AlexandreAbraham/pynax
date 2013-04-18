class UpdateMixin:

    def subscribe(self, subscriber):
        if not hasattr(self, 'subscribers'):
            self.subscribers = set()
        self.subscribers.add(subscriber)

    def fire_update(self, value):
        if not hasattr(self, 'subscribers'):
            return
        for subscriber in self.subscribers:
            if hasattr(subscriber, 'on_update'):
                subscriber.on_update(value)
