from math import sin, cos, sqrt, pi
import sqlite3

import gpxpy.gpx


def extract_lat_long_elev_from_gpx(gpx_path) -> list:
    """Uses gpxpy module to extract latitude, longitude, elevation from a gpx file.
    Returns a list of points (latitude, longitude, elevation)"""
    points = []
    with open(gpx_path, 'r') as f:
        gpx_file = f.read()

    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        # print(track)
        for segment in track.segments:
            # print(segment)
            for point in segment.points:
                # print(point)
                points.append((float(point.latitude), float(point.longitude), float(point.elevation)))
    return points

def distance_difference_with_elevation(p1: tuple, p2: tuple) -> float:
    """Takes lon, lat and elev for two points and returns distance in km"""

    def convert_to_radians(deg):
        """Converts degrees to radians"""
        return deg * pi / 180

    def convert_to_cartesian(lat, lon, elev):
        """Converts to Cartesian coordinates in km"""
        elev = elev / 1000
        lat = convert_to_radians(lat)
        lon = convert_to_radians(lon)
        R = 6378.1
        x = (elev + R) * cos(lat) * sin(lon)
        y = (elev + R) * sin(lat)
        z = (elev + R) * cos(lat) * cos(lon)
        return x, y, z

    x1, y1, z1 = convert_to_cartesian(*p1[:3])
    x2, y2, z2 = convert_to_cartesian(*p2[:3])

    d = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    return d

def add_total_distance_to_all_points(all_points: list) -> list:
    """Takes a list of all track points (lat, lon, elev)
     and add a total distance (lat, lon, eleve, tot_dist).
     Returns a list of all points with distance added."""
    d = 0
    all_points[0] += (0,)
    for i in range(len(all_points) - 1):
        d += distance_difference_with_elevation(all_points[i], all_points[i + 1])
        all_points[i + 1] += (d,)
    return all_points

def get_aid_stations_points(all_points_with_dist: list, stations_lst: list, official_stations_dist: list) -> dict:
    """Take a list of all points on track with distance and uses
    hardcoded information about the stations to generate a dictionary
    with station name as key and point info as value:
    {st_name: (lat, lon, elev, tot_dist)"""

    official_stations_dict = {key: value for key, value in zip(stations_lst, official_stations_dist)}
    stations = {}
    for point in all_points_with_dist:
        for name, off_dist in official_stations_dict.items():
            if abs(point[3] - off_dist) < 0.015 and name not in stations:
                stations[name] = point
    # Manually correct finish to be last available point
    stations['Finish'] = all_points_with_dist[-1]
    return stations

def update_points_with_distance_with_station_names(points_with_distance, stations):
    """Adds the station name to points that are a station and 'None' to points that are not a station"""
    for st_name, st_point in stations.items():
        point_idx = points_with_distance.index(st_point)
        points_with_distance[point_idx] += (st_name,)

    for idx, point in enumerate(points_with_distance):
        if len(point) == 4:
            points_with_distance[idx] += (None,)

    return points_with_distance

def build_database(all_points_with_dist_st_name, db_path, table_name):
    # TODO make the SQL query take the table_name as a variable!
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()


    cur.execute("""CREATE TABLE persenk110 (
                        latitude real NOT NULL,
                        longitude real NOT NULL,
                        elevation real NOT NULL,
                        distance real NOT NULL,
                        st_name text NULL 
                        );""")

    def insert_point(point):
        with conn:
            lat, lon, elev, dist, st_name = point
            cur.execute(f"INSERT INTO persenk110 VALUES (:lat, :lon, :elev, :dist, :st_name)",
                        {'lat': lat, 'lon': lon, 'elev': elev, 'dist': dist, 'st_name': st_name})


    def get_points():
        cur.execute(f"SELECT latitude, longitude, elevation, distance  FROM persenk110 WHERE st_name is NULL")
        return cur.fetchall()

    def get_stations():
        cur.execute(f"SELECT * FROM persenk110 WHERE st_name is NOT NULL")
        return cur.fetchall()

    for point in all_points_with_dist_st_name:
        insert_point(point)

    points = get_points()
    stations = get_stations()
    center_lat = sum(st[0] for st in stations)/len(stations)
    center_lon = sum(st[1] for st in stations)/len(stations)
    print(points)
    print(stations)
    print('Center:', center_lon, center_lat)
    conn.close()

