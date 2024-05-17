from abc import ABC, abstractmethod

class Tab(ABC):
    def set_up(self):
        pass

    def on_entry_tab(self):
        pass

    def update(self, dt):
        pass

    def key_pressed(self, event):
        pass

    def on_close_app(self):
        pass

    