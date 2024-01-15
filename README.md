
# Water Supply Forecasting System

## Description
This Python project forecasts water supply needs by processing and analyzing water demand, availability, and various constants. It includes data processing from Excel files and calculating water supply forecasts.

## Installation
To set up this project:

1. Clone or download the repository to your local machine.
2. Install Python 3.x, if not already installed.
3. Install required dependencies by running `pip install -r requirements.txt` (if a `requirements.txt` file is present with all necessary packages).

## Usage
Run the main script to execute the program:
```bash
python main.py
```
This script reads data from specified Excel files, performs necessary calculations, and saves the forecast results.

## Modules
- `DataReader`: Handles reading and processing data from Excel files. Supports various data types: demand, water availability, and constants.
- `WaterForecastCalculator`: Aligns data and calculates the water supply forecast based on the processed data.
- `config.py`: Contains configuration details such as file paths, default values, and output file names.
- `enums.py`: Defines the `FileType` enum for different data categories.

## Configuration
Configure the file paths and other constants in `config.py`and  `enums.py` . Ensure that the Excel files are placed in the correct directory as specified in the configuration.
