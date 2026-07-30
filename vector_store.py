
import faiss
import numpy as np

class SimpleVectorStore:

    def __init__(self, dimension=768):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)

        self.chunks = []   
        self.sources = []  

    def add_chunks(self, chunk_list, embedding_list, source_name):
        vectors = np.array(embedding_list).astype("float32")
        self.index.add(vectors)

        self.chunks.extend(chunk_list)

        for i in range(len(chunk_list)):
            self.sources.append(source_name)

    def search(self, query_embedding, top_k=3):
        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunks):
                results.append({
                    "text": self.chunks[idx],
                    "source": self.sources[idx]
                })

        return results

    def is_empty(self):
        if len(self.chunks) == 0:
            return True
        else:
            return False