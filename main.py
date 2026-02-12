import sys
import numpy as np
import os
os.environ["QT_API"] = "pyside6"
import pyqtgraph as pg

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QStandardItemModel, QStandardItem

from form import Ui_MainWindow
from import_h5 import Import_H5, Process_h5_file, PlotterH5


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ---------- Logic ----------
        self.import_h5 = Import_H5(self)
        self.process_h5 = Process_h5_file(self)
        self.plotter = PlotterH5(self)

        # ---------- Signals ----------
        self.process_h5.sig_plot_ready.connect(self.on_processing_ready)

        # ---------- File ----------
        self.ui.pushButton_choose.clicked.connect(self.import_h5.get_file_path)
        self.ui.pushButton_read_attr.clicked.connect(self.show_attributes)
        self.ui.pushButton_process_file.clicked.connect(self.run_processing)

        # ---------- Raw trace ----------
        self.ui.pushButton_raw.clicked.connect(self.update_raw_trace)

        # ---------- Variance ----------
        self.ui.checkBox_variance.stateChanged.connect(self.plot_variance)

        # ---------- Waterfall ----------
        self.ui.pushbutton_wfrow.clicked.connect(self.update_wf_row)
        self.ui.pushButton_wfcol.clicked.connect(self.update_wf_col)

        # ---------- Spectrum ----------
        self.ui.pushButton_specrow.clicked.connect(self.update_psd_row)
        self.ui.pushButton_speccol.clicked.connect(self.update_psd_col)

        # ---------- STFT ----------
        self.ui.pushButton_stftcol.clicked.connect(self.update_stft)

        # ---------- Init plots ----------
        self.plotter.init_waterfall_plots()
        self.plotter.init_stft_plot()

        self.plotter.init_fk_plot()

        self.ui.pushButton_fk_row.clicked.connect(self.run_fk)
        self.ui.pushButton_fk_col.clicked.connect(self.run_fk)

    def on_gui_data_ready(self, ch1, ch2, sample_rate, sample_length, PRF):
        """
        Called when GUI / hardware provides fresh data
        ch1, ch2 : numpy arrays (I & Q)
        """

        attrs = {
            "sample_rate": sample_rate,
            "sample_length": sample_length,
            "PRF": PRF
        }

        # Send GUI data directly to processing pipeline
        self.process_h5.gui_ch1 = ch1
        self.process_h5.gui_ch2 = ch2
        self.process_h5.gui_attrs = attrs

        # Run SAME DSP as file mode
        self.process_h5.process_once()

    def run_fk(self):

        wf = self.plotter.wf
        if wf is None:
            print("⚠ Run processing first")
            return

        PRF = self.import_h5.file_attrs.get("PRF")
        if PRF is None:
            print("⚠ PRF missing")
            return

        cs_min = float(self.ui.doubleSpinBox_fkrow.value())
        cp_min = float(self.ui.doubleSpinBox_wfrow.value())
        cp_max = float(self.ui.doubleSpinBox_wfcolumn.value())
        cs_max = float(self.ui.doubleSpinBox_specrow.value())

        print("Running FK...")
        print(cs_min, cp_min, cp_max, cs_max)

        wf_fk = self.process_h5.compute_fk(
            wf, PRF, cs_min, cp_min, cp_max, cs_max
        )

        if wf_fk is None:
            print("FK failed")
            return

        self.plotter.update_fk(wf_fk)

        print("✅ FK DONE")

    # ==================================================
    def show_attributes(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Attribute", "Value"])

        for k, v in self.import_h5.file_attrs.items():
            model.appendRow([
                QStandardItem(str(k)),
                QStandardItem(str(v))
            ])

        self.ui.tableView_attr.setModel(model)

    # ==================================================
    def run_processing(self):
    # ---- FORCE FILE MODE ----
        self.process_h5.gui_ch1 = None
        self.process_h5.gui_ch2 = None
        self.process_h5.gui_attrs = None

        self.process_h5.file_path = self.import_h5.file_path

        # ---- User parameters ----
        self.process_h5.hpf_cutoff = self.ui.spinBox_hpf_cutoff.value()
        self.process_h5.hpf_order = self.ui.spinBox_hpf_order.value()
        self.process_h5.glc_window = self.ui.spinBox_glc.value()
        self.process_h5.stft_win = self.ui.spinBox_window_size.value()
        self.process_h5.stft_ovl = self.ui.spinBox_stft_overlap.value()

        self.process_h5.process_once()


    # ==================================================
    def on_processing_ready(self, wf, psd, wf_var, new_phase):
        self.plotter.update_all(wf, psd, wf_var)
        self.new_phase = new_phase

        # ---- Spinbox limits (SAFE) ----
        self.ui.spinBox_row_no.setMaximum(max(0, wf.shape[0] - 1))

        self.ui.doubleSpinBox_wfrow.setMaximum(max(0, wf.shape[0] - 1))
        self.ui.doubleSpinBox_wfcolumn.setMaximum(max(0, wf.shape[1] - 1))

        self.ui.doubleSpinBox_specrow.setMaximum(max(0, psd.shape[0] - 1))
        self.ui.doubleSpinBox_speccol.setMaximum(max(0, psd.shape[1] - 1))

        self.ui.doubleSpinBox_stftcol.setMaximum(max(0, wf.shape[1] - 1))

    # ==================================================
    def update_raw_trace(self):
        wf = self.plotter.wf
        if wf is None:
            return

        row = int(self.ui.spinBox_row_no.value())
        row = max(0, min(row, wf.shape[0] - 1))

        self.ui.graphicsView_ch0_raw.clear()
        self.ui.graphicsView_ch1_raw.clear()

        # Raw trace = fast-time trace (same signal, different color)
        self.ui.graphicsView_ch0_raw.plot(
            wf[row],
            pen=pg.mkPen("yellow", width=2)
        )
        self.ui.graphicsView_ch1_raw.plot(
            wf[row],
            pen=pg.mkPen("cyan", width=2)
        )

    # ==================================================
    def plot_variance(self, state):
        self.ui.graphicsView_var.clear()

        if not state or self.plotter.wf_var is None:
            return

        var = np.nan_to_num(self.plotter.wf_var)

        self.ui.graphicsView_var.plot(
            var,
            pen=pg.mkPen("magenta", width=2)
        )

        self.ui.graphicsView_var.enableAutoRange()


    # ================= WATERFALL =================
    def update_wf_row(self):
        self.plotter.plot_wf_row(
            int(self.ui.doubleSpinBox_wfrow.value())
        )

    def update_wf_col(self):
        self.plotter.plot_wf_col(
            int(self.ui.doubleSpinBox_wfcolumn.value())
        )

    # ================= SPECTRUM =================
    def update_psd_row(self):
        self.plotter.plot_psd_row(
            int(self.ui.doubleSpinBox_specrow.value())
        )

    def update_psd_col(self):
        self.plotter.plot_psd_col(
            int(self.ui.doubleSpinBox_speccol.value())
        )

    # ================= STFT =================
    def update_stft(self):
        wf = self.plotter.wf
        if wf is None:
            return

        if self.process_h5.gui_attrs is not None:
            PRF = self.process_h5.gui_attrs["PRF"]
        else:
            PRF = self.import_h5.file_attrs.get("PRF")

        if PRF is None:
            return

        col = int(self.ui.doubleSpinBox_stftcol.value())
        col = max(0, min(col, wf.shape[1] - 1))

        nperseg = self.ui.spinBox_window_size.value()
        noverlap = self.ui.spinBox_stft_overlap.value()

        f, t, Zxx = self.process_h5.compute_stft(wf, col, PRF)
        self.plotter.update_stft(f, t, Zxx)






# ==================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
