from googletrans import Translator

translator = Translator()
translated = translator.translate('Бороди́нское сраже́ние')

print(translated.text)
