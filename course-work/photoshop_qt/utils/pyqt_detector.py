# pyqt_detector.py

class PyQtDetector:
    """
    Detects the PyQt version (5 or 6) being used.
    """
    def __init__(self):
        self._pyqt_version = self._detect_pyqt_version()

    def _detect_pyqt_version(self):
      """Detects the PyQt version (5 or 6) being used.

      Returns:
        str: "PyQt6" if PyQt6 is detected, "PyQt5" if PyQt5 is detected, or "None" if neither is found.
      """
      try:
        from PyQt6 import QtWidgets, QtGui, QtCore
        return "PyQt6"
      except ImportError:
        try:
          from PyQt5 import QtWidgets, QtGui, QtCore
          return "PyQt5"
        except ImportError:
            return "None"

    def get_version(self):
        """
        Returns:
            str: The detected PyQt version ("PyQt6", "PyQt5", or "None").
        """
        return self._pyqt_version

    def is_pyqt6(self):
        """
        Returns:
           bool: True if PyQt6 is detected, False otherwise.
        """
        return self._pyqt_version == "PyQt6"

    def is_pyqt5(self):
        """
        Returns:
           bool: True if PyQt5 is detected, False otherwise.
        """
        return self._pyqt_version == "PyQt5"


if __name__ == '__main__':
    # Example usage if you run this file directly:
    detector = PyQtDetector()
    version = detector.get_version()
    if version == "PyQt6":
      print("You are using PyQt6")
    elif version == "PyQt5":
      print("You are using PyQt5")
    else:
      print("Neither PyQt5 nor PyQt6 is installed")

    print(f"Is PyQt6?: {detector.is_pyqt6()}")
    print(f"Is PyQt5?: {detector.is_pyqt5()}")