def get_all_db_table_names(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = """SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;"""
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    return result

def get_all_points_from_table(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT latitude, longitude, elevation, distance FROM {table_name} WHERE st_name is NULL")
    result = cur.fetchall()
    conn.close()
    return result

def get_all_stations_from_table(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name} WHERE st_name is NOT NULL")
    result = cur.fetchall()
    conn.close()
    return result

def add_race_to_db(db_path, table_name, gpx_path, station_names, official_distances):
    points_no_dist = extract_lat_long_elev_from_gpx(gpx_path)
    points_with_dist = add_total_distance_to_all_points(points_no_dist)
    # print(points_with_dist)
    stations = get_aid_stations_points(points_with_dist, station_names, official_distances)
    # print(stations)
    points_with_dist_st_names = update_points_with_distance_with_station_names(points_with_dist, stations)
    # print(points_with_dist_st_names)
    # print(len(stations))
    build_database(points_with_dist_st_names, db_path, table_name)

if __name__ == '__main__':
    vitosha100 = ['../sample_data/vitosha100.gpx',
                  ['Start', 'Vladaya', 'Kladnitsa', 'Studena', 'Chuyipetlevo', 'Yarlovo', 'Belite Brezi', 'Bistritsa','Dragalevtsi', 'Finish'],
                  [0, 9.4, 23.4, 32.5, 43.8, 61.3, 74.6, 82.2, 91.9, 97.7]]
    douglas_trail = ['../sample_data/douglas_trail.gpx',
                     ['Start', 'Station1', 'Station2', 'Station3', 'Station4', 'Finish'],
                     [0, 7, 14, 21, 30, 37.2]]
    persenk110 = ['../sample_data/persenk110.gpx',
                  ['Start', 'Chervena Stena', 'Yugovo', 'Pashalitsa', 'Hvoyna', 'Orehovo', 'Byala Cherkva', 'Dobrolak', 'Koprivkite', 'Finish'],
                  [0, 17, 27.2, 40.5, 51.3, 62, 75.3, 85, 97, 111],
                  ]
    tryavna100 = ['../sample_data/tryavna100.gpx',
                  ['Start', 'Bozhentsi', 'Sechen Kamak', 'Yabalka', 'Shipka', 'Mladost', 'Balgarka', 'Stanchov Han', 'Spirkata', 'Finish'],
                  [0, 11.2, 19.4, 35.9, 49.2, 60.6, 70.6, 84.9, 91, 100]
                  ]

    # add_race_to_db('ultrabuddy_db_multi.db', douglas_trail, *douglas_trail)
    # add_race_to_db('ultrabuddy_db_multi.db', vitosha100, *vitosha100)
    # .gpx format doesn't work as is - at some point, the points become NoneType - could be skipped?
    add_race_to_db('../ultrabuddy_db_multi.db', persenk110, *persenk110)
    # add_race_to_db('ultrabuddy_db_multi.db', tryavna100, *tryavna100)

    print(get_all_db_table_names('../ultrabuddy_db_multi.db'))
    # print(get_all_points_from_table('ultrabuddy_db_multi.db', 'vitosha100'))
    # print(get_all_stations_from_table('ultrabuddy_db_multi.db', 'vitosha100'))
    # print(get_all_points_from_table('ultrabuddy_db_multi.db', 'douglas_trail'))
    # print(get_all_stations_from_table('ultrabuddy_db_multi.db', 'douglas_trail'))