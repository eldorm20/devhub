import meilisearch
from .database import MEILISEARCH_URL, MEILISEARCH_MASTER_KEY

client = meilisearch.Client(MEILISEARCH_URL, MEILISEARCH_MASTER_KEY)

def create_indexes():
    client.create_index("questions", {"primaryKey": "id"})
    client.create_index("discussions", {"primaryKey": "id"})

def index_question(question):
    client.index("questions").add_documents([question])

def index_discussion(discussion):
    client.index("discussions").add_documents([discussion])

def search_questions(query):
    return client.index("questions").search(query)

def search_discussions(query):
    return client.index("discussions").search(query)