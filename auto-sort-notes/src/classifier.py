# Classify files by subject/module/textbook

import re
from collections import Counter
from .preprocess import extract_pdf_text
from .utils import normalize_text


# src/classifier.py

SUBJECT_KEYWORDS = {
    "Software Engineering and Project Management": [
        "SDLC", "agile", "waterfall", "project plan", "requirement analysis", "testing", "design pattern"
    ],
    "Computer Network": [
        "TCP", "UDP", "routing", "IP", "protocol", "OSI", "switch", "bandwidth", "latency"
    ],
    "Theory of Computation": [
        "automata", "regular expression", "context free", "pushdown automaton",
        "Turing machine", "decidability", "NP-complete"
    ],
    "Web Technology Lab": [
        "HTML", "CSS", "JavaScript", "React", "Node.js", "Flask", "Django"
    ],
    "Artificial Intelligence": [
        "search algorithm", "heuristic", "minimax", "neural network", "machine learning",
        "Bayesian", "inference", "knowledge representation"
    ],
    "Research Methodology and IPR": [
        "hypothesis", "methodology", "plagiarism", "patent", "copyright", "research design"
    ],
    "Environmental Studies": [
        "ecosystem", "biodiversity", "climate change", "pollution", "sustainability",
        "renewable energy"
    ]
}


def detect_subject(path, filename_only=False):
    text = ""
    if not filename_only:
        if path.suffix.lower() == ".pdf":
            text = extract_pdf_text(path)
        # you can add docx, pptx extraction later
    
    # combine filename + text
    haystack = (path.name + " " + text).lower()

    scores = {}
    for subject, keywords in SUBJECT_KEYWORDS.items():
        count = 0
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw.lower()) + r"\b", haystack):
                count += 1
        scores[subject] = count

    # pick best subject
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Unclassified"
