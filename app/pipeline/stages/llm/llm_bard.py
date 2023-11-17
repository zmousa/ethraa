from bardapi import BardCookies
import json

class LLMBard:

    def __init__(self, bard_cookie_dict):
        self.bard = BardCookies(cookie_dict=bard_cookie_dict)
    
    def describe(self, word):
        result = self.bard.get_answer("معنى ومرادفات وأضداد وأمثلة كلمة %s على شكل json" % word)
        result_json = result['content'].split('```')[1].replace('،', ',')[4:]
        result_dict = json.loads(result_json)
        return result_dict
        



# Visit https://bard.google.com/
# Open the console
# Session: Application → Cookies → Copy the following values
bard_cookie_dict = {
    "__Secure-1PSID": "",
    "__Secure-1PSIDTS": "",
    "__Secure-1PSIDCC": ""
}

word = "حب"
llmBard = LLMBard(bard_cookie_dict)
print(llmBard.describe(word))
