from random import randint
from vk_api.longpoll import VkLongPoll,VkEventType
import requests
import vk_api
import json
import os
'''
				Надеюсь этот код поможет хоть кому-то получше
				разобраться в VK_API, код написан на языке
			   программирования PYTHON, версия vk_api - 5.103
				       и писал его Евгений Смирнов	
				   ссылка на вк:'https://vk.com/mrlimax'			

																			'''
token_group = os.environ.get('grt') #os.environ.get('grt')
token_app = os.environ.get('apt')


vk_session = vk_api.VkApi(token=token_group) #Токен вашей группы

def get_button(label,color): #Функция по добавлению кнопок в клавиатуру, пример: get_button(ЛЮБОЙ ТЕКСТ, negative)
	return {
		"action": {
			"type": "text",
			"payload":"{\"button\": \"1\"}",
			"label": label,

			},
		"color": color
		}

keyb = { #Основная клавиатура 
	'one_time': False,
	'buttons': [
		[get_button(label="Предложить фото", color="positive"),
		get_button(label="Пожаловаться", color="negative")],
		[get_button(label="Лучшее фото", color="positive"),
		get_button(label="Оставить отзыв", color="default")]
		]


	}
keyb = json.dumps(keyb, ensure_ascii=False).encode('utf-8') #Переводим нашу клавиатуру в json-объект
keyb = str(keyb.decode('utf-8'))                            #Обратно в utf-8 дабы python мог понимать эту ахинею


nazad = { #КНОПКА НАЗАД 
	'one_time': False,
	'buttons': [
		[
		get_button(label="Назад", color="default")
			]
		]
}
nazad = json.dumps(nazad, ensure_ascii=False).encode('utf-8') #Тут также переводим нашу клавиатуру в json-объект
nazad = str(nazad.decode('utf-8'))                            #Обратно в utf-8 дабы python мог понимать эту ахинею

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me: #Если вас НЕ будут волновать документы, фотки видео и тд, то также пропишите:'and event.text'
    #Слушаем longpoll, если пришло сообщение то:			
		if (event.text).lower() == 'привет' or event.text == 'начать' or event.text == 'Начать' : #Если написали заданную фразу
			vk.messages.send( #Отправляем сообщение
				user_id=event.user_id,
				message='Здравствуй! Если ты по удалению моськи тогда скорее нажимай кнопку пожаловаться.',
				random_id= randint(1, 2147483647),
				keyboard=keyb #Отправляем клавиатуру нашему юзеру
		)
		elif (event.text).lower() == 'как дела' or event.text == 'как дела?': #Здесь всё работает точно также, как и в if, только уже с другой командой
			vk.messages.send( #Отправляем сообщение
				user_id=event.user_id,
				message='У меня всё отлично! Рад, что вы интересуетесь мною.',
				random_id= randint(1, 2147483647),
				keyboard=keyb
		)
		elif (event.text).lower() == 'пожаловаться':
			vk.messages.send( #Отправляем сообщение
				user_id=event.user_id,
				message='Если вы хотите пожаловаться на человека, тогда прикрепите его профиль и напишите причину бана, а если вы по удалению моськи, тогда напишите причину(необязательно) и прикрепите пост.',
				random_id= randint(1, 2147483647),
				keyboard=nazad
		)
		elif (event.text).lower() == 'назад':		
			vk.messages.send( #Отправляем сообщение
				user_id=event.user_id,
				message='⠀',
				random_id= randint(1, 2147483647),
				keyboard=keyb
		)
		elif (event.text).lower() == 'предложить фото':
			vk.messages.send( #Отправляем сообщение
			user_id=event.user_id,
			message='Чтобы предложить фото, просто прикрепите его к сообщению и отправьте нам!',
			random_id= randint(1, 2147483647),
			keyboard=nazad
		)
		elif (event.text).lower() == 'оставить отзыв':
			vk.messages.send( #Отправляем сообщение
				user_id=event.user_id,
				message='Напишите свой отзыв ему: vk.com/mrlimax.',
				random_id= randint(1, 2147483647),
				keyboard=keyb
		)
		elif (event.text).lower() == 'лучшее фото':        	
			#Дальше будем парсить записи из группы 'Моськи школьников'
			response = requests.get("https://api.vk.com/method/wall.get?access_token={}&v=5.101&count=100&domain=mocski".format(token_app))
			data= response.json()["response"]['items']
			best_post_likes = 0
			for post in data:
				post_likes = ((post['likes']['count']))      #отбираем самые большие лайки
				if best_post_likes < post_likes:
					best_post_likes=post_likes               #Информация о самых залайканных записях
					best_photo_text = post['text']           #Текст лучшей записи
					photo_id = post                          #Ещё одна новая переменная 
			best_photo_id = ('photo{}_{}'.format(post['owner_id'], photo_id['attachments'][0]['photo']['id']))   #Айди лучшей записи
			vk.messages.send( #Отправляем сообщение
				user_id=event.user_id,
				message='Это лучшая запись. На данный момент на ней {} лайков. Текст записи: {} '.format(best_post_likes, best_photo_text),
				random_id= randint(1, 2147483647),
				keyboard=keyb,
				attachment=best_photo_id
		)
		else:
			#Если сообщение никак не относится к нашим командам, то отправляем сообщение администратору
	#		vk.messages.send(user_id=284389677,message='⠀',random_id = randint(1, 2147483647),keyboard=keyb,forward_messages=event.message_id)
			#Оповещаем пользователя о том, что его сообщение дошло до администрации
			'''
				На самом деле мы не просто оповещаем пользователя, 
				   это небольшой костыль, который защищает нас
				  от непродумости разработчиков VK_API т.к если
				 не отправлять сообщение пользователю, то бот будет
				 бесконечно переотправлять сообщение администратору,
			   из-за того, что бот просто не прочитает его и постоянно
				              будет считать его новым 
																	'''
	#		vk.messages.send(user_id=event.user_id,message='Ваш запрос отправлен администратору',random_id = randint(1, 2147483647),keyboard=keyb)
