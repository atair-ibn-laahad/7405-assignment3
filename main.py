import os
import subprocess
import sys
import platform
import glob


def find_gui_file(extension):
    files = glob.glob(os.path.join('./GUI', f'*{extension}'))
    return files[0] if files else None


def start_fastapi():
    # Start the FastAPI server and return the process
    return subprocess.Popen(['uvicorn', 'api.api_entries:app', '--host', '0.0.0.0', '--port', '7405'])


def start_electron():
    os_type = platform.system()
    gui_file_extensions = {
        "Linux": ".AppImage",
        "Windows": ".exe",
        "Darwin": ".app"
    }
    extension = gui_file_extensions.get(os_type)

    if extension:
        gui_file = find_gui_file(extension)
        if gui_file:
            try:
                print(f"Starting Electron app: {gui_file}")

                if os_type == "Linux" or os_type == "Windows":

                    process = subprocess.Popen([gui_file], stderr=subprocess.PIPE)
                elif os_type == "Darwin":
                    process = subprocess.Popen(['open', gui_file], stderr=subprocess.PIPE)

                _, errors = process.communicate()
                if errors:
                    print(f"Error: {errors.decode()}")
                return process
            except Exception as e:
                print(f"Failed to start Electron app: {e}")
                sys.exit(1)
        else:
            print("GUI file not found. Cannot start Electron app.")
            sys.exit(1)
    else:
        print("Unsupported OS")
        sys.exit(1)


if __name__ == "__main__":
    print("Starting might be slow. If you find any problem starting the whole project, try to start"
          " the server and GUI manually by running the ./api/api_entries.py"
          " and start the GUI program manually")
    fastapi_process = start_fastapi()

    electron_process = start_electron()
    electron_process.wait()

    fastapi_process.terminate()
