from kivy.app import App
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog
from plyer import gps


class GpsHelper:
    """Controls gps services and actions upon obtaining new gps coordinates."""

    def run(self):
        """Initiates GPS collection, including requesting persmissions."""
        gps_blinker = App.get_running_app().root.map_w.ids.blinker
        gps_blinker.blink()

        # uncomment to run as desktop app instead of mobile app
        self.pass_new_gps_to_map_model()

        # Request permissions and start gps service on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")
                    gps.configure(on_location=self.pass_new_gps_to_map_model,
                                  on_status=self.on_auth_status)
                    gps.start(minTime=15000, minDistance=100)
                else:
                    print("Did not get all permissions")


            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)

        # Start gps service on iOS
        if platform == 'ios':
            gps.configure(on_location=self.pass_new_gps_to_map_model,
                          on_status=self.on_auth_status)
            gps.start(minTime=15000, minDistance=0)

    def stop(self):
        """Initiated on_pause of App to stop collecting GPS data."""
        print('GPS stopped...')
        gps.stop()

    def resume(self):
        """Initiated on_resume of App to start collecting GPS data again (no permissions needed)."""
        gps.start(minTime=15000, minDistance=0)

    def pass_new_gps_to_map_model(self, *args, **kwargs):
        """Updates MapModel with new GPS position."""
        # gps_lat = kwargs['lat']
        # gps_lon = kwargs['lon']
        # Can use these hard-coded coordinates for testing
        gps_lat = 42.50049
        gps_lon = 23.206102
        app = App.get_running_app()
        if abs(gps_lat - app.map_model.map_center[0]) < 1 and abs(gps_lon - app.map_model.map_center[1]) < 1:
            print("GPS POSITION:", gps_lat, gps_lon)
            app.map_model.update_model_from_gps_pos(gps_lat, gps_lon)


    def on_auth_status(self, general_status, status_message):
        """Called on_status for gps.configure() - proceed normally if permissions granted, else popup warning Dialog."""
        if general_status == 'provider-enabled':
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        """Dialogue popped up in case of gps persmissions not granted."""
        dialog = MDDialog(title="GPS Error", text="You need to enable GPS access for the app to function properly")
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        dialog.open()
