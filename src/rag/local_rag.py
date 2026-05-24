from pathlib import Path

CORPUS_PATHS = [Path('docs'), Path('config')]

def load_corpus():
    docs = []
    for path in CORPUS_PATHS:
        if path.exists():
            for file in path.rglob('*'):
                if file.suffix.lower() in ['.md', '.json', '.yml', '.yaml']:
                    docs.append({'path': str(file), 'text': file.read_text(encoding='utf-8', errors='ignore')})
    return docs

def simple_retrieve(question: str, top_k: int = 5):
    terms = set(question.lower().split())
    scored = []
    for doc in load_corpus():
        score = sum(1 for t in terms if t in doc['text'].lower())
        if score:
            scored.append((score, doc))
    return [d for _, d in sorted(scored, key=lambda x: x[0], reverse=True)[:top_k]]
