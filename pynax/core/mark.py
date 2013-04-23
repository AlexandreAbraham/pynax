from . import UpdateMixin


class Mark(UpdateMixin):

    def __init__(self, value, display_options={}):
        self.value = value
        self.display_options = display_options

    def set_value(self, new_value):
        self.value = new_value
