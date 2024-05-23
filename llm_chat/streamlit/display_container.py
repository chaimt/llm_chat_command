class DisplayContainer:
    def __init__(self, data, id, generate_func):
        self.data = data
        self.id = id
        self.generate_func = generate_func

    def get_display(self):
        self.generate_func(self.data, self.id)
