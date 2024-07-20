# Neural Data Visualization Tool

This tool provides a graphical user interface for visualizing neural data recorded from Neuropixel probes. It allows users to load specific channels of data, navigate through the recording in time, and visualize voltage traces for selected channels.

## Features

- Load and visualize data from Neuropixel recordings
- Select specific channels for visualization
- Adjust the time window and duration of the displayed data
- Real-time updates of the visualization as parameters are changed
- Display voltage traces in millivolts (mV)
- Configurable data source and parameters via config.ini file

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed
- pip (Python package installer)

## Installation

1. Clone this repository or download the script to your local machine.

2. Navigate to the directory containing the script in your terminal or command prompt.

3. Install the required Python packages by running:

   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a file named `config.ini` in the same directory as the script with the following content:

   ```ini
   [Data]
   file_path = /path/to/your/neuropixel/data.bin
   shape = 384,24301033
   ```

   Replace `/path/to/your/neuropixel/data.bin` with the actual path to your Neuropixel recording file.

2. Adjust the `shape` parameter to match your data:
   - The first number is the total number of channels in your Neuropixel probe.
   - The second number is the total number of time samples in your recording.

   For example, for a 15-minute recording at 30 kHz sampling rate with 384 channels:
   ```ini
   shape = 384,27000000
   ```

   (27000000 = 15 minutes * 60 seconds * 30000 samples/second)

## Running the Application

1. Open a terminal or command prompt.
2. Navigate to the directory containing the script.
3. Run the script using Python:

   ```
   python Neural_Data_Visualization.py
   ```

4. The application window should appear.

## Using the Application

1. Enter the channel numbers you want to visualize in the "Channels" field, separated by commas (e.g., "0,50,100,150").
2. Click the "Load Data" button to load the specified channels.
3. Use the "Center Time" slider or entry field to navigate through the recording.
4. Adjust the "Duration" field to change the time window of data displayed.
5. Click "Update" or "Update Duration" to refresh the plot with new parameters.

## Customization

You can customize various aspects of the visualization by modifying the constants at the top of the `Neural_Data_Visualization.py` file:

- `DEFAULT_WINDOW_SIZE`: Initial size of the application window
- `DEFAULT_DURATION_SAMPLES`: Default number of samples to display
- `DEFAULT_CHANNELS`: Default channels to load
- `SAMPLING_RATE`: Sampling rate of the recording in Hz
- `VOLTAGE_CONVERSION_FACTOR`: Factor to convert raw values to millivolts
- `CHANNEL_OFFSET`: Vertical offset between channels in the plot

## Troubleshooting

- If you encounter any errors related to missing packages, ensure you've installed all required dependencies using the `requirements.txt` file.
- If the data doesn't load, double-check that the file path and shape in `config.ini` match your actual data file.
- For any other issues, check the console output for error messages which may provide more information about the problem.

## Contributing

Contributions to this project are welcome. Please ensure that your code adheres to the existing style and includes appropriate comments and documentation.

## License

This project is licensed under the Apache License, Version 2.0. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

## Contact

If you have any questions or feedback, please open an issue in the project repository.