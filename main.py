import configparser

from kivy.core.window import Window
from kivymd.app import MDApp

from appcore.gpshelper import GpsHelper
from appcore.map_model import MapModel

# Uncomment to emulate phone dimensions in Desktop app
Window.size = (375, 750)

class UltraBuddyApp(MDApp):
    """TheMDApp with build, on_start, on_pause, and on_resume methods.
    The kv file for it must be named with same name without 'App' - 'ultrabuddy'."""

    def build(self):
        """Builds app from ultrabuddy.kv"""
        pass

    def on_start(self):
        """Read configs, apply theme, connect to DB, get route points and stations, initiate GPS service."""

        # Read configs
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read('config.ini')
        # print(self.config['raceresult']['url'])

        # Apply theme
        self.theme_cls.primary_palette = 'LightGreen'
        self.theme_cls.primary_hue = '700'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = 'M3'

        # Start map model
        self.map_model = MapModel('ultrabuddy_db_multi.db', 'vitosha100')

        # Set up views and models
        app = MDApp.get_running_app()
        app.root.map_w.add_station_views_from_station_models()
        self.map_model.add_observer(app.root.map_w)
        self.map_model.add_observer(app.root.next_w)
        app.root.map_w.main_map.center_on(*self.map_model.map_center)

        # Initiate GPS
        print('***App starting - starting GPS...')
        self.gps_helper = GpsHelper()
        self.gps_helper.run()

    def on_pause(self):
        # Stop GPS on App pause
        print('***App  paused - stopping GPS****')
        self.gps_helper.stop()
        return True

    def on_resume(self):
        # Start GPS on App resume
        print('***App resuming - resuming GPS...***')
        self.gps_helper.resume()


if __name__ == '__main__':
    UltraBuddyApp().run()
