# Running SpeedRead on a physical Android device (USB)

Two long-running terminals, two folders: `backend/` and `flutter_app/`.

## One-time setup (already done on this machine)

- Phone/tablet: Developer options → **USB debugging** enabled, cable accepted
  ("Allow USB debugging?" popup → Allow).
- USB connection mode set to **File Transfer (MTP)**, not "Charging only"
  (some phones hide ADB in charging-only mode).
- Android SDK: platform 36, build-tools 28.0.3/36, NDK 28.2.13676358, all
  licenses accepted (`sdkmanager --licenses`).

If you plug in a **different** device for the first time, redo the phone-side
steps above for it.

## Terminal 1 — Backend

```powershell
cd "C:\Users\Acer Nitro 5\PycharmProjects\SpeedRead-app\backend"
.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Leave this running — the app can't fetch data without it.

## Terminal 2 — USB port forward + launch

```powershell
adb reverse tcp:8000 tcp:8000
```
This makes the device's own `localhost:8000` tunnel to the PC's backend over
USB. **Must be redone every time you unplug/replug the device** — it does not
persist across reconnects.

Check which device is connected (id changes if you switch phone/tablet):
```powershell
flutter devices
```

Then, from the Flutter project folder:
```powershell
cd "C:\Users\Acer Nitro 5\PycharmProjects\SpeedRead-app\flutter_app"
flutter run -d <device-id>
```

## Recap — every time

1. Plug in the device via USB‑C.
2. Terminal 1: activate venv, run uvicorn (`backend/`).
3. Terminal 2: `adb reverse tcp:8000 tcp:8000`, then `flutter run -d <device-id>` (`flutter_app/`).

## Troubleshooting

- `adb devices` shows nothing → USB debugging not enabled, cable is
  charge-only, or the "Allow USB debugging?" popup needs re-accepting.
- App shows "Failed to fetch" on the device → you forgot to redo
  `adb reverse tcp:8000 tcp:8000` after reconnecting, or the backend isn't
  running.
- First build only: Gradle may need to download SDK components (Build-Tools,
  NDK, CMake) — this can take several minutes and is normal. If a download
  fails with `java.net.SocketException: An established connection was
  aborted`, it's a local network/firewall interruption, not a real error —
  delete the partially-downloaded package under
  `%LOCALAPPDATA%\Android\Sdk\...` and reinstall it via `sdkmanager` directly
  (more reliable than Gradle's on-demand downloader for large packages like
  the NDK).
