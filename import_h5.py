import h5py
import numpy as np

import cupy as cp
from cupy import fft
from cupyx.scipy import signal, ndimage
from scipy.signal import stft

from PySide6.QtCore import QObject, Signal
import os
os.environ["QT_API"] = "pyside6"

import pyqtgraph as pg


# =========================================================
# Butterworth HPF (GPU)
# =========================================================
def butterHigh(cutoff, critical, order):
    normal_cutoff = float(cutoff) / critical
    b, a = signal.butter(order, normal_cutoff, btype='highpass')
    return b, a


def butterFilter(data, cutoff_freq, freq, order):
    nyq_freq = freq // 2
    b, a = butterHigh(cutoff_freq, nyq_freq, order)
    return signal.filtfilt(b, a, data)


# =========================================================
# IMPORT H5
# =========================================================
class Import_H5(QObject):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.ui = main.ui
        self.file_path = ""
        self.file_attrs = {}

        self.hpf_cutoff = 60
        self.hpf_order = 2
        self.glc_window = 1
        self.stft_win = 1024
        self.stft_ovl = 512

    def get_file_path(self):
        from PySide6.QtWidgets import QFileDialog

        self.file_path, _ = QFileDialog.getOpenFileName(
            None, "Select H5 file", "", "H5 Files (*.h5)"
        )

        self.ui.lineEdit.setText(self.file_path)

        if not self.file_path:
            return

        with h5py.File(self.file_path, "r") as f:
            self.file_attrs = dict(f.attrs)
            print("Root keys:", list(f.keys()))




