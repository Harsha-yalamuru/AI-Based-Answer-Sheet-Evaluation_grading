import os

def load_full_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_keywords(schema_text):
    # Flatten all lines and keywords into a single list
    lines = [line.strip() for line in schema_text.splitlines() if line.strip() and not line.startswith("=")]
    keywords = []
    for line in lines:
        keywords.extend([k.strip() for k in line.split(",") if k.strip()])
    return keywords

def score_full_text(extracted_text, keywords):
    extracted_lower = extracted_text.lower()
    matched_keywords = [kw for kw in keywords if kw.lower() in extracted_lower]
    score = len(matched_keywords)
    return score, len(keywords), matched_keywords

def grade_extracted_text_whole(extracted_file, schema_file, max_marks, output_file="graded_results.txt"):
    extracted_text = load_full_text(extracted_file)
    schema_text = load_full_text(schema_file)

    keywords = extract_keywords(schema_text)
    matched, total, matched_keywords = score_full_text(extracted_text, keywords)

    # Calculate final grade
    final_score = round((matched / total) * max_marks, 0)

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("Grading Summary (Whole Document)\n")
        out.write("-" * 40 + "\n")
        out.write(f"Total Keywords: {total}\n")
        out.write(f"Matched Keywords: {matched}\n")
        out.write(f"Score: {matched} / {total}\n")
        out.write(f"Final Grade: {final_score} / {max_marks}\n\n")
        out.write("Matched Keywords:\n")
        out.write(", ".join(matched_keywords) + "\n")

    print(f"Grading complete. Results saved to: {output_file}")

    # Also return result dictionary for UI use
    return {
        "matched": matched,
        "total": total,
        "score": final_score,
        "max_marks": max_marks,
        "matched_keywords": matched_keywords
    }

def run_grading():
    # Original usage retained for CLI
    while True:
        try:
            max_marks = float(input("Enter maximum marks for this question: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    grade_extracted_text_whole("extracted_texts.txt", "answer_schema.txt", max_marks)

# Example usage
if __name__ == "__main__":
    run_grading()
