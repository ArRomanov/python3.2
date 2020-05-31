import os

import requests


#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/


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
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'

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


def upload_translated_files_on_yadisk():
    URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    OAUTH_KEY = ''  # https://yandex.ru/dev/disk/poligon/ - генерация OAuth-токен

    all_files = os.listdir('.')
    translated_files = filter(lambda x: x.endswith('translated.txt'), all_files)
    for file in translated_files:
        with open(file, 'rb') as upload_file:
            params_for_get_url = {
                'path': file,
                'overwrite': True,
            }
            headers = {
                'Authorization': OAUTH_KEY
            }

            generate_upload_link_response = requests.get(URL, headers=headers, params=params_for_get_url)
            response_content = generate_upload_link_response.json()
            upload_link = response_content['href']

            files = {
                'file': upload_file.read()
            }
            requests.put(upload_link, files=files)


if __name__ == '__main__':
    translate_and_write_to_file('DE.txt', 'DE_translated.txt', 'de')
    translate_and_write_to_file('ES.txt', 'ES_translated.txt', 'es')
    translate_and_write_to_file('FR.txt', 'FR_translated.txt', 'fr')
    upload_translated_files_on_yadisk()
