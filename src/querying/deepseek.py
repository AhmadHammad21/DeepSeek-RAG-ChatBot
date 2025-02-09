import ollama

class DeepSeekQuery:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = ollama.Client()

    def query(self, question, context):
        response = self.client.generate(
            model=self.model_name,
            system="You are a helpful assistant answering questions using retrieved context.",
            prompt=f"Context: {context}\n\nQuestion: {question}\nAnswer:"
        )
        return response.get("response", "")
