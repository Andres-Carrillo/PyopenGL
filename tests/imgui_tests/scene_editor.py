import pathlib
import sys
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from apps.scene_editor import SceneEditor
        
# Run the application
if __name__ == "__main__":

    app = SceneEditor( width=1280, height=720,static_camera=False )
    app.run()
