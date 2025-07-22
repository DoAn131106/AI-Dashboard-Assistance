import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Predefined metric and dimension keywords to match (expand later)
KNOWN_METRICS = {"sales", "revenue", "profit", "expenses", "cost"}
KNOWN_DIMENSIONS = {"region", "date", "month", "quarter", "year", "category"}

def parse_query(query):
    doc = nlp(query.lower())

    intent = None
    metrics = set()
    dimensions = set()
    filters = []

    for token in doc:
        # Extract intent (look for verbs like 'show', 'compare', etc.)
        if token.pos_ == "VERB" and intent is None:
            intent = token.lemma_

        # Match metric keywords
        if token.text in KNOWN_METRICS:
            metrics.add(token.text)

        # Match dimension keywords
        if token.text in KNOWN_DIMENSIONS:
            dimensions.add(token.text)

        # Handle filters like "in Q2 2024"
        if token.ent_type_ in ("DATE", "TIME"):
            filters.append(token.text)

    return {
        "intent": intent,
        "metrics": list(metrics),
        "dimensions": list(dimensions),
        "filters": filters
    }

if __name__ == "__main__":
    test_query = "Show me the sales and profit by region in Q2 2024"
    result = parse_query(test_query)
    print(result)

