import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
import threading
import configparser

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
DEFAULT_WINDOW_SIZE = "800x600"
DEFAULT_DURATION_SAMPLES = 10000
DEFAULT_CHANNELS = "0,50,100,150"
SAMPLING_RATE = 30000  # Hz
VOLTAGE_CONVERSION_FACTOR = 2.34 / 1000  # Convert to mV
CHANNEL_OFFSET = 0.5  # mV offset between channels

class DataLoader:
    """Loads and manages neural data from Neuropixel recordings."""

    def __init__(self, path, full_shape, dtype):
        """
        Initialize the DataLoader.

        Args:
            path (Path): Path to the data file.
            full_shape (tuple): Shape of the full dataset (channels, samples).
            dtype: Data type of the recording.
        """
        self.path = path
        self.full_shape = full_shape
        self.dtype = dtype
        self.file = None
        self.data = None
        self.loaded_channels = None

    def load_data(self, channels):
        """
        Load data for specified channels.

        Args:
            channels (list): List of channel indices to load.

        Raises:
            Exception: If there's an error loading the data.
        """
        try:
            logging.info(f"Opening file {self.path}")
            npx_recording = np.memmap(self.path, mode='r', dtype=self.dtype, order='C')
            npx_samples = int(len(npx_recording) / self.full_shape[0])
            npx_recording = npx_recording.reshape(self.full_shape, order='F')
            
            logging.info(f"Loading data for channels {channels}")
            self.data = npx_recording[channels, :] * VOLTAGE_CONVERSION_FACTOR
            self.loaded_channels = channels
            logging.info("Data loaded successfully")
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise

    def get_chunk(self, start, end):
        """
        Get a chunk of data for the loaded channels.

        Args:
            start (int): Start sample index.
            end (int): End sample index.

        Returns:
            numpy.ndarray: Chunk of data.

        Raises:
            ValueError: If data hasn't been loaded yet.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        return self.data[:, start:end]

class App(tk.Tk):
    """Main application for Neural Data Visualization."""

    def __init__(self):
        super().__init__()
        self.title("Neural Data Visualization")
        self.geometry(DEFAULT_WINDOW_SIZE)

        self.config = self.load_config()
        self.data_loader = DataLoader(
            Path(self.config.get('Data', 'file_path')),
            tuple(map(int, self.config.get('Data', 'shape').split(','))),
            np.int16
        )

        self.center_time = tk.DoubleVar(value=0)
        self.duration_samples = tk.IntVar(value=DEFAULT_DURATION_SAMPLES)
        self.channels = []
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.create_widgets()

    def load_config(self):
        """Load configuration from config.ini file."""
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    def create_widgets(self):
        """Create and arrange widgets in the application window."""
        self.create_center_time_widgets()
        self.create_duration_widgets()
        self.create_channel_selection_widgets()
        self.create_load_data_button()
        self.create_canvas()

    def create_center_time_widgets(self):
        ttk.Label(self, text="Center Time (s):").pack()
        center_time_frame = ttk.Frame(self)
        center_time_frame.pack(fill=tk.X, padx=10)
        
        self.center_time_entry = ttk.Entry(center_time_frame, width=10, textvariable=self.center_time)
        self.center_time_entry.pack(side=tk.LEFT)
        
        max_time = self.data_loader.full_shape[1] / SAMPLING_RATE
        self.center_time_slider = ttk.Scale(center_time_frame, from_=0, to=max_time,
                                            orient=tk.HORIZONTAL, variable=self.center_time, command=self.update_plot)
        self.center_time_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        ttk.Button(center_time_frame, text="Update", command=self.update_center_time).pack(side=tk.LEFT, padx=(10, 0))

    def create_duration_widgets(self):
        ttk.Label(self, text="Duration (samples):").pack()
        duration_frame = ttk.Frame(self)
        duration_frame.pack()
        self.duration_entry = ttk.Entry(duration_frame, width=10, textvariable=self.duration_samples)
        self.duration_entry.pack(side=tk.LEFT)
        ttk.Button(duration_frame, text="Update Duration", command=self.update_duration).pack(side=tk.LEFT)

    def create_channel_selection_widgets(self):
        ttk.Label(self, text="Channels (comma-separated):").pack()
        self.channel_entry = ttk.Entry(self, width=30)
        self.channel_entry.pack()
        self.channel_entry.insert(0, DEFAULT_CHANNELS)

    def create_load_data_button(self):
        ttk.Button(self, text="Load Data", command=self.load_data).pack(pady=10)

    def create_canvas(self):
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_data(self):
        """Load data for the specified channels."""
        try:
            channel_input = self.channel_entry.get()
            self.channels = [int(ch.strip()) for ch in channel_input.split(',')]
            self.data_loader.load_data(self.channels)
            self.update_plot()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def update_center_time(self):
        """Update the center time based on user input."""
        try:
            new_center_time = float(self.center_time_entry.get())
            max_time = self.data_loader.full_shape[1] / SAMPLING_RATE
            if 0 <= new_center_time <= max_time:
                self.center_time.set(new_center_time)
                self.center_time_slider.set(new_center_time)
                self.update_plot()
            else:
                messagebox.showwarning("Invalid Input", f"Center time must be between 0 and {max_time:.2f} seconds")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number for center time")

    def update_duration(self):
        """Update the duration based on user input."""
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
        """Update the plot with current settings."""
        if self.data_loader.data is None:
            return  # Don't update if no data is loaded

        center_time = self.center_time.get()
        duration_samples = self.duration_samples.get()
        half_duration_samples = duration_samples // 2
        start_sample = int(center_time * SAMPLING_RATE) - half_duration_samples
        end_sample = start_sample + duration_samples

        # Ensure start_sample is not negative
        if start_sample < 0:
            start_sample = 0
            end_sample = duration_samples

        # Ensure end_sample does not exceed data length
        if end_sample > self.data_loader.full_shape[1]:
            end_sample = self.data_loader.full_shape[1]
            start_sample = end_sample - duration_samples

        time = np.linspace(start_sample / SAMPLING_RATE, end_sample / SAMPLING_RATE, duration_samples)

        try:
            data_chunk = self.data_loader.get_chunk(start_sample, end_sample)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data chunk: {str(e)}")
            return

        self.ax.clear()
        for i, channel in enumerate(self.channels):
            self.ax.plot(time, data_chunk[i, :] + i*CHANNEL_OFFSET, linewidth=0.5)
            # Add horizontal zero line for each channel
            self.ax.axhline(y=i*CHANNEL_OFFSET, color='r', linestyle='-', linewidth=0.5, alpha=0.5)

        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Voltage (mV)')
        self.ax.set_title(f"Neural Data Visualization - Channels {self.channels}")
        
        # Set y-ticks to show actual voltage values
        y_ticks = np.arange(0, len(self.channels)*CHANNEL_OFFSET, CHANNEL_OFFSET)
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