import pandas as pd
import dateutil.parser
import datetime
import json
import StaticValues

class DataFormatter():

    def __init__(self, response):

        # Load adapter_dict
        a = StaticValues.StaticValues()
        self.adapter_dict = a.get_adapter_dict()

        # Generate dataframe based on contents of r
        data = pd.DataFrame(response)
        # pull out desired data ( search results from the json <cell 1,3>
        actualData = pd.DataFrame(data.iloc[1, 3])

        main = self.generate_subTable(actualData)

        # Join the subtable back with original dataFrame
        result = pd.concat([actualData, main], axis=1, join_axes=[actualData.index])
        result = result.sort_values(by=['timestamp'], ascending=False)
        result = result.reset_index(drop=True)

        # Remove '_source' column from original Dataframe
        result = result.drop('_source', 1)

        # Copy desired fields to separate new df
        self.to_display = self.form_displayTable(result)

        # Replace logger_name with values in adapter_dict
        self.to_display['logger_name'].replace(self.adapter_dict, inplace=True)

    def get_display(self):
        return self.to_display

    # Generate sub table from json in "_source" column
    def generate_subTable(self, actualData):
        for i in range(len(actualData.index)):
            try:
                temp = pd.DataFrame(actualData.iloc[i, 3])
            except ValueError:
                print("Invalid Log Entry: " + str(actualData.iloc[i, 3]))
                continue
            if i == 0:
                subtable = temp
                subtable.loc[i, "timestamp"] = dateutil.parser.parse(subtable["@timestamp"][i])
                subtable.loc[i, "date"] = (subtable["timestamp"][i] + datetime.timedelta(hours=8)).strftime(
                    "%H:%M:%S %d/%m/%Y")
                if isinstance(subtable.iloc[i]['response_body'], str):
                   subtable.loc[i, "response_message"] = json.loads(subtable.iloc[i]['response_body'])['message']
                # else:
                #     subtable.loc[i, "response_message"] = ""
            else:
                subtable = subtable.append(temp, ignore_index=True)
                subtable.loc[i, 'timestamp'] = dateutil.parser.parse(subtable["@timestamp"][i])
                subtable.loc[i, "date"] = (subtable["timestamp"][i] + datetime.timedelta(hours=8)).strftime(
                    "%H:%M:%S %d/%m/%Y")
                if isinstance(subtable.iloc[i]['response_body'], str):
                  subtable.loc[i, "response_message"] = json.loads(subtable.iloc[i]['response_body'])['message']
        return subtable

    # Copies values of desired columns to be displayed
    # Input: pd.Dataframe
    # Output: pd.Dataframe
    def form_displayTable(self, mainDataFrame):
        displayTable = pd.DataFrame()
        displayTable['timestamp'] = mainDataFrame['date']
        displayTable['logger_name'] = mainDataFrame['logger_name']
        displayTable['path'] = mainDataFrame['path']
        displayTable['response_status'] = mainDataFrame['response_status']
        displayTable['response_message'] = mainDataFrame['response_message']
        displayTable['request_body'] = mainDataFrame['request_body']
        displayTable['response_body'] = mainDataFrame['response_body']
        return displayTable