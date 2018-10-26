from elasticsearch import Elasticsearch
import Exceptions
import StaticValues


class elasticRequest():

    def __init__(self, esServer):
        self.es = Elasticsearch([esServer])
        a = StaticValues.StaticValues()
        self.search_body = a.get_default_elastic()
        print("Request Handler Initialised")
        super().__init__()

    # Change max requests in search body to newNumber
    def change_max_results(self, newNumber):
        self.search_body["size"] = newNumber

    # Changes minimum required matches to specific number
    def set_minimum_matches(self, integer):
        self.search_body["query"]["bool"].update({"minimum_should_match": integer})

    # Appends a search term to the query
    def add_search_term(self, keyword):
        self.search_body["query"]["bool"]["should"].append({"match": {"_all": keyword}})

    # Appends a "must not match" logger_name term
    # def exclude_logger_name(self, logger_name):
    #     self.search_body["query"]["bool"]["must_not"].append({"match": {"logger_name": logger_name}})

    def add_logger_name(self, logger_name):
        self.search_body["query"]["bool"]["must"][1]["bool"]["should"].append({"match": {"logger_name": logger_name}})

    def set_from_date(self, date):
        self.search_body["query"]["bool"]["must"][0]["range"]["@timestamp"].update({"gte": date})
        self.search_body["query"]["bool"]["must"][0]["range"]["@timestamp"].update({"format": "dd/MM/yyyy"})

    def set_to_date(self, date):
        self.search_body["query"]["bool"]["must"][0]["range"]["@timestamp"].update({"lte": date})
        self.search_body["query"]["bool"]["must"][0]["range"]["@timestamp"].update({"format": "dd/MM/yyyy"})

    def send_request(self):
        res = self.es.search(index="_all", body=self.search_body)
        if res['hits']['total'] == 0:
            print("No Hits!")
            raise Exceptions.noDataFoundError
            return
        return res