# =========================================================
# PROCESS H5 (CORE DSP — UNCHANGED)
# =========================================================
class Process_h5_file(QObject):
    sig_plot_ready = Signal(object, object, object, object)

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.file_path = ""

        self.gui_ch1 = None
        self.gui_ch2 = None
        self.gui_attrs = None

        self.hpf_cutoff = 60
        self.hpf_order = 2
        self.glc_window = 1
        self.stft_win = 1024
        self.stft_ovl = 512

    def _get_attr(self, attrs, names):
        for n in names:
            if n in attrs:
                return attrs[n]
        return None
    
    def set_gui_data(self, ch1, ch2, attrs):
        self.gui_ch1 = ch1
        self.gui_ch2 = ch2
        self.gui_attrs = attrs
    
    # glc_window intentionally disabled to match reference DSP
    #hpf_cutoff, hpf_order, glc_window
    def process_once(self):

        # ---------- DATA SOURCE SELECTION ----------
        if self.gui_ch1 is not None:
            # GUI-acquired data
            ch1 = self.gui_ch1
            ch2 = self.gui_ch2
            sample_rate = self.gui_attrs["sample_rate"]
            sample_length = self.gui_attrs["sample_length"]
            PRF = self.gui_attrs["PRF"]

        else:
            # H5 file data
            if not self.file_path:
                return

            with h5py.File(self.file_path, "r") as f:
                ch1 = f['I_channel'][:]
                ch2 = f['Q_channel'][:]
                sample_rate = f.attrs['sample_rate']
                sample_length = f.attrs['sample_length']
                PRF = f.attrs['PRF']


        # ---------------- PDR PARAMETERS ----------------
        fiblen_actual = int(70e3)
        pulselength = 100  # ns

        stop = sample_length / sample_rate
        no_traces = int(stop * PRF)

        pulse_width = pulselength * 1e-9
        start = int(pulse_width * sample_rate)
        if start <= 0:
            raise ValueError("Invalid pulse width → start = 0")


        # ---------------- CORE DSP ----------------
        c3_trace = (ch1 + ch2) * 0.5
        c3_trace = cp.asarray(c3_trace[:no_traces, :fiblen_actual])

        c3_trace = (c3_trace.T - cp.mean(c3_trace, axis=1)).T
        c3_trace = fft.fftshift(fft.fft(c3_trace, axis=-1))
        c3_trace[:, :c3_trace.shape[1] // 2] = 0
        c3_trace = fft.ifft(fft.ifftshift(c3_trace), axis=-1)

        phase = cp.arctan2(cp.imag(c3_trace), cp.real(c3_trace))
        shift = start * self.glc_window
        phase = phase[:, shift:] - phase[:, :-shift]


        new_phase = cp.unwrap(phase, axis=0)
        new_phase -= cp.mean(new_phase, axis=0)
        new_phase -= new_phase[0, :]
        new_phase = signal.detrend(new_phase, axis=0)
        new_phase = ndimage.median_filter(new_phase, size=(1, start))
        new_phase = signal.savgol_filter(new_phase, start, 1, axis=1)

        #new_phase = butterFilter(new_phase.T, hpf_cutoff, PRF, hpf_order).T
        new_phase = butterFilter(new_phase.T, self.hpf_cutoff, PRF, self.hpf_order).T


        _, Pxx = signal.periodogram(new_phase, PRF, axis=0)


        wf = new_phase.get()
        psd = Pxx.get()
        wf_var = np.var(wf, axis=0)
        wf_var[0] = 0   # remove reference-trace artefact

        

        self.sig_plot_ready.emit(wf, psd, wf_var, new_phase)

    def compute_stft(self, wf, col, PRF):
        win = self.stft_win
        ovl = self.stft_ovl

        sig = wf[:, col]
        f, t, Zxx = stft(sig, fs=PRF, nperseg=win, noverlap=ovl)
        return f, t, 20 * np.log10(np.abs(Zxx) + 1e-12)

    # =========================================================
    # F-K FILTER DESIGN
    # =========================================================
    def fk_filter_design(self, trace_shape, selected_channels, dx, fs,
                         cs_min=1400, cp_min=1450, cp_max=3400, cs_max=3500):

        nnx, nns = trace_shape

        freq = np.fft.fftshift(np.fft.fftfreq(nns, d=1/fs))
        knum = np.fft.fftshift(np.fft.fftfreq(nnx, d=selected_channels[2]*dx))

        np.seterr(invalid='ignore')

        fk_filter_matrix = np.zeros((len(knum), len(freq)))

        for i in range(len(knum)):
            if abs(knum[i]) < 0.005:
                continue

            speed = abs(freq / knum[i])
            line = np.ones_like(freq)

            mask = ((speed >= cs_min) & (speed <= cp_min))
            line[mask] = np.sin(
                0.5*np.pi*(speed[mask]-cs_min)/(cp_min-cs_min)
            )

            mask = ((speed >= cp_max) & (speed <= cs_max))
            line[mask] = 1 - np.sin(
                0.5*np.pi*(speed[mask]-cp_max)/(cs_max-cp_max)
            )

            line[speed >= cs_max] = 0
            line[speed < cs_min] = 0

            fk_filter_matrix[i] = line

        return fk_filter_matrix


    # =========================================================
    # APPLY FK FILTER
    # =========================================================
    def fk_filter_apply(self, trace, fk_filter_matrix):
        fk_trace = np.fft.fftshift(np.fft.fft2(trace))
        fk_filtered = fk_trace * fk_filter_matrix
        trace = np.fft.ifft2(np.fft.ifftshift(fk_filtered))
        return trace.real


    # =========================================================
    # FK MAIN CALL (FOR UI BUTTON)
    # =========================================================
    def compute_fk(self, wf, PRF, cs_min, cp_min, cp_max, cs_max):

        if wf is None:
            print("WF not ready")
            return None

        wf_t = wf.T
        trace_shape = wf_t.shape

        selected_channels = (1, trace_shape[0], 1)
        dx = 1
        fs = PRF

        fk_matrix = self.fk_filter_design(
            trace_shape,
            selected_channels,
            dx,
            fs,
            cs_min, cp_min, cp_max, cs_max
        )

        wf_fk = self.fk_filter_apply(wf_t, fk_matrix)
        wf_fk = wf_fk.T

        return wf_fk



# =========================================================
# PLOTTER (DISPLAY = PDR STYLE)
# =========================================================
class PlotterH5(QObject):
    def __init__(self, main):
        super().__init__()
        self.ui = main.ui
        self.wf = None
        self.psd = None
        self.wf_var = None

    def _sync_top_axis(self, vb, axis):
        def update():
            x0, x1 = vb.viewRange()[0]
            axis.setRange(x0, x1)

        vb.sigXRangeChanged.connect(lambda *_: update())
        update()

    def init_waterfall_plots(self):
        self.ui.graphicsView_wf.clear()
        self.ui.graphicsView_psd.clear()

        # ---------- Image items ----------
        self.wf_img = pg.ImageItem()
        self.psd_img = pg.ImageItem()

        jet = pg.colormap.get("jet")

        self.wf_img.setColorMap(jet)
        self.psd_img.setColorMap(jet)

        self.ui.graphicsView_wf.addItem(self.wf_img)
        self.ui.graphicsView_psd.addItem(self.psd_img)

        # ---------- WATERFALL TOP AXIS ----------
        wf_plot = self.ui.graphicsView_wf.getPlotItem()
        self.top_axis = pg.AxisItem("top")
        wf_plot.layout.addItem(self.top_axis, 1, 1)
        self.top_axis.setZValue(10)

        # ---------- SPECTRUM TOP AXIS ----------
        psd_plot = self.ui.graphicsView_psd.getPlotItem()
        self.psd_top_axis = pg.AxisItem("top")
        psd_plot.layout.addItem(self.psd_top_axis, 1, 1)
        self.psd_top_axis.setZValue(10)

        # ---------- View settings ----------
        wf_plot.vb.invertY(True)
        wf_plot.vb.setAspectLocked(False)

        psd_plot.vb.invertY(True)

        self._sync_top_axis(wf_plot.vb, self.top_axis)
        self._sync_top_axis(psd_plot.vb, self.psd_top_axis)



    def update_all(self, wf, psd, wf_var):
        self.wf = wf
        self.psd = psd
        self.wf_var = wf_var

        rows, cols = wf.shape

        # ---------- WATERFALL ----------
        self.wf_img.setImage(wf, autoLevels=True)

        fiber_length_km = 70.0
        time_ms = 1000.0

        self.wf_img.setRect(0, 0, fiber_length_km, time_ms)
        wf_vb = self.ui.graphicsView_wf.getViewBox()
        wf_vb.setXRange(0, fiber_length_km, padding=0)
        wf_vb.setYRange(0, time_ms, padding=0)


        # ---------- SPECTRUM ----------
        psd_db = 10 * np.log10(psd + 1e-12)

        self.psd_img.setImage(psd_db, autoLevels=False)
        self.psd_img.setLevels([-120, -40])   


        freq_max_hz = 500.0  # PRF / 2
        self.psd_img.setRect(0, 0, fiber_length_km, freq_max_hz)
        psd_vb = self.ui.graphicsView_psd.getViewBox()
        psd_vb.setXRange(0, fiber_length_km, padding=0)
        psd_vb.setYRange(0, freq_max_hz, padding=0)


        # --------- AXES  ----------
        # Bottom X (km)
        ax = self.ui.graphicsView_wf.getAxis("bottom")
        ax.setLabel("Position (km)")
        ax.setTicks([[(i, str(i)) for i in range(0, 71, 10)]])

        # Left Y (ms)
        ay = self.ui.graphicsView_wf.getAxis("left")
        ay.setLabel("Time (ms)")
        ay.setTicks([[(i, str(i)) for i in range(0, 1001, 200)]])

        self.top_axis.setLabel("Position (km)")
        self.top_axis.setTicks([[
            (i, str(i)) for i in range(0, int(fiber_length_km) + 1, 10)
        ]])


        # --------- SPECTRUM AXES ----------
        # Bottom X (km)
        ax = self.ui.graphicsView_psd.getAxis("bottom")
        ax.setLabel("Position (km)")
        ax.setTicks([[(i, str(i)) for i in range(0, 71, 10)]])

        # Left Y (Hz)
        ay = self.ui.graphicsView_psd.getAxis("left")
        ay.setLabel("Frequency (Hz)")
        ay.setTicks([[(i, str(i)) for i in range(0, 501, 100)]])

        # Top X (trace index)
        self.psd_top_axis.setLabel("Position (km)")
        self.psd_top_axis.setTicks([[
            (i, str(i)) for i in range(0, int(fiber_length_km) + 1, 10)
        ]])



    # ---------- SLICES ----------
    def plot_wf_row(self, row):
        if self.wf is None:
            return

        row = max(0, min(row, self.wf.shape[0] - 1))
        self.ui.graphicsView_wf_row.clear()
        self.ui.graphicsView_wf_row.plot(self.wf[row, :])



    def plot_wf_col(self, col):
        if self.wf is None:
            return

        col = max(0, min(col, self.wf.shape[1] - 1))
        self.ui.graphicsView_wf_col.clear()
        self.ui.graphicsView_wf_col.plot(self.wf[:, col])



    def plot_psd_row(self, row):
        self.ui.graphicsView_psd_row.clear()
        self.ui.graphicsView_psd_row.plot(self.psd[row])

    def plot_psd_col(self, col):
        self.ui.graphicsView_psd_col.clear()
        self.ui.graphicsView_psd_col.plot(self.psd[:, col])

    def init_stft_plot(self):
        self.ui.graphicsView_stft.clear()
        self.stft_img = pg.ImageItem()
        self.stft_img.setColorMap(pg.colormap.get("jet"))
        self.ui.graphicsView_stft.addItem(self.stft_img)

    def update_stft(self, f, t, Zxx_db):
        self.stft_img.resetTransform()

        self.stft_img.setImage(Zxx_db, autoLevels=False)
        self.stft_img.setLevels([-80, -20])    

        # Map to physical units (same as matplotlib extent)
        self.stft_img.setRect(
            t.min(),                 # Time start (sec)
            f.min(),                 # Frequency start (Hz)
            t.max() - t.min(),       # Time width
            f.max() - f.min()        # Frequency height
        )

        vb = self.ui.graphicsView_stft.getViewBox()
        vb.setXRange(t.min(), t.max(), padding=0)
        vb.setYRange(f.min(), f.max(), padding=0)

        # Axis labels
        ax = self.ui.graphicsView_stft.getAxis("bottom")
        ax.setLabel("Time (sec)")

        ay = self.ui.graphicsView_stft.getAxis("left")
        ay.setLabel("Frequency (Hz)")


    # =========================================================
    # FK DISPLAY
    # =========================================================
    def init_fk_plot(self):
        self.ui.graphicsView.clear()

        self.fk_img = pg.ImageItem()
        self.fk_img.setColorMap(pg.colormap.get("jet"))

        self.ui.graphicsView.addItem(self.fk_img)
        self.ui.graphicsView.getViewBox().invertY(True)

    def update_fk(self, wf_fk):
        if wf_fk is None:
            return

        self.fk_img.setImage(wf_fk, autoLevels=True)



