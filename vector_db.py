import numpy as np
from sklearn.preprocessing import normalize
from sentence_transformers import SentenceTransformer
from sample_data import get_assessments

class VectorDB:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.assessments = get_assessments()  # Ensure the assessments are available
        self.embeddings = self._create_embeddings()

    def _create_embeddings(self):
        descriptions = [a['description'] for a in self.assessments]
        embeddings = self.model.encode(descriptions)
        return normalize(embeddings)  # Normalize embeddings to unit length
        
    def search(self, query, top_k=10):
        query_embedding = self.model.encode(query)
        query_embedding = normalize([query_embedding])  # Normalize query embedding
        scores = np.dot(self.embeddings, query_embedding.T)  # Dot product between normalized embeddings
        top_indices = np.argsort(scores.flatten())[-top_k:][::-1]  # Get top-k indices
        
        # Dynamically extract keywords from the query to filter relevant assessments
        query_keywords = query.lower().split()  # Split the query into lowercase words for matching
        
        filtered_results = []
        for i in top_indices:
            assessment = self.assessments[i]
            # Check if any query keyword is in the name or description of the assessment
            if any(keyword in assessment['name'].lower() or keyword in assessment['description'].lower() for keyword in query_keywords):
                filtered_results.append(assessment)
        
        # If no matching results, return the top-k results without filtering
        if not filtered_results:
            filtered_results = [self.assessments[i] for i in top_indices]
        
        return filtered_results

# Singleton instance
vector_db = VectorDB()

# Example query to search for "sales" or "java developers"
query = "I want to hire new graduates for a Java developer role in my company"
results = vector_db.search(query, top_k=5)

# Display results (Example)
for i, result in enumerate(results):
    print(f"Rank {i+1}: {result['name']} | URL: {result['url']}")
