import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer
from transformers import pipeline


class LLMTaggerStage:
    # Load the model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained("hatmimoha/arabic-ner")
    model = AutoModelForTokenClassification.from_pretrained("hatmimoha/arabic-ner")
    nlp_model = pipeline("ner", model=model, tokenizer=tokenizer)
    
    def tag(self, parts):
        annotations = self.nlp_model(parts)
        print(annotations)
