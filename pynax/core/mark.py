from . import UpdateMixin


class Mark(UpdateMixin):

    def __init__(self, value, display_options={}):
        self.value = value
        self.display_options = display_options

    def update_value(self, new_value):
        if self.value == new_value:
            return
        self.value = new_value
        self.fire_update(self)
