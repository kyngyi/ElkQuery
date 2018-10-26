
class StaticValues():

    def __init__(self):

        # Default Request body for sending request
        # Size: 1000, DateRange: 10 Days before
        self.default_elastic = {"size": 100, "query": {
                    "bool": {
                        "must": [{
                            "range": {
                                "@timestamp": {
                                    "gte": "now-10d/d"
                                }
                            }
                        }, {"bool": {
                            "should": [
                            ]}
                            }
                        ],
                        "must_not": [
                        ],
                        "should": [
                        ],
                        "minimum_should_match": 1,
                        "boost": 1.0
                    }
                }}

        # Mapping of logger to programme names
        self.adapter_dict = {"ewalletproxy_server":"eWallet",
         "fevoadapter_server":"FEVO",
         "ltaewalletadapter":"LTA E Wallet",
         "ntaadapter_server":"NTA Adapter",
         "ntamanager_server":"NTA Manager",
         "trustadapter_server":"TRUST",
         "umaadapter_server":"UMA",
         "walletservice_server":"Wallet Service"
        }

        self.elasticsearch_server = 'http://10.2.5.21:9200'

    def get_adapter_dict(self):
        return self.adapter_dict

    def get_default_elastic(self):
        return self.default_elastic

    def get_elasticsearch_server(self):
        return self.elasticsearch_server


