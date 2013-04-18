class UpdateMixin:

    def subscribe(self, subscriber):
        if not hasattr(self, 'subscribers'):
            self.subscribers = []
        if not subscriber in self.subscribers:
            self.subscribers.append(subscriber)

    def fire_update(self, value):
        if not hasattr(self, 'subscribers'):
            return
        for subscriber in self.subscribers:
            if hasattr(subscriber, 'on_update'):
                subscriber.on_update(value)
