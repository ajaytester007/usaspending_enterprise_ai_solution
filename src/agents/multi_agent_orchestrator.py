from src.rag.local_rag import simple_retrieve

class DataQualityAgent:
    def assess(self):
        return {'status': 'stub', 'message': 'Add Great Expectations or custom PySpark rules here.'}

class AnalyticsAgent:
    def answer(self, question: str):
        docs = simple_retrieve(question)
        return {'answer': 'RAG scaffold response. Connect an approved LLM provider to synthesize over retrieved context.', 'sources': [d['path'] for d in docs]}

class GovernanceAgent:
    def verify(self):
        return {'status': 'stub', 'checks': ['connector allowlist', 'lineage traceability', 'read-only SQL policy']}
