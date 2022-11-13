import sqlite3
import sys

from appcore.station_model import StationModel


class MapModel:
    """Keeps the logic of the map and gets update when new GPS coordinates are received.
    Observed by Mapview, which is notified when self is updated.
    New MapModel is initialized when race is changed."""
    def __init__(self, db_path, table):
        self.model_name = table
        self.points = None
        self.model_stations = []
        self.runner_path = []
        self.next_station_info = None
        self.observers = []

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        self._get_track_points(cursor, table)
        self._make_station_objects(cursor, table)
        connection.close()

        self.map_center = self.get_center_of_map_from_stations()


    def _get_track_points(self, cursor, table_name):
        """Queries DB for all points on route."""
        query = "SELECT name FROM sqlite_master WHERE type='table' and name=?"
        validated_table_name = cursor.execute(query, (table_name,)).fetchone()[0]
        cursor.execute(f"SELECT latitude, longitude, elevation, distance FROM {validated_table_name}")
        self.points = cursor.fetchall()

    def _get_station_points(self, cursor, table_name):
        """Queries DB for all points on route that are stations."""
        query = "SELECT name FROM sqlite_master WHERE type='table' and name = ?"
        validated_table_name = cursor.execute(query, (table_name,)).fetchone()[0]
        cursor.execute(f"SELECT * FROM {validated_table_name} WHERE st_name is NOT NULL")
        return cursor.fetchall()

    def _make_station_objects(self, cursor, table):
        """Pins the stations along the route and saves them as a list of Station() objects in self.stations"""
        for station in self._get_station_points(cursor, table):
            st_lat, st_lon, elev, dist, st_name = station
            st = StationModel(st_name, st_lat, st_lon, elev, dist, 0)
            self.model_stations.append(st)
            self.add_observer(st)

    def get_center_of_map_from_stations(self) -> tuple:
        """Returns center of map as tuple."""
        avg_lat = sum(p.lat for p in self.model_stations)/len(self.model_stations)
        avg_lon = sum(p.lon for p in self.model_stations)/len(self.model_stations)
        return (avg_lat, avg_lon)

    def get_next_station_info(self) -> dict:
        """Returns a dictionary with information about next station."""
        runner = self.runner_path[-1]
        until_end = self.points[-1][3] - runner[3]
        min_dist = 100
        closest_station = None
        next_station = [station for station in self.model_stations if station.dist_diff > 0][0]
        for station in self.model_stations:
            if abs(station.dist_diff) < min_dist:
                min_dist = abs(station.dist_diff)
                closest_station = station
        in_between_points = [point for point in self.points if runner[3] < point[3] < next_station.dist]
        elev_gain = 0
        elev_loss = 0
        for i in range(len(in_between_points) - 1):
            diff = in_between_points[i + 1][2] - in_between_points[i][2]
            if diff < 0:
                elev_loss += diff
            else:
                elev_gain += diff
        return {'next': next_station,
                'closest': closest_station,
                'gain': elev_gain,
                'loss': elev_loss,
                'end': until_end}

    def get_closest_point_on_track(self, gps_lat, gps_lon) -> tuple:
        """Returns closest point on track to GPS position."""
        min_diff = sys.maxsize
        closest_point = None
        for point in self.points:
            diff = abs(point[0] - gps_lat) + abs(point[1] - gps_lon)
            if diff < min_diff:
                min_diff = diff
                closest_point = point
        self.runner_path.append(closest_point)
        return closest_point

    def update_model_from_gps_pos(self, gps_lat, gps_lon):
        """Updates MapModel upon receiving new GPS coordiante.
         Updates runner path with closest point from route based on new GPS position.
         Updates dist_diff from runner for each station.
         Notifies observers of self update."""

        self.get_closest_point_on_track(gps_lat, gps_lon)
        for st in self.model_stations:
            st.respond_to_model_update()
        self.next_station_info = self.get_next_station_info()
        self.notify_observers()

    def add_observer(self, observer):
        """Add observer to MapModel."""
        self.observers.append(observer)

    def notify_observers(self):
        """Notify observers of MapModel update."""
        for observer in self.observers:
            observer.respond_to_model_update()

if __name__ == '__main__':
    pass
    # mm = MapModel('ultra_buddy3.db')
    # print(mm.points)
    # print(mm.model_stations)
    # print(mm.map_center)
    # mm.update_model_from_gps_pos(42.50049, 23.206102)
    # print(mm.next_station_info)
