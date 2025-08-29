from pinecone import Pinecone, ServerlessSpec
import os

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])


def create_index():
    if "insurance-clauses" not in [i["name"] for i in pc.list_indexes()]:
        pc.create_index(
            name="insurance-clauses",
            dimension=int(os.environ.get("EMBED_DIM", "768")),
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws", region=os.environ.get("PINECONE_REGION", "us-east-1")
            ),
        )


def get_index():
    return pc.Index("insurance-clauses")
