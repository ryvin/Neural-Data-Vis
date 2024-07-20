import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
import threading

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLoader:
    def __init__(self, path, full_shape, dtype):
        self.path = path
        self.full_shape = full_shape
        self.dtype = dtype
        self.file = None
        self.data = None
        self.loaded_channels = None

    def load_data(self, channels):
        try:
            logging.info(f"Opening file {self.path}")
            npx_recording = np.memmap(self.path, mode='r', dtype=np.int16, order='C')
            npx_samples = int(len(npx_recording) / self.full_shape[0])
            npx_recording = npx_recording.reshape((self.full_shape[0], npx_samples), order='F')
            
            logging.info(f"Loading data for channels {channels}")
            self.data = npx_recording[channels, :] * 2.34 / 1000  # Convert to mV
            self.loaded_channels = channels
            logging.info("Data loaded successfully")
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise

    def get_chunk(self, start, end):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        return self.data[:, start:end]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Neural Data Visualization")
        self.geometry("800x600")

        self.data_loader = DataLoader(
            Path("C:/Datasets/CRCNS/spe-1/data/c45/c45_npx_raw-001.bin"),
            (384, 24301033),
            np.int16
        )

        self.center_time = tk.DoubleVar(value=0)
        self.duration_samples = tk.IntVar(value=10000)  # Default 10000 samples
        self.channels = []
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.create_widgets()

    def create_widgets(self):
        # Center Time
        ttk.Label(self, text="Center Time (s):").pack()
        center_time_frame = ttk.Frame(self)
        center_time_frame.pack(fill=tk.X, padx=10)
        
        self.center_time_entry = ttk.Entry(center_time_frame, width=10, textvariable=self.center_time)
        self.center_time_entry.pack(side=tk.LEFT)
        
        max_time = self.data_loader.full_shape[1] / 30000  # Assuming 30 kHz sampling rate
        self.center_time_slider = ttk.Scale(center_time_frame, from_=0, to=max_time,
                                            orient=tk.HORIZONTAL, variable=self.center_time, command=self.update_plot)
        self.center_time_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        ttk.Button(center_time_frame, text="Update", command=self.update_center_time).pack(side=tk.LEFT, padx=(10, 0))

        # Duration
        ttk.Label(self, text="Duration (samples):").pack()
        duration_frame = ttk.Frame(self)
        duration_frame.pack()
        self.duration_entry = ttk.Entry(duration_frame, width=10, textvariable=self.duration_samples)
        self.duration_entry.pack(side=tk.LEFT)
        ttk.Button(duration_frame, text="Update Duration", command=self.update_duration).pack(side=tk.LEFT)

        # Channel Selection
        ttk.Label(self, text="Channels (comma-separated):").pack()
        self.channel_entry = ttk.Entry(self, width=30)
        self.channel_entry.pack()
        self.channel_entry.insert(0, "0,50,100,150")  # Default channels

        # Load Data Button
        ttk.Button(self, text="Load Data", command=self.load_data).pack(pady=10)

        # Canvas
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_data(self):
        try:
            channel_input = self.channel_entry.get()
            self.channels = [int(ch.strip()) for ch in channel_input.split(',')]
            self.data_loader.load_data(self.channels)
            self.update_plot()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def update_center_time(self):
        try:
            new_center_time = float(self.center_time_entry.get())
            max_time = self.data_loader.full_shape[1] / 30000
            if 0 <= new_center_time <= max_time:
                self.center_time.set(new_center_time)
                self.center_time_slider.set(new_center_time)
                self.update_plot()
            else:
                messagebox.showwarning("Invalid Input", f"Center time must be between 0 and {max_time:.2f} seconds")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number for center time")

    def update_duration(self):
        try:
            new_duration = int(self.duration_entry.get())
            if 100 <= new_duration <= self.data_loader.full_shape[1]:
                self.duration_samples.set(new_duration)
                self.update_plot()
            else:
                messagebox.showwarning("Invalid Input", f"Duration must be between 100 and {self.data_loader.full_shape[1]} samples")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid integer for duration")

    def update_plot(self, *args):
        if self.data_loader.data is None:
            return  # Don't update if no data is loaded

        center_time = self.center_time.get()
        duration_samples = self.duration_samples.get()
        half_duration_samples = duration_samples // 2
        start_sample = int(center_time * 30000) - half_duration_samples
        end_sample = start_sample + duration_samples

        # Ensure start_sample is not negative
        if start_sample < 0:
            start_sample = 0
            end_sample = duration_samples

        # Ensure end_sample does not exceed data length
        if end_sample > self.data_loader.full_shape[1]:
            end_sample = self.data_loader.full_shape[1]
            start_sample = end_sample - duration_samples

        time = np.linspace(start_sample / 30000, end_sample / 30000, duration_samples)

        try:
            data_chunk = self.data_loader.get_chunk(start_sample, end_sample)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data chunk: {str(e)}")
            return

        self.ax.clear()
        offset = 0.5  # 0.5 mV offset between channels
        for i, channel in enumerate(self.channels):
            self.ax.plot(time, data_chunk[i, :] + i*offset, linewidth=0.5)
            # Add horizontal zero line for each channel
            self.ax.axhline(y=i*offset, color='r', linestyle='-', linewidth=0.5, alpha=0.5)

        # Add vertical line at center time
        # self.ax.axvline(x=center_time, color='g', linestyle='--', linewidth=1)

        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Voltage (mV)')
        self.ax.set_title(f"Neural Data Visualization - Channels {self.channels}")
        
        # Set y-ticks to show actual voltage values
        y_ticks = np.arange(0, len(self.channels)*offset, offset)
        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels([f'{tick:.2f}' for tick in y_ticks])
        
        self.ax.grid(True)

        self.canvas.draw()

if __name__ == "__main__":
    try:
        logging.info("Starting application")
        app = App()
        app.mainloop()
    except Exception as e:
        logging.error(f"Error in main application: {e}")
        raise