import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


class WaterForecastCalculator:
    def __init__(self, demand_data, availability_data, constants):
        self.aligned_data = None
        self.demand_data = demand_data
        self.availability_data = availability_data
        self.constants = constants
        self.forecast_df = pd.DataFrame()  # Empty DataFrame to store results

    def align_data(self):
        try:
            self.demand_data['Day'] = self.demand_data['Day'].astype(str)
            self.demand_data['Hour'] = self.demand_data['Hour'].astype(str)
            self.availability_data['Day'] = self.availability_data['Day'].astype(str)
            self.availability_data['Hour'] = self.availability_data['Hour'].astype(str)

            # Merge the data on 'Day' and 'Hour'
            self.aligned_data = pd.merge(self.demand_data, self.availability_data, on=['Day', 'Hour'], how='inner')
        except Exception as e:
            print(f"Error aligning data: {e}")
            self.aligned_data = pd.DataFrame()  # Assign empty DataFrame in case of error

    def _create_combo_chart(self, filename):
        try:
            if self.forecast_df.empty:
                print("No forecast data available for chart creation.")
                return

            ax = self.forecast_df.plot(kind='bar', x='Hour', y='Water Supplied to the Network', color='blue', label='Water Supplied')
            self.forecast_df.plot(kind='line', x='Hour', y='City Demand', color='red', label='City Demand', ax=ax)

            ax.set_xlabel('Hour')
            ax.set_ylabel('Volume')
            ax.set_title('Water Supply vs Demand Over Time')
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # to use only integer labels on x-axis

            plt.savefig(filename)
            plt.close()
        except Exception as e:
            print(f"Error creating combo chart: {e}")

    def save_forecast_to_excel(self, excel_filename='Water_Forecast.xlsx', chart_filename='Water_Forecast_Chart.png'):
        try:
            if self.forecast_df.empty:
                print("Forecast data is empty. Please calculate the forecast first.")
                return

            # Save the forecast DataFrame to an Excel file
            self.forecast_df.to_excel(excel_filename, index=False)
            print(f"Forecast data saved to '{excel_filename}'.")

            # Create and save the chart
            self._create_combo_chart(chart_filename)
            print(f"Chart saved to '{chart_filename}'.")
        except Exception as e:
            print(f"Error saving forecast data: {e}")

    def calculate_forecast(self):
        try:
            # Check if aligned data is available and not empty
            if self.aligned_data is None or self.aligned_data.empty:
                print("Aligned data is not available or is empty. Cannot calculate forecast.")
                return
            # Initialize an empty DataFrame for the forecast with the required columns
            columns = ['Day', 'Hour', 'Water Availability', 'City Demand', 'Water Supplied to the Network',
                       'Water Reservoir Level']
            forecast_df = pd.DataFrame(columns=columns)

            # Constants from the 'Constants' dictionary
            max_supply_rate = self.constants.get("MaxGenerationFacilityToNet [Liters]", 0)
            max_reservoir_capacity = self.constants.get("MaxReservoir  [Liters]", 0)
            reservoir_level = 0

            # Loop through each row in the aligned data
            for index, row in self.aligned_data.iterrows():
                water_availability = row['Available Supply']
                city_demand = row['Demand']

                # Calculate water supplied considering the max supply rate
                water_supplied = min(city_demand, water_availability + reservoir_level, max_supply_rate)

                # Update reservoir level considering the max reservoir capacity
                reservoir_level = min(max_reservoir_capacity, reservoir_level + water_availability - water_supplied)

                # Create a new row and add it to forecast_df using pd.concat
                new_row = pd.DataFrame([{
                    'Day': row['Day'],
                    'Hour': row['Hour'],
                    'Water Availability': water_availability,
                    'City Demand': city_demand,
                    'Water Supplied to the Network': water_supplied,
                    'Water Reservoir Level': reservoir_level
                }])
                forecast_df = pd.concat([forecast_df, new_row], ignore_index=True)

            # Store the forecast DataFrame in self.forecast_df for further use
            self.forecast_df = forecast_df
        except Exception as e:
            print(f"An unexpected error occurred during forecast calculation: {e}")
