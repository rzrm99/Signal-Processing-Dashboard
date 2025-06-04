# Signal-Processing-Dashboard

# Signal Processing Dashboard (PyQt + Matplotlib)

A fully interactive signal processing dashboard built with **PyQt5** and **Matplotlib**, supporting real-time filtering, visualization, and analysis of signals loaded from CSV files.

---

## 📌 Features

- ✅ Load signals from `.csv` files (`time, amplitude`)
- ✅ Visualize original and filtered signals
- ✅ Real-time filter updates as parameters change
- ✅ Support for multiple filter families:
  - Butterworth
  - Bessel
  - Chebyshev I
  - Chebyshev II
  - Elliptic
  - Custom (user-defined `b`, `a` coefficients)
- ✅ Adjustable parameters:
  - Filter type (low-pass, high-pass, band-pass)
  - Cutoff frequencies
  - Filter order
  - Ripple (for Chebyshev/elliptic)
  - Attenuation (for Chebyshev II/elliptic)
- ✅ Interactive zoom and pan (via matplotlib toolbar)
- ✅ Reset zoom button
- ✅ Toggle to show/hide original signal

---

## ⚠️ Disclaimer

This project is intended for educational and research use only.

While care has been taken to implement correct signal processing behavior, the tool is not intended for production use in medical, safety-critical, or financial applications. Use it at your own risk.

---

## 🧪 Example Signals

You can generate test signals like sine, square, sawtooth, or noisy waveforms and save them in CSV format using the included generator script (see `generate_signals.py`).

CSV format expected:

```csv
time,amplitude
0.000,0.00
0.001,0.31
...

