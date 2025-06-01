import os
import faiss
import numpy as np
import json
from services.llm_service import call_llm, call_embedding


metadata_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "metadata/tables")
table_embeddings_path = os.path.join(metadata_dir, "table_embeddings.json")

index = None
table_names = []
summaries = []

def get_faiss_index(force_rebuild=False):
    global index, table_names, summaries
    if force_rebuild or index is None:
        index, table_names, summaries = build_faiss_index(table_embeddings_path)
    return index, table_names, summaries

def build_faiss_index(embedding_path):
    """Builds a FAISS index from table_embeddings.json and returns the index + metadata."""
    with open(embedding_path, "r") as file:
        data = json.load(file)

    # Extract embeddings
    embeddings = np.array([item["embedding"] for item in data], dtype="float32")
    faiss.normalize_L2(embeddings)  # 🔁 normalize for cosine similarity

    table_names = [item["table"] for item in data]
    summaries = [item["summary"] for item in data]

    # Build FAISS index (still uses IndexFlatL2, but now operates like cosine because of normalization)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print(f"✅ FAISS index built with {len(embeddings)} vectors of dimension {dim}")
    return index, table_names, summaries


# def search_similar_tables(query_embedding, index, table_names, summaries, top_k=5):
#     """Searches for top-k similar tables based on the query embedding."""
#     query_np = np.array([query_embedding], dtype="float32")  # shape (1, dim)
#     distances, indices = index.search(query_np, top_k)
#
#     results = []
#     for i in range(top_k):
#         idx = indices[0][i]
#         results.append({
#             "table": table_names[idx],
#             "summary": summaries[idx],
#             "distance": float(distances[0][i])
#         })
#
#     return results

def get_top_k_similar_tables(query, index, summaries, k=3):
    """Returns indices of top-k similar tables using semantic similarity."""
    query_embedding = call_embedding(query)  # returns list of floats
    query_vector = np.array([query_embedding], dtype="float32")
    distances, indices = index.search(query_vector, k)
    return indices[0]  # flat list of top-k indices
