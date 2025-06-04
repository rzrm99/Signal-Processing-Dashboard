import sys
import numpy as np
import pandas as pd
from scipy.signal import (
    butter, bessel, cheby1, cheby2, ellip, filtfilt
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QSlider, QFormLayout, QFileDialog,
    QCheckBox, QLabel, QLineEdit
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure


class SignalDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Signal Processing Dashboard")
        self.setGeometry(100, 100, 1400, 700)
        self.fs = 1000
        self.signal = np.zeros(self.fs)
        self.filtered_signal = self.signal
        self.t = np.linspace(0, 1, self.fs)
        self.initUI()
        self.last_params = {}

    def initUI(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        layout = QHBoxLayout(self.main_widget)

        # === Plot ===
        plot_layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        layout.addLayout(plot_layout, 2)

        # === Controls ===
        control_layout = QVBoxLayout()

        self.filter_type = QComboBox()
        self.filter_type.addItems(["None", "Low-pass", "High-pass", "Band-pass"])

        self.filter_family = QComboBox()
        self.filter_family.addItems(["Butterworth", "Bessel", "Chebyshev I", "Chebyshev II", "Elliptic", "Custom"])

        self.cutoff_slider = QSlider(Qt.Horizontal)
        self.cutoff_slider.setMinimum(1)
        self.cutoff_slider.setMaximum(500)
        self.cutoff_slider.setValue(10)
        self.cutoff_label = QLabel("Cutoff Freq 1: 10 Hz")

        self.cutoff_slider2 = QSlider(Qt.Horizontal)
        self.cutoff_slider2.setMinimum(1)
        self.cutoff_slider2.setMaximum(500)
        self.cutoff_slider2.setValue(30)
        self.cutoff_label2 = QLabel("Cutoff Freq 2: 30 Hz")

        self.order_slider = QSlider(Qt.Horizontal)
        self.order_slider.setMinimum(1)
        self.order_slider.setMaximum(10)
        self.order_slider.setValue(4)
        self.order_label = QLabel("Filter Order: 4")

        self.ripple_input = QLineEdit("1")   # For Chebyshev/elliptic
        self.atten_input = QLineEdit("20")

        self.b_input = QLineEdit("")
        self.a_input = QLineEdit("")

        self.show_original_checkbox = QCheckBox("Show Original Signal")
        self.show_original_checkbox.setChecked(True)

        self.load_btn = QPushButton("Load Signal (CSV)")
        self.reset_btn = QPushButton("Reset Zoom")

        # Form layout
        form = QFormLayout()
        form.addRow("Filter Type:", self.filter_type)
        form.addRow("Filter Family:", self.filter_family)
        form.addRow(self.cutoff_label, self.cutoff_slider)
        form.addRow(self.cutoff_label2, self.cutoff_slider2)
        form.addRow(self.order_label, self.order_slider)
        form.addRow("Ripple (dB):", self.ripple_input)
        form.addRow("Attenuation (dB):", self.atten_input)
        form.addRow("Custom b Coeffs (comma):", self.b_input)
        form.addRow("Custom a Coeffs (comma):", self.a_input)
        form.addRow(self.show_original_checkbox)

        control_layout.addLayout(form)
        control_layout.addWidget(self.load_btn)
        control_layout.addWidget(self.reset_btn)
        control_layout.addStretch()
        layout.addLayout(control_layout, 1)

        # Connect signals
        self.load_btn.clicked.connect(self.load_signal)
        self.reset_btn.clicked.connect(self.plot_signals)

        self.filter_type.currentIndexChanged.connect(self.apply_filter)
        self.filter_family.currentIndexChanged.connect(self.apply_filter)
        self.cutoff_slider.valueChanged.connect(self.update_cutoff1)
        self.cutoff_slider2.valueChanged.connect(self.update_cutoff2)
        self.order_slider.valueChanged.connect(self.update_order)
        self.ripple_input.textChanged.connect(self.apply_filter)
        self.atten_input.textChanged.connect(self.apply_filter)
        self.b_input.textChanged.connect(self.apply_filter)
        self.a_input.textChanged.connect(self.apply_filter)
        self.show_original_checkbox.stateChanged.connect(self.plot_signals)

        self.plot_signals()

    def load_signal(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        df = pd.read_csv(path)
        if 'time' not in df.columns or 'amplitude' not in df.columns:
            print("CSV must contain 'time' and 'amplitude'")
            return

        self.t = df['time'].values
        self.signal = df['amplitude'].values
        self.filtered_signal = self.signal.copy()

        dt = np.mean(np.diff(self.t))
        self.fs = int(1 / dt)
        nyq = self.fs // 2

        self.cutoff_slider.setMaximum(nyq - 1)
        self.cutoff_slider2.setMaximum(nyq - 1)

        self.apply_filter()

    def get_filter(self, ftype, family, cutoff1, cutoff2, order, ripple, atten):
        nyq = 0.5 * self.fs
        norm1 = cutoff1 / nyq
        norm2 = cutoff2 / nyq
        b, a = None, None

        try:
            if family == "Butterworth":
                b, a = butter(order, [norm1, norm2] if ftype == "band" else norm1, btype=ftype)
            elif family == "Bessel":
                b, a = bessel(order, [norm1, norm2] if ftype == "band" else norm1, btype=ftype)
            elif family == "Chebyshev I":
                b, a = cheby1(order, ripple, [norm1, norm2] if ftype == "band" else norm1, btype=ftype)
            elif family == "Chebyshev II":
                b, a = cheby2(order, atten, [norm1, norm2] if ftype == "band" else norm1, btype=ftype)
            elif family == "Elliptic":
                b, a = ellip(order, ripple, atten, [norm1, norm2] if ftype == "band" else norm1, btype=ftype)
            elif family == "Custom":
                b_text = self.b_input.text().strip()
                a_text = self.a_input.text().strip()
                b = np.fromstring(b_text, sep=',') if b_text else None
                a = np.fromstring(a_text, sep=',') if a_text else None
        except Exception as e:
            print(f"[Filter generation error] {e}")
            b, a = None, None

        return b, a

    # def apply_filter(self):
    #     if len(self.signal) == 0:
    #         return
    #
    #     ftype_map = {"Low-pass": "low", "High-pass": "high", "Band-pass": "band"}
    #     ftype = ftype_map.get(self.filter_type.currentText(), None)
    #     family = self.filter_family.currentText()
    #     cutoff1 = self.cutoff_slider.value()
    #     cutoff2 = self.cutoff_slider2.value()
    #     order = self.order_slider.value()
    #
    #     try:
    #         ripple = float(self.ripple_input.text())
    #         atten = float(self.atten_input.text())
    #     except:
    #         ripple, atten = 1, 20
    #
    #     if ftype is None or family == "None":
    #         self.filtered_signal = self.signal
    #     else:
    #         b, a = self.get_filter(ftype, family, cutoff1, cutoff2, order, ripple, atten)
    #         if b is None or a is None:
    #             print("[Warning] Invalid filter, using original signal.")
    #             self.filtered_signal = self.signal
    #         else:
    #             try:
    #                 self.filtered_signal = filtfilt(b, a, self.signal)
    #                 print(f"[Filter applied] {family}, Type: {ftype}, Order: {order}")
    #             except Exception as e:
    #                 print(f"[Filtering error] {e}")
    #                 self.filtered_signal = self.signal
    #
    #     self.plot_signals()

    def apply_filter(self):
        if len(self.signal) == 0:
            return

        ftype_map = {"Low-pass": "low", "High-pass": "high", "Band-pass": "band"}
        ftype = ftype_map.get(self.filter_type.currentText(), None)
        family = self.filter_family.currentText()
        cutoff1 = self.cutoff_slider.value()
        cutoff2 = self.cutoff_slider2.value()
        order = self.order_slider.value()

        try:
            ripple = float(self.ripple_input.text())
            atten = float(self.atten_input.text())
        except:
            ripple, atten = 1, 20

        # 🚫 Prevent redundant reapplication
        current_params = (
        ftype, family, cutoff1, cutoff2, order, ripple, atten, self.b_input.text(), self.a_input.text())
        if current_params == self.last_params:
            return
        self.last_params = current_params

        if ftype is None or family == "None":
            self.filtered_signal = self.signal
        else:
            b, a = self.get_filter(ftype, family, cutoff1, cutoff2, order, ripple, atten)
            if b is None or a is None:
                print("[Warning] Invalid filter, using original signal.")
                self.filtered_signal = self.signal
            else:
                try:
                    self.filtered_signal = filtfilt(b, a, self.signal)
                    print(f"[Filter applied] {family}, Type: {ftype}, Order: {order}")
                except Exception as e:
                    print(f"[Filtering error] {e}")
                    self.filtered_signal = self.signal

        self.plot_signals()

    def plot_signals(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if self.show_original_checkbox.isChecked():
            ax.plot(self.t, self.signal, label="Original", alpha=0.5)
        ax.plot(self.t, self.filtered_signal, label="Filtered", linewidth=2)
        ax.set_title("Signal Viewer")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        ax.legend()
        self.canvas.draw()

    def update_cutoff1(self, val):
        self.cutoff_label.setText(f"Cutoff Freq 1: {val} Hz")
        self.apply_filter()

    def update_cutoff2(self, val):
        self.cutoff_label2.setText(f"Cutoff Freq 2: {val} Hz")
        self.apply_filter()

    def update_order(self, val):
        self.order_label.setText(f"Filter Order: {val}")
        self.apply_filter()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalDashboard()
    window.show()
    sys.exit(app.exec_())

