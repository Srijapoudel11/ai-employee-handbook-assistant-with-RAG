from handbook_loader import load_handbook
from pathlib import Path
import re


STOP_WORDS = {
    "the", "a", "an", "is", "are", "am", "i", "me", "my",
    "do", "does", "did", "can", "could", "should", "would",
    "what", "how", "when", "where", "who", "why",
    "company", "employee", "employees", "provide", "get",
    "of", "to", "in", "on", "for", "from", "and", "or",
    "if", "it", "this", "that"
}


# Extra keywords for different handbook policies
POLICY_KEYWORDS = {
    "2. Working Hours": {
        "hours", "working", "work", "overtime", "schedule", "flexible"
    },

    "3. Annual Leave": {
        "annual", "leave", "holiday", "vacation"
    },

    "4. Sick Leave": {
        "sick", "ill", "illness", "medical", "certificate"
    },

    "5. Remote Work": {
        "remote", "home", "remotely"
    },

    "6. Workplace Conduct": {
        "harassment", "bullying", "discrimination",
        "conduct", "behaviour"
    },

    "7. Travel and Expenses": {
        "travel", "expense", "expenses", "receipt",
        "reimbursement", "reimbursed"
    },

    "8. Health and Safety": {
        "safety", "hazard", "accident", "emergency",
        "ergonomic"
    },

    "9. IT and Data Security": {
        "phishing", "password", "security", "malware",
        "device", "software", "data", "breach", "computer"
    },

    "10. Contact and Support": {
        "contact", "support", "hr", "manager"
    }
}


def tokenize(text):
    """Convert text into useful searchable words."""

    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    return {
        word for word in words
        if word not in STOP_WORDS
    }


def retrieve_context(question):
    """Find the most relevant handbook section."""

    handbook_path = Path("data") / "employee_handbook.docx"
    sections = load_handbook(handbook_path)

    question_words = tokenize(question)

    best_section = None
    best_score = 0

    for section in sections:

        section_words = tokenize(
            section["section"] + " " + section["text"]
        )

        # Normal text matches
        normal_matches = question_words.intersection(section_words)
        score = len(normal_matches)

        # Give policy keywords extra importance
        keywords = POLICY_KEYWORDS.get(section["section"], set())
        keyword_matches = question_words.intersection(keywords)

        score += len(keyword_matches) * 3

        if score > best_score:
            best_score = score
            best_section = section

    if best_section is None or best_score == 0:
        return {
            "found": False,
            "section": None,
            "text": "",
            "score": 0
        }

    return {
        "found": True,
        "section": best_section["section"],
        "text": best_section["text"],
        "score": best_score
    }


if __name__ == "__main__":

    question = input("Ask an employee handbook question: ")

    result = retrieve_context(question)

    if result["found"]:
        print("\nRelevant information found!")
        print("Source:", result["section"])
        print("Information:", result["text"])
        print("Match score:", result["score"])

    else:
        print(
            "\nNo relevant information was found "
            "in the employee handbook."
        )
