import requests

#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate_and_write_to_file(input_file_path, output_file_path, from_lang, to_lang='ru'):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    @param input_file_path:
    @param output_file_path:
    @param from_lang:
    @param to_lang:
    """
    with open(input_file_path, encoding='utf-8') as file:
        text = file.readlines()

    params = {
        'key': API_KEY,
        'text': text,
        'lang': f'{from_lang}-{to_lang}',
    }

    response = requests.get(URL, params=params)
    response_content = response.json()
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(''.join(response_content['text']))


# print(translate_it('В настоящее время доступна единственная опция — признак включения в ответ автоматически определенного языка переводимого текста. Этому соответствует значение 1 этого параметра.', 'no'))

if __name__ == '__main__':
    translate_and_write_to_file('DE.txt', 'DE_translated.txt', 'de')
    translate_and_write_to_file('ES.txt', 'ES_translated.txt', 'es')
    translate_and_write_to_file('FR.txt', 'FR_translated.txt', 'fr')
