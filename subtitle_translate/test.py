import os
import deepl

auth_key = os.getenv("DEEPL_AUTH_KEY")
translator = deepl.Translator(auth_key)

result = translator.translate_text("Hello, world!", target_lang="ZH")
print(result.text)  # "Bonjour, le monde !"