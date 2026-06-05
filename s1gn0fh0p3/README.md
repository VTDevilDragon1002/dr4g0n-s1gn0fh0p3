# Sign of Hope — Complete Working Accessibility Project

A complete frontend accessibility support project for blind, deaf, mute, movement-impaired users and emergency communication.

## Working Features
- Login page with localStorage demo login
- Home dashboard
- Blind Mode: text-to-speech support
- Deaf Mode: speech-to-text captions
- Mute Mode: text-to-voice communication
- Movement Mode: large accessible buttons
- Emotion board with voice output
- Emergency SOS with optional location and SMS link
- Working hand sign recognition page
  - Open palm / help
  - Fist / stop
  - Finger count
  - Thumbs up
  - Thumbs down
  - OK sign
  - Call me sign
  - I love you sign
  - Manual test buttons for every sign
- Dark/light theme
- Responsive professional UI

## Important: How to Run Camera Features
Camera and microphone are blocked by some browsers when you open HTML directly.

### Windows
1. Extract the ZIP.
2. Open the folder.
3. Double-click `start-server.bat`.
4. Open Chrome/Edge and go to:
   `http://localhost:5500`
5. Allow camera/microphone permission.

### Linux / Kali
```bash
cd sign-of-hope-working-project
python3 -m http.server 5500
```
Then open:
```text
http://localhost:5500
```

## Folder Structure
```text
sign-of-hope-working-project/
├── index.html
├── home.html
├── blind.html
├── deaf.html
├── mute.html
├── movement.html
├── camera.html
├── emotion.html
├── emergency.html
├── about.html
├── start-server.bat
├── start-server.sh
└── assets/
    ├── css/style.css
    ├── js/app.js
    ├── js/camera.js
    └── img/logo.svg
```

## Note
This is a frontend project. Login is demo authentication only. MediaPipe hand recognition uses CDN, so internet is required for real camera sign detection. Manual buttons work offline.
