class Router:
    def __init__(self, page):
        self.page = page
        self.views = {}

    def get_view(self, name, cls):
        if name not in self.views:
            self.views[name] = cls(self.page, self)
        return self.views[name]

    def go(self, name, cls):
        self.page.controls.clear()
        view = self.get_view(name, cls)
        view.build()
        self.page.update()
