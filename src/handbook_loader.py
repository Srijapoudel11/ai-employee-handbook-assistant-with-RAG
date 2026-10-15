from docx import Document
from pathlib import Path


def load_handbook(file_path):
    """Read the employee handbook and return its sections."""

    document = Document(file_path)

    sections = []
    current_section = None
    current_text = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if not text:
            continue

        # Detect headings such as "2. Working Hours"
        if paragraph.style.name.startswith("Heading"):
            # Save the previous section
            if current_section is not None:
                sections.append({
                    "section": current_section,
                    "text": " ".join(current_text)
                })

            current_section = text
            current_text = []

        elif current_section is not None:
            current_text.append(text)

    # Save the final section
    if current_section is not None:
        sections.append({
            "section": current_section,
            "text": " ".join(current_text)
        })

    return sections


if __name__ == "__main__":
    handbook_path = Path("data") / "employee_handbook.docx"

    sections = load_handbook(handbook_path)

    print(f"Loaded {len(sections)} handbook sections.\n")

    for section in sections:
        print("SECTION:", section["section"])
        print("TEXT:", section["text"])
        print("-" * 50)
