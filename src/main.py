from data_reader import DataReader
from water_forecast_calculator import WaterForecastCalculator
from config import *
from enums import FileType


def main():
    demand_data = DataReader(DEMAND_FILE_PATH, FileType.DEMAND).read_and_process()
    availability_data = DataReader(WATER_AVAILABILITY_FILE_PATH, FileType.WATER_AVAILABILITY).read_and_process()
    constants_data = DataReader(CONSTANTS_FILE_PATH, FileType.CONSTANTS).read_and_process()

    # Initialize the WaterForecastCalculator with the processed data
    forecast_calculator = WaterForecastCalculator(demand_data, availability_data, constants_data)

    # Align, calculate and save the forecast
    forecast_calculator.align_data()
    forecast_calculator.calculate_forecast()
    forecast_calculator.save_forecast_to_excel()


if __name__ == "__main__":
    main()
