from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from appcore.map_model import MapModel


class MainWindow(MDScreen):
    """The home window that shows which race is selected and allows uset to change race."""

    def change_race(self, race, img_path):
        app = MDApp.get_running_app()
        app.map_model = MapModel('ultrabuddy_db_multi.db', race)
        app.root.map_w.add_station_views_from_station_models()
        app.map_model.add_observer(app.root.map_w)
        app.map_model.add_observer(app.root.next_w)
        app.root.map_w.main_map.center_on(*app.map_model.map_center)
        app.root.main_w.ids.smart_tile.source = img_path
        app.gps_helper.run()
        print('Race getting changed...')

    def change_race_to_vitosha100(self, source):
        self.change_race('vitosha100', 'img/vit100b.jpeg')

    def change_race_to_tryavna100(self, source):
        self.change_race('tryavna100', 'img/tryavna100_cropped.jpg')

    def change_race_to_persenk110(self, source):
        self.change_race('persenk110', 'img/persenk110.png')