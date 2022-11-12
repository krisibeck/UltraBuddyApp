from kivy.clock import Clock
from kivy.properties import ObjectProperty, partial
from kivy_garden.mapview import MapMarker
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from appcore.station_view import StationView


class MapWindow(MDScreen):
    """Displays the MapView widget with use of the current MapModel (route points, stations and gps blinker)."""
    main_map = ObjectProperty(None)
    blinker = ObjectProperty(None)
    plotting_points_timer = None

    def __init__(self, **kwargs):
        super(MapWindow, self).__init__(**kwargs)
        self.plotted_route_points = set()
        self.station_views = []
        self.start_plotting_points_in_fov()
        self.app = MDApp.get_running_app()

    def add_station_views_from_station_models(self):
        """Adds StationViews for each StationModel in the MapModel."""
        for st_model in self.app.map_model.model_stations:
            st_view = StationView(st_model)
            st_model.add_observer(st_view)
            self.station_views.append(st_view)
            self.main_map.add_widget(st_view)
            btn_callback = partial(self.popup_station_and_zoom, st_view)
            st_view.btn.bind(on_touch_down=btn_callback)

    def popup_station_and_zoom(self, st_touched, source, touch):
        """Bound event on_touch_down for each StationView popup - shows popup with station name."""
        if source.collide_point(*touch.pos):
            for station in self.station_views:
                if station != st_touched and station.is_open:
                    station.refresh_open_status()
            if st_touched.model.dist_diff:
                display_dist = '+' + str(round(st_touched.model.dist_diff, 1)) \
                    if st_touched.model.dist_diff >= 0 \
                    else str(round(st_touched.model.dist_diff, 1))
                st_touched.btn.text = st_touched.model.name + '\n' + f'{display_dist} km'
            self.main_map.center_on(st_touched.lat, st_touched.model.lon)
            self.main_map.zoom = 12

    def start_plotting_points_in_fov(self):
        """Called on_zoom of MapView - wait 0.5 second before starting to plot waypoints
         to avoid doing it constantly if the user is zooming in and out a lot."""

        try:
            # if the timer is not None (i.e. it is counting down from a previous on_zoom), stop the timer, so it can be reset
            self.plotting_points_timer.cancel()
        except:
            # If the timer IS None, canceling it won't work - pass
            pass

        # when the 1 second has passed without the timer getting cancelled, call the function that will plot the points
        # .schedule_once() schedules only 1 execution of the function as the name suggest
        self.plotting_points_timer = Clock.schedule_once(self.plot_points_in_fov, 0.5)

    def plot_points_in_fov(self, clock):
        # print(f'{clock} since self.getting_waypoints_timer was set (should be ~ 0.5 sec)')
        # print(f'Current zoom is: {self.main_map.zoom}')
        # print(f'The four corners of the map are: {self.main_map.get_bbox()}')
        # print('Plotting waypoints now...')

        step = -5 * self.main_map.zoom + 95

        min_lat, min_lon, max_lat, max_lon = self.main_map.get_bbox()

        for i in range(0, len(self.app.map_model.points), step):
            p = self.app.map_model.points[i]
            lat, lon = p[0], p[1]
            if p not in self.plotted_route_points and min_lat < lat < max_lat and min_lon < lon < max_lon:
                point = MapMarker(lat=p[0], lon=p[1], source='img/green_small_waypoint.png')
                self.plotted_route_points.add(point)
                self.main_map.add_marker(point)

    def respond_to_model_update(self):
        new_lat, new_lon = self.app.map_model.runner_path[-1][:2]
        self.blinker.lat = new_lat
        self.blinker.lon = new_lon

    def reset_map(self):
        for st in self.station_views:
            self.remove_widget(st)
        for pt in self.plotted_route_points:
            self.remove_widget(pt)