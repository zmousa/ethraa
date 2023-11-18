from bardapi import BardCookies
import json
import os

class LLMBard:

    def __init__(self):
        # Visit https://bard.google.com/
        # Open the console
        # Session: Application → Cookies → Copy the following values to environment variables
        bard_cookie_dict = {
            "__Secure-1PSID": os.getenv("bardSecure1PSID"),
            "__Secure-1PSIDTS": os.getenv("bardSecure1PSIDTS"),
            "__Secure-1PSIDCC": os.getenv("bardSecure1PSIDCC"),
        }
        self.bard = BardCookies(cookie_dict=bard_cookie_dict)
    
    def describe(self, word):
        result = self.bard.get_answer("معنى ومرادفات وأضداد وأمثلة كلمة %s على شكل json" % word)
        result_json = result['content'].split('```')[1].replace('،', ',')[4:]
        result_dict = json.loads(result_json)
        return result_dict
        

word = "فرح"
llmBard = LLMBard()
print(llmBard.describe(word))
# {
#     "word": "فرح",
#     "meaning": "السعادة والبهجة والسرور",
#     "synonyms": ["ابتهاج", "بهجة", "سرور", "غبطة", "مسرة"],
#     "antonyms": ["حزن", "هم", "غم", "كآبة", "أسى", "ابتأس", "اغتم", "اكتأب", "شقي"],
#     "examples": [
#         "فرحتُ بنجاحه",
#         "أفرحني خبر تخرجك",
#         "فرحتُ كثيراً عندما رأيتك"
#     ]
# }

