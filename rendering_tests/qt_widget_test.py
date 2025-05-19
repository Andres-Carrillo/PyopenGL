import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.qt_base import QGLApp
from PyQt5 import QtWidgets

import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QGLApp()
    main_window.run()
    main_window.show()
    sys.exit(app.exec_())