from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class NextWindow(MDScreen):
    next_st = ObjectProperty(None)
    closest_st = ObjectProperty(None)
    elev_gain = ObjectProperty(None)
    elev_loss = ObjectProperty(None)
    until_end = ObjectProperty(None)

    def respond_to_model_update(self):
        app = MDApp.get_running_app()
        info = app.map_model.next_station_info
        # print(info)
        self.next_st.secondary_text = f"{info['next'].name} in {info['next'].dist_diff:.1f} km"
        self.closest_st.secondary_text = f"{info['closest'].name} in {info['closest'].dist_diff:.1f} km"
        self.elev_loss.secondary_text = f"{int(info['loss'])} meters"
        self.elev_gain.secondary_text = f"{int(info['gain'])} meters"
        self.until_end.secondary_text = f"Only {info['end']:.1f} km to go!"
