import pandas as pd
import ElasticRequest
import elasticsearch
import json
import Exceptions
import dateutil.parser
import datetime
import DataFormatter


def get_data(keyword, keyword2):

    # # Generate sub table from json in "_source" column
    # def generate_subTable(data):
    #     for i in range(len(data.index)):
    #         if i == 0:
    #             subtable = pd.DataFrame(actualData.iloc[i, 3])
    #             subtable.loc[i, "timestamp"] = dateutil.parser.parse(subtable["@timestamp"][i])
    #             subtable.loc[i, "date"] = (subtable["timestamp"][i] + datetime.timedelta(hours=8)).strftime("%H:%M:%S %d/%m/%Y")
    #             if isinstance(subtable.iloc[i]['response_body'], str):
    #                 subtable.loc[i, "response_message"] = json.loads(subtable.iloc[i]['response_body'])['message']
    #         else:
    #             subtable = subtable.append(pd.DataFrame(actualData.iloc[i, 3]), ignore_index=True)
    #             subtable.loc[i, 'timestamp'] = dateutil.parser.parse(subtable["@timestamp"][i])
    #             subtable.loc[i, "date"] = (subtable["timestamp"][i] + datetime.timedelta(hours=8)).strftime("%H:%M:%S %d/%m/%Y")
    #             if isinstance(subtable.iloc[i]['response_body'], str):
    #                 subtable.loc[i, "response_message"] = json.loads(subtable.iloc[i]['response_body'])['message']
    #     return subtable
    #
    # # Copies values of desired columns to be displayed
    # def form_displayTable(mainDataFrame):
    #     displayTable = pd.DataFrame()
    #     displayTable['timestamp'] = mainDataFrame['date']
    #     displayTable['logger_name'] = mainDataFrame['logger_name']
    #     displayTable['path'] = mainDataFrame['path']
    #     displayTable['response_status'] = mainDataFrame['response_status']
    #     displayTable['response_message'] = mainDataFrame['response_message']
    #     displayTable['request_body'] = mainDataFrame['request_body']
    #     displayTable['response_body'] = mainDataFrame['response_body']
    #     return displayTable

    print("Sendrequest Module Initiated")
    requestHandler = ElasticRequest.elasticRequest('http://10.2.5.21:9200')
    r = 0
    try:
        requestHandler.add_search_term(keyword)
        requestHandler.add_search_term(keyword2)
        r = requestHandler.send_request()
    except elasticsearch.exceptions.ConnectionError as e:
        print("Except block entered")
        raise elasticsearch.exceptions.ConnectionError
    # Checking for any search results
    if (r['hits']['total'] == 0):
        print("No Hits!")
        raise Exceptions.noDataFoundError
        return
    print("Finished log extraction from ELK")
    # Generate dataframe based on contents of r
    # data = pd.DataFrame(r)
    # # pull out desired data ( search results from the json <cell 1,3>
    # actualData = pd.DataFrame(data.iloc[1,3])
    #
    # main = generate_subTable(actualData)
    #
    # # Join the subtable back with original dataFrame
    # result = pd.concat([actualData, main], axis=1, join_axes=[actualData.index])
    # result = result.sort_values(by=['timestamp'], ascending=False)
    # result = result.reset_index(drop=True)
    #
    # # Remove '_source' column from original Dataframe
    # result = result.drop('_source', 1)
    #
    # # Copy desired fields to separate new df
    # to_display = form_displayTable(result)

    data_formatter = DataFormatter.DataFormatter(r)
    to_display = data_formatter.get_display()

    return to_display
