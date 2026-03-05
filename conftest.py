import os
import shutil


def pytest_sessionstart(session):
    if shutil.which("chromedriver"):
        return

    import chromedriver_autoinstaller

    driver_path = chromedriver_autoinstaller.install()
    driver_dir = os.path.dirname(driver_path or "")
    os.environ["PATH"] = driver_dir + os.pathsep + os.environ.get("PATH", "")

