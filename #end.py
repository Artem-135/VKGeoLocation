import vk
import time

# Выводим на экран название программы и автора
print('VKGeoLocation by mioe')
print('ubuntu-16.04-amd64')
print('---')

# Авторизуем сессию с помощью access token
session = vk.Session('493b9dc31f6601e324013d75eb8a79b545eb3e0c7ec6833d23054b5d018f3f0e776a4f61c8afb103b28b7')

# или с помощью id приложения и данных авторизации пользователя
# session = vk.AuthSession('app id', 'user login', 'user pass')

# Создаем объект API
api = vk.API(session)

# Запрашиваем список всех друзей
friends = api.friends.get()

# Запрос кол-во друзей
print('Кол-во друзей: ' + str(len(friends)))
print('---')

# Получаем список всех друзей
friends = api.friends.get()

# Получаем информацию о всех друзьях
friends_info = api.users.get(user_ids=friends)

# Выводем список друзей в удобном виде
for friend in friends_info:
    print('ID: %s || %s %s' % (friend['uid'], friend['last_name'], friend['first_name']))

# Здесь будут храниться геоданные
geolocation = []

# Получим геоданные всех фотографий каждого друга
# Цикл перебирающий всех друзей
for id in friends:
    # Блокировка
    try:
        print('Получаем данные пользователя: %s' % id)
        # Получаем все альбомы пользователя, кроме служебных
        albums = api.photos.getAlbums(owner_id=id)
        print('\t...aльбомов %s...' % len(albums))
        # Цикл перебирающий все альбомы пользователя
        for album in albums:
            # Обрабатываем исключение для приватных альбомов/фото
            try:
                # Получаем все фотографии из альбома
                photos = api.photos.get(owner_id=id, album_id=album['aid'])
                print('\t\t...обрабатываем фотографии альбома...')
                # Цикл перебирающий все фото в альбоме
                for photo in photos:
                    # Если в фото имеются геоданные, то добавим их в список geolocation
                    if 'lat' in photo and 'long' in photo:
                        # + добавил ссылку на фото и id фото
                        geolocation.append((photo['lat'], photo['long'], photo['src_big'], photo['pid']))
                print('\t\t\t...найдено %s фото...' % len(photos))
            except:
                pass
            # Задержка между запросами photos.get
            time.sleep(0.5)
        # Задержка между запросами photos.getAlbums
        time.sleep(0.5)
    except:
        print('dead :(')
        pass

# Здесь будет хранится сгенерированый js код
js_code = ""

# Проходим по всем геоданным и генерируем js команду добавления маркера
for loc in geolocation:
    js_code += '\nvar marker' + str(
        loc[3]) + ' = new google.maps.Marker({position: {lat: %s, lng: %s}, map: map});\n' % (loc[0], loc[1])
    # Добавить фото в маркер
    js_code += '\n marker' + str(loc[3]) + '.addListener("click", function() {infowindow.setContent("<img src=' + str(
        loc[2]) + '>"' + ');infowindow.open(map, marker' + str(loc[3]) + ');});'

# Считываем из файла-шаблона html данные
html = open('map.html').read()
# Заменяем placeholder на сгенерированный код
html = html.replace('/* PLACEHOLDER */', js_code)

# Записываем данные в новый файл
f = open('VKPhotosGeoLocation.html', 'w')
f.write(html)
f.close()

# Сообщение о завершении работы программы
print('---')
print('end.')