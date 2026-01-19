import h5py
import numpy as np
from scipy.signal import periodogram

import pyqtgraph as pg
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject, Signal


class Import_H5(QObject):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.ui = main.ui
        self.file_path = ""

    def get_file_path(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            None, "Select H5 file", "", "H5 Files (*.h5)"
        )

        if not self.file_path:
            return

        self.attrs = {}  # <-- store all attributes here

        with h5py.File(self.file_path, "r") as f:
            print("Root keys:", list(f.keys()))

            for key, value in f["/"].attrs.items():
                # Convert numpy types to Python types
                if hasattr(value, "tolist"):
                    value = value.tolist()

                self.attrs[key] = value

        print("H5 attributes loaded:")
        for k, v in self.attrs.items():
            print(k, ":", v)


class Process_h5_file(QObject):
    sig_plot_ready = Signal(np.ndarray, np.ndarray)

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.file_path = ""

    def process_once(self):
        # Use already loaded data from main
        chA = self.main.chA

        if chA is None:
            print("❌ No data available for processing")
            return

        wf = chA.astype(np.float32)

        # PSD along time axis
        _, psd = periodogram(wf, axis=0)

        self.sig_plot_ready.emit(wf, psd)

    def load_channel(self, ch_name):
        if not self.file_path:
            return None

        with h5py.File(self.file_path, "r") as f:
            if ch_name not in f:
                return None
            return np.array(f[ch_name][:])


class PlotterH5(QObject):
    def __init__(self, main):
        super().__init__()
        self.ui = main.ui
        self.wf = None
        self.psd = None

        self.wf_data = None
        self.wf_display = None

        self.psd_data = None
        self.psd_display = None

    def init_waterfall_plots(self):
        self.ui.graphicsView_wf.clear()
        self.wf_img = pg.ImageItem()
        self.ui.graphicsView_wf.addItem(self.wf_img)
        self.wf_img.setColorMap(pg.colormap.get("CET-R4"))

        self.ui.graphicsView_psd.clear()
        self.psd_img = pg.ImageItem()
        self.ui.graphicsView_psd.addItem(self.psd_img)
        self.psd_img.setColorMap(pg.colormap.get("CET-R4"))

    def update_waterfall(self, wf, psd):
        # ---------- RAW DATA (for slicing) ----------
        self.wf_data = wf
        self.psd_data = psd

        self.rows, self.cols = wf.shape

        # ---------- DISPLAY DATA ----------
        # Flip vertically for correct visual orientation
        self.wf_display = np.flipud(wf)
        self.psd_display = np.flipud(psd)

        # ---------- Plot ----------
        self.wf_img.setImage(self.wf_display, autoLevels=True)
        self.psd_img.setImage(self.psd_display, autoLevels=True)

    def plot_row_col(self, row, col):
        if self.wf_data is None:
            return

        # Clamp indices
        row = max(0, min(self.rows - 1, row))
        col = max(0, min(self.cols - 1, col))

        self.ui.graphicsView_wf_row.clear()
        self.ui.graphicsView_wf_col.clear()

        # ROW slice → time / distance
        self.ui.graphicsView_wf_row.plot(
            self.wf_data[row, :], pen='c'
        )
        self.ui.graphicsView_wf_row.setTitle(f"Row {row}")

        # COLUMN slice → fast time
        self.ui.graphicsView_wf_col.plot(
            self.wf_data[:, col], pen='y'
        )
        self.ui.graphicsView_wf_col.setTitle(f"Column {col}")

    def plot_psd_row_col(self, row, col):
        if self.psd_data is None:
            return

        rows, cols = self.psd_data.shape

        row = max(0, min(rows - 1, row))
        col = max(0, min(cols - 1, col))

        self.ui.graphicsView_psd_row.clear()
        self.ui.graphicsView_psd_col.clear()

        # Frequency bin slice (freq → distance)
        self.ui.graphicsView_psd_row.plot(
            self.psd_data[row, :], pen='y'
        )
        self.ui.graphicsView_psd_row.setTitle(f"Freq bin {row}")

        # Full spectrum at one distance
        self.ui.graphicsView_psd_col.plot(
            self.psd_data[:, col], pen='c'
        )
        self.ui.graphicsView_psd_col.setTitle(f"Channel {col}")

