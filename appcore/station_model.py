
class StationModel:
    def __init__(self, name, lat, lon, elev, dist, dist_diff):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.elev = elev
        self.dist = dist
        self.dist_diff = dist_diff
        self.observers = []

    def update_station_dist_diff_from_runner(self, runner_dist):
        self.dist_diff = self.dist - runner_dist

    def notify_observers(self):
        for observer in self.observers:
            observer.respond_to_model_update()

    def add_observer(self, observer):
        self.observers.append(observer)