from deep_translator import GoogleTranslator


class TranslateStage:
    google_translator_ar = GoogleTranslator(source='en', target='ar')
    google_translator_en = GoogleTranslator(source='ar', target='en')
    
    def translate_ar(self, input_text: str) -> str:
        #print(f"input: {input_text}")
        translated_text = self.google_translator_ar.translate(input_text)
        #print(f"translated_text: {translated_text}")
        return translated_text
    
    def translate_en(self, input_text: str) -> str:
        translated_text = self.google_translator_en.translate(input_text)
        #print(f"translated_text: {translated_text}")
        return translated_text

