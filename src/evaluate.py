from .retrieval import retrieve
from .chat import query_portfolio

# Define your test queries and expected results
TEST_QUERIES = [
    {
        "query": "Which projects are healthcare-related?",
        "expected_projects": [
            "Parkinson Disease Detection from Speech Features",
            "Heart Disease Dashboard — Power BI Project",
            "Hypertension Prediction — Machine Learning Project"
        ]
    },
    {
        "query": "Which projects applied machine learning?",
        "expected_projects": [
            "Parkinson Disease Detection from Speech Features",
            "Fine-Tuned BART for Abstractive Text Summarization",
            "Hypertension Prediction — Machine Learning Project",
            "Text Coherence Evaluation Project"
        ]
    },
    {
        "query": "Which projects involved dashboards or data visualization?",
        "expected_projects": [
            "Heart Disease Dashboard — Power BI Project",
            "Hypertension Prediction — Machine Learning Project"
        ]
    }
]
TOP_K=10
def evaluate_queries(queries):
    results = []

    for test in queries:
        query = test["query"]
        print(f"\n=== Evaluating Query: {query} ===\n")
        
        # Retrieval
        retrieved_chunks = retrieve(query, k=TOP_K)
        print(f"Retrieved {len(retrieved_chunks)} chunks.\n")
        
        # Generation
        generated_answer = query_portfolio(query)
        print("Generated Answer Preview:\n", generated_answer[:400], "...\n")
        
        # Base eval result
        eval_result = {"query": query, "retrieved_chunks_count": len(retrieved_chunks), "generated_answer": generated_answer}

        # --- ML / healthcare project detection ---
        if "expected_projects" in test:
            if isinstance(test["expected_projects"], dict):
                for category, projects in test["expected_projects"].items():
                    detected_projects = [proj for proj in projects if any(proj.lower() in chunk.lower() for chunk in retrieved_chunks)]
                    eval_result[f"{category}_recall"] = len(detected_projects) / max(len(projects), 1)
                    eval_result[f"{category}_detected"] = detected_projects

                    # Faithfulness: are generated projects present in retrieved chunks?
                    faithful_projects = [proj for proj in detected_projects if proj.lower() in generated_answer.lower()]
                    eval_result[f"{category}_faithfulness"] = len(faithful_projects) / max(len(detected_projects), 1)
            elif isinstance(test["expected_projects"], list):
                detected_projects = [proj for proj in test["expected_projects"] if any(proj.lower() in chunk.lower() for chunk in retrieved_chunks)]
                eval_result["projects_recall"] = len(detected_projects) / max(len(test["expected_projects"]), 1)
                eval_result["projects_detected"] = detected_projects
                # Faithfulness
                faithful_projects = [proj for proj in detected_projects if proj.lower() in generated_answer.lower()]
                eval_result["projects_faithfulness"] = len(faithful_projects) / max(len(detected_projects), 1)

        # Keyword detection
        if "expected_keywords" in test:
            keywords_detected = [kw for kw in test["expected_keywords"] if kw.lower() in generated_answer.lower()]
            eval_result["keyword_match_score"] = len(keywords_detected) / max(len(test["expected_keywords"]), 1)
            eval_result["keywords_detected"] = keywords_detected
            # Faithfulness can be same as keyword match for this case
            eval_result["keyword_faithfulness"] = eval_result["keyword_match_score"]

        # Context precision: how many retrieved chunks are actually referenced in the answer
        used_chunks = [chunk for chunk in retrieved_chunks if any(word.lower() in chunk.lower() for word in generated_answer.lower())]
        eval_result["context_precision"] = len(used_chunks) / max(len(retrieved_chunks), 1)

        results.append(eval_result)

    return results

if __name__ == "__main__":
    evaluation_results = evaluate_queries(TEST_QUERIES)
    
    # Print summary
    for res in evaluation_results:
        print("\nQuery:", res["query"])
        print("Retrieved Chunks:", res["retrieved_chunks_count"])
        print("Generated Answer Preview:", res["generated_answer"][:300], "...")
        if any(k.endswith("_recall") for k in res):
            for k, v in res.items():
                if "_recall" in k or "_detected" in k or "_faithfulness" in k:
                    print(f"{k}: {v}")
        if "keyword_match_score" in res:
            print(f"Keyword Match Score: {res['keyword_match_score']:.2f}, Detected: {res['keywords_detected']}")
            print(f"Keyword Faithfulness: {res['keyword_faithfulness']:.2f}")
        print(f"Context Precision: {res['context_precision']:.2f}")