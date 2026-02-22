from googletrans import Translator

translator = Translator()
translated = translator.translate("Hello, how are you?", dest='hi')
print(translated.text)
