import pandas as pd
from enums import FileType


class DataReader:
    def __init__(self, filepath, data_type):
        self.filepath = filepath
        self.data_type = data_type

    def read_and_process(self):
        try:
            if self.data_type == FileType.DEMAND:
                return self._process_demand_data()
            elif self.data_type == FileType.WATER_AVAILABILITY:
                return self._process_availability_data()
            elif self.data_type == FileType.CONSTANTS:
                return self._read_constants()
            else:
                raise ValueError("Invalid data type")
        except FileNotFoundError:
            print(f"File not found: {self.filepath}. Please check the file path.")
        except pd.errors.EmptyDataError:
            print(f"No data: The file {self.filepath} is empty.")
        except Exception as e:
            print(f"An error occurred while processing {self.filepath}: {e}")

    def _process_demand_data(self):
        try:
            data = pd.read_excel(self.filepath, header=None, skiprows=[0], names=['Day', 'Hour', 'GenGrid [Liters]'])
            data.rename(columns={'GenGrid [Liters]': 'Demand'}, inplace=True)
            return data
        except Exception as e:
            print(f"Error processing demand data: {e}")

    def _process_availability_data(self):
        try:
            data = pd.read_excel(self.filepath, header=None, skiprows=[0],
                                 names=['Timestamp', 'Expected Rainfall [Liters]'])
            data['Timestamp'] = pd.to_datetime(data['Timestamp'])
            data['Day'] = data['Timestamp'].dt.strftime('%#d/%#m/%Y')
            data['Hour'] = data['Timestamp'].dt.time
            data.rename(columns={'Expected Rainfall [Liters]': 'Available Supply'}, inplace=True)
            return data[['Day', 'Hour', 'Available Supply']]
        except Exception as e:
            print(f"Error processing availability data: {e}")

    def _read_constants(self):
        try:
            data = pd.read_excel(self.filepath, header=0, names=['key', 'val'])
            return data.set_index('key')['val'].to_dict()
        except Exception as e:
            print(f"Error reading constants: {e}")