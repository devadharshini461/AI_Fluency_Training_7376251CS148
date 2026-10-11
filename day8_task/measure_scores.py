"""Part C helper: print cosine-distance scores for a good and a bad question, then pick MAX_DISTANCE between them."""
from lc_config import get_vectorstore

store = get_vectorstore()
for label, q in [("GOOD (placements)", "What CGPA do I need to be eligible for placements?"),
                 ("BAD  (France)    ", "What is the capital of France?")]:
    scores = [round(s, 3) for _, s in store.similarity_search_with_score(q, k=3)]
    print(f"{label}: {scores}   best = {min(scores)}")
print("\nPick MAX_DISTANCE between the GOOD best score and the BAD best score.")
