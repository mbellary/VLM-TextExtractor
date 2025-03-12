from pdf.src.Interfaces import Processor
from pdf.src.util import get_query, get_keys


class QueryProcessor(Processor):
    def __init__(self, query_path):
        super().__init__()
        self.query_path = query_path

    def process(self):
        try :
            query = get_query(self.query_path)
            query_keys = get_keys(self.query_path)
            query_schema = str(query)
            query = "retrieve " + query_keys
            query = (query + ". return response in JSON format, by strictly following this JSON schema: " + query_schema +
                     ". If a field is not visible or cannot be found in the document, return null. Do not guess, infer, or generate values for missing fields.")
            return query, query_schema
        except ValueError as e:
            raise ValueError(f'Error preparing query: {e}')
