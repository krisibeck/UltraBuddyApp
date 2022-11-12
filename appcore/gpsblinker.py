from kivy_garden.mapview import MapMarker
from kivy.animation import Animation

class GpsBlinker(MapMarker):
    """GPS Blinker Animation."""
    def blink(self):
        """Animation that changes the blink size and opacity.
        When animation completes, reset animation, then repeat."""
        # opacity = 0 is fully transparent, opacity = 1 is not transparent at all
        anim = Animation(outer_opacity=0, blink_size=50)
        anim.bind(on_complete=self.reset)
        anim.start(self)

    def reset(self, *args):
        """Resets GPS blinker animation."""
        self.outer_opacity = 1
        self.blink_size = self.default_blink_size
        self.blink()