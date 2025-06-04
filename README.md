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

## 🧪 Example Signals

You can generate test signals like sine, square, sawtooth, or noisy waveforms and save them in CSV format using the included generator script (see `generate_signals.py`).

CSV format expected:

```csv
time,amplitude
0.000,0.00
0.001,0.31
...

## ⚠️ Disclaimer

This project is intended for educational and research use only.

    While care has been taken to implement correct signal processing behavior, the tool is not intended for production use in medical, safety-critical, or financial applications. Use it at your own risk.


## Licencse
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
