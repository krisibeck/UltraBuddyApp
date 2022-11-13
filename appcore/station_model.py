from kivymd.app import MDApp


class StationModel:
    """A model for stations along the running route."""
    def __init__(self, name, lat, lon, elev, dist, dist_diff):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.elev = elev
        self.dist = dist
        self.dist_diff = dist_diff
        self.observers = []

    def respond_to_model_update(self):
        runner_dist = MDApp.get_running_app().map_model.runner_path[-1][3]
        self.dist_diff = self.dist - runner_dist
        self.notify_observers()

    def notify_observers(self):
        for observer in self.observers:
            observer.respond_to_model_update()

    def add_observer(self, observer):
        self.observers.append(observer)