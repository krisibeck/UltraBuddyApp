[//]: <> (Readme for Ultra BUddy App)

# Ultra Buddy App
## A Mobile App for Ultra Runners
Ultra Buddy provides information for runners during ultra races. 
The runner can see a map of the race with aid stations along the way.
By touching an aid station, the runner is shown the distance remaining to that station. 
More detailed information, such as elevation gain and lost is available also. 
Three running races are currently integrated into the app: Vitosha100, Tryavna100, and Persenk110.
- [Video Demo](https://www.youtube.com/watch?v=9Y7RaWTjJjw)
- [Full Presentation](https://www.youtube.com/watch?v=ieIp-gkvLB4)
---
![alt text](https://github.com/krisibeck/UltraBuddyApp/blob/master/img/home_screen_small.png "Home screen")
![alt text](https://github.com/krisibeck/UltraBuddyApp/blob/master/img/map_screen_small.png "Map screen")
![alt text](https://github.com/krisibeck/UltraBuddyApp/blob/master/img/map_screen_zoom_small.png "Map screen")
![alt text](https://github.com/krisibeck/UltraBuddyApp/blob/master/img/next_screen_small.png "Next screen")
---
## Installation
The mobile app is available as an .apk in the repo. To install the mobile app, copy the .apk file on your Android device and open the file to install the app.
- ![Ultra Buddy apk](https://github.com/krisibeck/UltraBuddyApp/tree/master/apk "Ultra Buddy Apk")

To run as a desktop app: 
1. Clone the repo into a new directory on your machine.
2. Pip install the required modules:
```bash
$ pip install -r requirement.txt
```
4. Run main.py with your Python interpreter.
```bash
$ python main.py
```
Note: For the "find friend" feature to work, you have to obtain the config.ini file, which is not included in this repository. 

## Dependencies
<div>
    <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" width="40" height="40"/>&nbsp;
    <img src="https://github.com/devicons/devicon/blob/master/icons/android/android-original-wordmark.svg" width="40" height="40"/>&nbsp;
    <img src="https://raw.githubusercontent.com/kivy/kivy/master/kivy/data/logo/kivy-icon-256.png" width="40" height="40"/>&nbsp;
</div>

The project is created with: 
- Python 3.10.7
- Kivy 2.1.0
- KivyMD 1.1.1
- Plyer 2.0.0
- Buildozer 1.4.0
For detailed requirements, please the requirements.txt file. 

## Contributing

Pull requests are welcome.

## Licensing and Distribution

[MIT](https://choosealicense.com/licenses/mit/)