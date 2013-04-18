class Refresher:

    def __init__(self, figure, mark_list):
        self.figure = figure
        for m in mark_list:
            m.subscribe(self)

    def on_update(self, value):
        self.figure.canvas.draw()
