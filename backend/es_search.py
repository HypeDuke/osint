from fastapi import APIRouter, Query
from elasticsearch import Elasticsearch
import os

es_router = APIRouter()
es = Elasticsearch([{"host": os.getenv("ES_HOST", "elasticsearch"), "port": 9200}])

@es_router.get("/")
def search(keyword: str = Query(..., min_length=1)):
    res = es.search(index="leaked_data", body={
        "query": {
            "match_phrase": {
                "content": keyword
            }
        }
    })
    return [hit["_source"] for hit in res["hits"]["hits"]]
