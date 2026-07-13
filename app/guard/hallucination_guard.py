

def apply_hallucination_guard(answer, evaluation):
    """
    evaluation: string output from evaluator
    """

    # Normalize text
    eval_text = evaluation.lower()

    hallucination = "hallucination: yes" in eval_text

    # Extract groundedness (optional)
    groundedness_score = None
    for line in eval_text.split("\n"):
        if "groundedness" in line:
            try:
                groundedness_score = float(line.split(":")[1].strip())
            except:
                pass

    # 🚨 Rule 1: Hallucination detected
    if hallucination:
        return {
        "status": "warning",
        "answer": answer + "\n\n⚠️ This answer may not be fully supported by the document.",
        "reason": "Hallucination detected"
    }
    

    # ⚠️ Rule 2: Low groundedness
    if groundedness_score is not None and groundedness_score < 6:
        return {
            "status": "warning",
            "answer": answer,
            "reason": "Low groundedness"
        }

    # ✅ Safe
    return {
        "status": "safe",
        "answer": answer,
        "reason": "Answer is grounded"
    }