# Neural Data Visualization Tool

This tool provides a graphical user interface for visualizing neural data recorded from Neuropixel probes. It allows users to load specific channels of data, navigate through the recording in time, and visualize voltage traces for selected channels.

## Features

- Load and visualize data from Neuropixel recordings
- Select specific channels for visualization
- Adjust the time window and duration of the displayed data
- Real-time updates of the visualization as parameters are changed
- Display voltage traces in millivolts (mV)

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

## Data Preparation

1. Ensure you have a Neuropixel recording file (.bin) available.
2. Note the path to this file, as you'll need to update it in the script.

## Configuration

1. Open the `Neural_Data_Visualization.py` file in a text editor.
2. Locate the following line in the `App` class initialization:

   ```python
   Path("C:/Datasets/CRCNS/spe-1/data/c45/c45_npx_raw-001.bin")
   ```

3. Replace this path with the path to your Neuropixel recording file.

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

## Troubleshooting

- If you encounter any errors related to missing packages, ensure you've installed all required dependencies using the `requirements.txt` file.
- If the data doesn't load, double-check that the file path in the script matches the location of your .bin file.
- For any other issues, check the console output for error messages which may provide more information about the problem.

## Contributing

Contributions to this project are welcome. Please ensure that your code adheres to the existing style and includes appropriate comments and documentation.

## License

This project is licensed under the Apache License, Version 2.0. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

## Contact

If you have any questions or feedback, please open an issue in the project repository.s