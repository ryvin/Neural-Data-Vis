# Neural Data Visualization Tool
![Neural Data Visualization Tool](/images/Neural%20Data%20Visualization3.png)

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

## Data Files

This project uses data from the CRCNS.org spe-1 dataset, which contains simultaneous patch-clamp and dense CMOS probe extracellular recordings from the same cortical neuron in anesthetized rats. The following files are crucial for understanding and using the data:

1. `c45_expt_meta.csv`: This file contains metadata about the experiment, specifically the dimensions and data types of the Neuropixel and patch-clamp recordings. The content is:

   ```
   npx,patch
   "[(384L, 24301033L), 'int16']","[40521060, 'float64']"
   ```

   This indicates that:
   - The Neuropixel (npx) data has 384 channels and 24,301,033 samples, stored as 16-bit integers.
   - The patch-clamp data has 40,521,060 samples, stored as 64-bit floats.

2. `crcns_spe-1_data_description.pdf`: This document provides a comprehensive description of the dataset, including:
   - Summary of the experiment
   - Data organization
   - File formats
   - How to cite the dataset
   - Methods used
   - Detailed explanation of each file in the dataset

### Key Points from the Data Description:

- The dataset includes recordings from 43 neurons in the primary motor and somatosensory cortex of anesthetized rats.
- Data is organized by cell, with each cell having its own directory (cxx, where xx is the cell number).
- The Neuropixel data (`cxx_npx_raw.bin`) is stored as a 1D binary file that needs to be reshaped into a 2D array (384 channels x samples).
- The conversion factor for Neuropixel data to microvolts is 2.34 μV per bit.
- Patch-clamp data (`cxx_patch_ch1.bin`) is already in pA or mV, depending on the recording mode.
- Additional files include synchronization channels, spike sample information, and summary data.

## Data Preparation

Before running the visualization tool, ensure you have:

1. Downloaded the necessary data files from CRCNS.org (you may need to request access).
2. Placed the `cxx_npx_raw.bin` file (where xx is the cell number you're interested in) in the directory specified in your `config.ini` file.
3. Updated the `shape` parameter in `config.ini` to match the dimensions in `c45_expt_meta.csv` for the Neuropixel data.

## Installation

1. Clone this repository or download the script to your local machine.

2. Navigate to the directory containing the script in your terminal or command prompt.

3. Set up a virtual environment (recommended):
   
   On Windows:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   
   On macOS and Linux:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required Python packages by running:

   ```
   pip install -r requirements.txt
   ```

5. When you're done working on the project, you can deactivate the virtual environment by running:
   
   ```
   deactivate
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
3. Activate the virtual environment if you haven't already:
   
   On Windows:
   ```
   venv\Scripts\activate
   ```
   
   On macOS and Linux:
   ```
   source venv/bin/activate
   ```

4. Run the script using Python:

   ```
   python Neural_Data_Visualization.py
   ```

5. The application window should appear.

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

- If you encounter any errors related to missing packages, ensure you've activated the virtual environment and installed all required dependencies using the `requirements.txt` file.
- If the data doesn't load, double-check that the file path and shape in `config.ini` match your actual data file.
- For any other issues, check the console output for error messages which may provide more information about the problem.

## Additional Resources

For more detailed information about the dataset and example code for data analysis, visit the companion repository:
https://github.com/kampff-lab/sc.io/tree/master/Paired%20Recordings

## Contributing

Contributions to this project are welcome. Please ensure that your code adheres to the existing style and includes appropriate comments and documentation.

## License

This project is licensed under the Apache License, Version 2.0. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

## Contact

If you have any questions or feedback, please open an issue in the project repository.