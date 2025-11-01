import re
import fitz  # PyMuPDF
from google import genai
from .config import GEMINI_API_KEY, MODEL

# Initialize Gemini LLM client
client = genai.Client(api_key=GEMINI_API_KEY)


def pdf_to_txt(pdf_path: str, txt_path: str):
    raw_text = pdf_to_text(pdf_path)
    cleaned_text = clean_text(raw_text)
    person_name = extract_name(cleaned_text)
    if person_name == "Unknown Candidate":
        person_name = extract_name_llm(cleaned_text)
        
    structured_cv = generate_structured_cv(cleaned_text, person_name)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(structured_cv)
    print(f"✅ Structured CV saved to: {txt_path}")

def extract_name_llm(text: str) -> str:
    prompt = """
    Extract ONLY the full name of the person from the CV text below.
    If multiple names appear, choose the one clearly belonging to the candidate.
    Do not add extra text.
    """
    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt, text[:1200]]  # first part of CV contains the name
    )
    return response.text.strip()

def pdf_to_text(pdf_path: str) -> str:
    """Extract raw text from PDF."""
    doc = fitz.open(pdf_path)
    raw_text = "\n".join(page.get_text("text") for page in doc)
    doc.close()
    return raw_text


def clean_text(text: str) -> str:
    """Basic cleaning and normalization of extracted PDF text."""
    text = re.sub(r'\s+', ' ', text)                          # collapse whitespace
    text = re.sub(r'[\u200b\u200e\u202a-\u202e]', '', text)  # remove invisible chars
    text = re.sub(r'(\/gtb|\/♀nedn)', '', text)              # remove weird markers
    text = re.sub(r'\s([.,])', r'\1', text)                  # fix spacing before punctuation
    return text.strip()


# def extract_name(text: str) -> str:
#     """
#     Try to detect the candidate's name.
#     Simple heuristic: assume the name is in the first line(s) with capitalized words.
#     """
#     lines = text.splitlines()
#     for line in lines[:5]:  # check only first 5 lines
#         # Match sequences of 2-3 capitalized words (e.g., "John Doe", "Mohammed Dechraoui")
#         match = re.search(r'\b([A-Z][a-z]+(?: [A-Z][a-z]+){1,2})\b', line)
#         if match:
#             return match.group(1)
#     return "Unknown Candidate"


def extract_name(text: str) -> str:
    """
    Attempts to detect the full name of the candidate using multiple strategies:
    1. Look for lines with 2–4 consecutive capitalized words.
    2. Look for ALL-CAPS names (e.g., DECHRAOUI MOHAMMED).
    3. Infer from email username if necessary.
    """

    # Normalize spacing
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # --- 1) Look for Title Case Names ---
    pattern_title_case = re.compile(r"\b([A-Z][a-z]+(?: [A-Z][a-z]+){1,3})\b")
    for line in lines[:8]:  # check first 8 lines
        match = pattern_title_case.search(line)
        if match:
            return match.group(1)

    # --- 2) Look for ALL CAPS Names (common in CV headers) ---
    pattern_all_caps = re.compile(r"\b([A-Z]{2,}(?: [A-Z]{2,}){1,3})\b")
    for line in lines[:8]:
        match = pattern_all_caps.search(line)
        if match:
            # Convert: "DECHRAOUI MOHAMMED" → "Dechraoui Mohammed"
            name = " ".join(w.capitalize() for w in match.group(1).split())
            return name

    # --- 3) Infer from Email (fallback) ---
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    if email_match:
        username = email_match.group().split("@")[0]
        # Convert variations like mohammed.dechraoui → Mohammed Dechraoui
        name_guess = " ".join([part.capitalize() for part in re.split(r"[._\-]", username) if len(part) > 1])
        if len(name_guess.split()) >= 2:
            return name_guess

    return "Unknown Candidate"



def generate_structured_cv(raw_text: str, person_name: str) -> str:
    """
    Sends raw CV text to the LLM and asks it to output a fully structured CV,
    even if original titles are missing or inconsistent.
    """
    system_prompt = f"""
You are a professional CV parser and formatter assistant.
Your task is to take the raw CV content of {person_name} and generate a structured, human-readable CV in the following format:

# Summary
<one paragraph summary of the candidate>

# Professional Experiences
## [Job Title] — [Company] (Start – End)
* Objective: ...
* Responsibilities & Achievements:
- ...
* Technologies / Skills: ...

# Projects
## [Project Name] (Start – End)
* Objective: ...
* Key Features:
- ...
* Responsibilities / Role:
- ...
* Results / Achievements:
- ...
* Technologies / Skills Used:
- ...
* Current Status: ...

# Education
# Certifications
# Skills
# Languages
# Strengths & Interests

Rules:
- Detect missing section titles and infer them from context.
- Use clear bullets for achievements.
- Highlight skills, technologies, and project names in bold.
- Preserve all dates and durations.
- Output in markdown format as shown above.
"""

    user_prompt = f"""
Raw CV Text:
{raw_text}

Please return a fully structured CV in markdown, following the system instructions.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=[system_prompt, user_prompt]
    )

    return response.text.strip() if response.text else "No structured CV generated."


# === Example Usage ===
if __name__ == "__main__":
    pdf_path = "data/finale_cv.pdf"
    txt_output = "data/structured_cv.txt"

    pdf_to_txt(pdf_path, txt_output)
