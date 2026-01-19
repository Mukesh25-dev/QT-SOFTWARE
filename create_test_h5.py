import h5py
import numpy as np

file_name = "test_das.h5"

# Create dummy DAS-like data
PRF = 100
TIME_FRAMES = 50
SAMPLES = 1500


Ch_A = np.random.randn(PRF * TIME_FRAMES, SAMPLES).astype(np.float32)
Ch_B = np.random.randn(PRF * TIME_FRAMES, SAMPLES).astype(np.float32)

with h5py.File(file_name, "w") as f:
    f.create_dataset("Ch_A", data=Ch_A)
    f.create_dataset("Ch_B", data=Ch_B)

    # Root attributes (VERY IMPORTANT)
    f.attrs["Fiber_len(m)"] = 1000.0
    f.attrs["Capture_duration(s)"] = TIME_FRAMES
    f.attrs["Trig_PRF(Hz)"] = PRF
    f.attrs["Sampling rate(MSPS)"] = 10.0
    f.attrs["Trig_pulse_width(ns)"] = 100
    f.attrs["Trigger_delay(ns)"] = 0
    f.attrs["DAS hardware"] = "IITM DAS - I, Q"

print("✅ test_das.h5 created successfully")
