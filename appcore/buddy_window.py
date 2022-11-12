import certifi
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen


class BuddyWindow(MDScreen):
    dialog = None
    input_bib = ObjectProperty(None)
    runner_bib = ObjectProperty(None)
    runner_name = ObjectProperty(None)
    dnf_status = ObjectProperty(None)
    last_checkin = ObjectProperty(None)

    def get_buddy_data(self):
        input_bib = self.input_bib.text
        if not len(input_bib) == 4 or not input_bib.isdigit():
            info = 'Runner bib should be a 4-digit number!'
            self.show_dialog(info)
        model_name = MDApp.get_running_app().map_model.model_name
        if model_name == 'persenk110' or model_name == 'tryavna100':
            info = 'Find friend feature not available for this race yet!'
            self.show_dialog(info)
        # 2549 for DNF
        # 2206 for third place
        app = MDApp.get_running_app()
        race_result_url = app.config['raceresult']['Url'] + input_bib
        # response = requests.get(race_result_url)
        UrlRequest(race_result_url, on_success=self.process_successful_buddy_request, on_failure=self.failure, on_error=self.error, ca_file=certifi.where())

    def process_successful_buddy_request(self, urlrequest, response):
        self.buddy_data = response
        # with open('samplejsonDNF.json', 'r') as f:
        #     self.buddy_data = json.load(f)

        if not self.buddy_data['data']:
            info = f"Bib {self.input_bib.text} was not found!"
            self.show_dialog(info)
            return
        self.display_buddy_data()

    def failure(self, urlrequest, response):
        print('failure!')
        print(response)

    def error(self, urlrequest, response):
        print('error!')
        print(response)

    def dialog_close(self, *args):
        self.input_bib.text = ''
        self.dialog.dismiss(force=True)

    def show_dialog(self, info, *args):
        if not self.dialog:
            self.dialog = MDDialog(
                text=info,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color='darkgreen',
                        on_release=self.dialog_close
                    )
                ]
            )
        self.dialog.open()

    def display_buddy_data(self):
        # bib
        self.runner_bib.secondary_text = self.buddy_data['data'][0][0]
        # name
        self.runner_name.secondary_text = self.buddy_data['data'][0][3]
        # DNF status
        status = self.buddy_data['data'][0][1]
        if 'DNF' in status:
            self.dnf_status.secondary_text = 'Buddy is DNF!'
        else:
            self.dnf_status.secondary_text = 'Buddy is still in the race!'
        checkpoints = self.buddy_data['data'][0][11:17]
        available_timepoints = [x for x in self.buddy_data['data'][0][18:24] if x]
        self.last_checkin.secondary_text = f'At {checkpoints[len(available_timepoints) - 1]} with time {available_timepoints[-1]}'
