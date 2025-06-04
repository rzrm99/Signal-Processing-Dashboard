import numpy as np
import pandas as pd
from scipy import signal
from scipy.io.wavfile import write
import os

# Output directory
output_dir = "generated_signals"
os.makedirs(output_dir, exist_ok=True)

# Parameters
fs = 1000  # Sample rate
duration = 2  # seconds
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Define signals
signals = {
    "sine_5Hz": np.sin(2 * np.pi * 5 * t),
    "sine_50Hz": np.sin(2 * np.pi * 50 * t),
    "square_5Hz": signal.square(2 * np.pi * 5 * t),
    "sawtooth_5Hz": signal.sawtooth(2 * np.pi * 5 * t),
    "mixed": (
        np.sin(2 * np.pi * 5 * t) +
        0.5 * np.sin(2 * np.pi * 20 * t) +
        0.3 * signal.square(2 * np.pi * 10 * t)
    ),
    "noisy_sine": np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 0.3, len(t))
}

# Save signals to CSV and WAV
for name, data in signals.items():
    df = pd.DataFrame({'time': t, 'amplitude': data})
    csv_path = os.path.join(output_dir, f"{name}.csv")
    df.to_csv(csv_path, index=False)

    # Normalize to int16 range for WAV
    wav_data = np.int16(data / np.max(np.abs(data)) * 32767)
    wav_path = os.path.join(output_dir, f"{name}.wav")
    write(wav_path, fs, wav_data)

print(f"Saved signals to: {output_dir}")
