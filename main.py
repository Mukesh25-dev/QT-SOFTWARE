import sys
import numpy as np

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from form import Ui_MainWindow
from import_h5 import Import_H5, Process_h5_file, PlotterH5


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.import_h5 = Import_H5(self)
        self.process_h5 = Process_h5_file(self)
        self.plotter = PlotterH5(self)

        self.chA = None
        self.chB = None
        self.variance = None

        self.process_h5.sig_plot_ready.connect(
            self.plotter.update_waterfall
        )

        self.ui.pushButton_choose.clicked.connect(self.import_h5.get_file_path)
        self.ui.pushButton_read_attr.clicked.connect(self.show_attributes)
        self.ui.pushButton_process_file.clicked.connect(self.run_processing)

        # Waterfall slice
        self.ui.pushButton.clicked.connect(self.view_row_col)

        # Spectrum slice
        self.ui.pushButton_2.clicked.connect(self.view_spectrum_row_col)

        # Raw trace
        self.ui.spinBox_row_no.valueChanged.connect(self.update_raw_trace)

        # Variance
        self.ui.checkBox_variance.stateChanged.connect(self.plot_variance)

        self.plotter.init_waterfall_plots()

    # -----------------------------------------
    def show_attributes(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Attribute", "Value"])

        # File path first
        model.appendRow([
            QStandardItem("File path"),
            QStandardItem(self.import_h5.file_path)
        ])

        # All H5 attributes
        for key, value in self.import_h5.attrs.items():
            model.appendRow([
                QStandardItem(str(key)),
                QStandardItem(str(value))
            ])

        self.ui.tableView_attr.setModel(model)
        self.ui.tableView_attr.resizeColumnsToContents()

    # -----------------------------------------
    def run_processing(self):
        if not self.import_h5.file_path:
            return

        self.process_h5.file_path = self.import_h5.file_path

        # ✅ Load correct datasets
        self.chA = self.process_h5.load_channel("I_channel")
        self.chB = self.process_h5.load_channel("Q_channel")

        if self.chA is None:
            print("❌ I_channel not loaded")
            return

        # ✅ Variance across time (rows)
        # Shape assumption: (rows, columns)
        self.variance = np.var(self.chA, axis=0)

        # ✅ Waterfall + Spectrum
        self.process_h5.process_once()

        # ✅ Raw trace initial plot
        self.update_raw_trace(self.ui.spinBox_row_no.value())

    # -----------------------------------------
    def update_raw_trace(self, row):
        if self.chA is None:
            return

        self.ui.graphicsView_ch0_raw.clear()
        self.ui.graphicsView_ch1_raw.clear()

        self.ui.graphicsView_ch0_raw.plot(self.chA[row], pen="y")
        self.ui.graphicsView_ch0_raw.setTitle(f"Ch A – Row {row}")

        if self.chB is not None:
            self.ui.graphicsView_ch1_raw.plot(self.chB[row], pen="c")
            self.ui.graphicsView_ch1_raw.setTitle(f"Ch B – Row {row}")

    # -----------------------------------------
    def plot_variance(self, state):
        self.ui.graphicsView_var.clear()

        if state == 0 or self.variance is None:
            return

        self.ui.graphicsView_var.plot(self.variance, pen="m")
        self.ui.graphicsView_var.setTitle("Variance vs Distance")

    # -----------------------------------------
    def view_row_col(self):
        row = int(self.ui.doubleSpinBox.value())
        col = int(self.ui.doubleSpinBox_2.value())

        self.plotter.plot_row_col(row, col)

    def view_spectrum_row_col(self):
        row = int(self.ui.doubleSpinBox_3.value())
        col = int(self.ui.doubleSpinBox_4.value())

        print("Spectrum slice requested → Row:", row, "Col:", col)

        self.plotter.plot_psd_row_col(row, col)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
