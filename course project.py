from pprint import pprint
import requests
import os
from tqdm import tqdm, tqdm_gui, trange
import json


class VkApi:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos(self, owner_id):
        get_photos_url = self.url + 'photos.get'
        params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'feed_type': 'photo',
            'photo_sizes': 1,
            # 'offset': 25,
            'count': 5
        }
        res = requests.get(get_photos_url, params={**self.params, **params}).json()['response']['items']
        pprint('Ссылки на фото получены')
        return res


def get_content_file_json():
    res = vk_user.get_photos(input('Введите ID пользователя ВК: '))
    content_list = []
    file_list = []
    for i in range(len(res)):
        photo_content = {'file_name': str(res[i]['likes']['count']) + '.jpg', 'size': res[i]['sizes'][-1]['type'],
                         'url': res[i]['sizes'][-1]['url']}
        content_list.append(photo_content)
    for k in range(len(res)):
        file_content = {'file_name': str(res[k]['likes']['count']) + '.jpg', 'size': res[k]['sizes'][-1]['type']}
        file_list.append(file_content)
    with open('content_file.json', 'w') as f:
        json.dump(file_list, f, ensure_ascii=False, indent=2)
    return content_list


class YandexAPILoader:

    def __init__(self, token):
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {token}'
        }

    def create_new_file(self):
        link_url = self.url
        path = 'Photos_VK'
        params = {
            'path': path
        }
        requests.put(url=link_url, headers=self.headers, params=params).json()
        print('Файл создан')
        return path

    def upload_file(self):
        url = self.url + '/upload'
        content_list = get_content_file_json()
        disk_path = yan.create_new_file()
        for i in tqdm_gui(content_list, desc='Загрузка фото на Яндекс Диск'):
            f = i['file_name']
            path = disk_path + '/' + f
            params = {
                'url': i['url'],
                'path': path,
                'disable_redirects': True
            }
            requests.post(url=url, headers=self.headers, params=params)
        print('Загрузка завершена')


if __name__ == '__main__':
    vk_user = VkApi('', '5.131')
    yan = YandexAPILoader(input('Введите токен с Полигона Яндекс.Диска: '))
    yan.upload_file()
