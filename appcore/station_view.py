from kivy_garden.mapview import MapMarkerPopup
from kivymd.uix.button import MDFlatButton


class StationView(MapMarkerPopup):
    """Visualization for StationModel (inherits from Kivy MapMarkerPopup.)"""
    def __init__(self, st_model, **kwargs):
        super(StationView, self).__init__(lat=st_model.lat, lon=st_model.lon, **kwargs)
        self.model = st_model
        # btn is the popup that pops up when marker is touched
        self.btn = MDFlatButton(text=f'See\n{self.model.name}',
                                font_style='Button',
                                theme_text_color='Custom',
                                text_color='white',
                                md_bg_color='green',
                                valign='center',
                                halign='center')
        self.add_widget(self.btn)