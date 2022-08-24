import config
import asyncio
from random import randint
from aiogram import Bot, Dispatcher, types
from aiogram.types.message import ContentType
from vedis import Vedis
from datetime import datetime, date, timedelta
import functools
import aioschedule
import logging
from aiogram.utils.executor import start_webhook


# loop=loop
# loop = asyncio.get_event_loop()
bot = Bot(token=config.token, parse_mode='MarkdownV2')
dp = Dispatcher(bot)


PRICES = [
    types.LabeledPrice(label='Оформить подписку на месяц', amount=39000),
    types.LabeledPrice(label='Оформить подписку на год', amount=99900)]

PRICES1 = [
    types.LabeledPrice(label='Оформить подписку на месяц + 1', amount=39000),
    types.LabeledPrice(label='Оформить подписку на год + 6мес', amount=99900)]



def get_mainmenu():
    # Генерация клавиатуры главного меню.
    buttons = [
        types.InlineKeyboardButton('«Жизнь, планы, направление»', callback_data='life_area'),
        types.InlineKeyboardButton('«Отношения»', callback_data='relations_area'),
        types.InlineKeyboardButton('«Здоровье»', callback_data='health_area'),
        types.InlineKeyboardButton('«Деньги»', callback_data='money_area'),
        types.InlineKeyboardButton('«Семья»', callback_data='family_area'),
        types.InlineKeyboardButton('«Карьера» (скоро)', callback_data='job_area'),
        types.InlineKeyboardButton('- Как работают МАК -', callback_data='aboutMAK'),
        types.InlineKeyboardButton('- Часто задаваемые вопросы -', callback_data='FAQs')
    ]
    mainmenu = types.InlineKeyboardMarkup(row_width=1)
    mainmenu.add(*buttons)
    return mainmenu






def get_menu_life_area_with_subscription():
    # Генерация клавиатуры меню Сферы "Жизнь, планы, направление" с подпиской.
    buttons = [
        types.InlineKeyboardButton('Техника «Что меня беспокоит»', callback_data='life_area_technique1'),
        types.InlineKeyboardButton('Техника «Маяк»', callback_data='life_area_technique2'),
        types.InlineKeyboardButton('Техника «Перспективы и планы»', callback_data='life_area_technique3'),
        types.InlineKeyboardButton('Техника «Познать себя»', callback_data='life_area_technique4'),
        types.InlineKeyboardButton('← Назад', callback_data='area_back')
    ]
    menu_life_area_with_subscription = types.InlineKeyboardMarkup(row_width=1)
    menu_life_area_with_subscription.add(*buttons)
    return menu_life_area_with_subscription

def get_menu_life_area_without_subscription():
    # Генерация клавиатуры меню Сферы "Жизнь, планы, направление" без платной подписки.
    buttons = [
        types.InlineKeyboardButton('Техника «Что меня беспокоит»', callback_data='life_area_technique1'),
        types.InlineKeyboardButton('Техника «Маяк»', callback_data='life_area_technique2'),
        types.InlineKeyboardButton('Техника «Перспективы и планы» 🔐', callback_data='life_area_technique3'),
        types.InlineKeyboardButton('Техника «Познать себя» 🔐', callback_data='life_area_technique4'),
        types.InlineKeyboardButton('← Назад', callback_data='area_back')
    ]
    menu_life_area_without_subscription = types.InlineKeyboardMarkup(row_width=1)
    menu_life_area_without_subscription.add(*buttons)
    return menu_life_area_without_subscription

@dp.callback_query_handler(text="life_area")  # вызов меню Сферы "Жизнь, планы, направление"
async def life_area(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='*Вы выбрали сферу «Жизнь, планы, направление»*\n'
                                             '\n'
                                             'Выберите нужную Технику:', reply_markup=get_menu_life_area_without_subscription())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='*Вы выбрали сферу «Жизнь, планы, направление»*\n'
                                             '\n'
                                             'Выберите нужную Технику:',
                                        reply_markup=get_menu_life_area_with_subscription())







def get_menu_relations_area_with_subscription():
    # Генерация клавиатуры меню Сферы "Отношения" с подпиской.
    buttons = [
        types.InlineKeyboardButton('Техника «Моя половинка»', callback_data='relations_area_technique1'),
        types.InlineKeyboardButton('Техника «Я в отношениях»', callback_data='relations_area_technique2'),
        types.InlineKeyboardButton('← Назад', callback_data='area_back')
    ]
    menu_relations_area_with_subscription = types.InlineKeyboardMarkup(row_width=1)
    menu_relations_area_with_subscription.add(*buttons)
    return menu_relations_area_with_subscription

def get_menu_relations_area_without_subscription():
    # Генерация клавиатуры меню Сферы "Отношения" без платной подписки.
    buttons = [
        types.InlineKeyboardButton('Техника «Моя половинка» 🔐', callback_data='relations_area_technique1'),
        types.InlineKeyboardButton('Техника «Я в отношениях» 🔐', callback_data='relations_area_technique2'),
        types.InlineKeyboardButton('← Назад', callback_data='area_back')
    ]
    menu_relations_area_without_subscription = types.InlineKeyboardMarkup(row_width=1)
    menu_relations_area_without_subscription.add(*buttons)
    return menu_relations_area_without_subscription

@dp.callback_query_handler(text="relations_area")  # вызов меню Сферы "Отношения"
async def relations_area(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='*Вы выбрали сферу «Отношения»*\n'
                                             '\n'
                                             'Выберите нужную Технику:', reply_markup=get_menu_relations_area_without_subscription())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='*Вы выбрали сферу «Отношения»*\n'
                                             '\n'
                                             'Выберите нужную Технику:',
                                        reply_markup=get_menu_relations_area_with_subscription())







def get_menu_health_area_with_subscription():
    # Генерация клавиатуры меню Сферы "Здоровье" с подпиской.
    buttons = [
        types.InlineKeyboardButton('Техника «Моя любимая болячка»', callback_data='health_area_technique1'),
        types.InlineKeyboardButton('Техника «Моё здоровье»', callback_data='health_area_technique2'),
        types.InlineKeyboardButton('Техника «Уроки моего тела»', callback_data='health_area_technique3'),
        types.InlineKeyboardButton('← Назад', callback_data='area_back')
    ]
    menu_health_area_with_subscription = types.InlineKeyboardMarkup(row_width=1)
    menu_health_area_with_subscription.add(*buttons)
    return menu_health_area_with_subscription

def get_menu_health_area_without_subscription():
    # Генерация клавиатуры меню Сферы "Здоровье" без платной подписки.
    buttons = [
        types.InlineKeyboardButton('Техника «Моя любимая болячка» 🔐', callback_data='health_area_technique1'),
        types.InlineKeyboardButton('Техника «Моё здоровье» 🔐', callback_data='health_area_technique2'),
        types.InlineKeyboardButton('Техника «Уроки моего тела» 🔐', callback_data='health_area_technique3'),
        types.InlineKeyboardButton('← Назад', callback_data='area_back')
    ]
    menu_health_area_without_subscription = types.InlineKeyboardMarkup(row_width=1)
    menu_health_area_without_subscription.add(*buttons)
    return menu_health_area_without_subscription

@dp.callback_query_handler(text="health_area")  # вызов меню Сферы "Здоровье"
async def health_area(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='*Вы выбрали сферу «Здоровье»*\n'
                                             '\n'
                                             'Выберите нужную Технику:', reply_markup=get_menu_health_area_without_subscription())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='*Вы выбрали сферу «Здоровье»*\n'
                                             '\n'
                                             'Выберите нужную Технику:',
                                        reply_markup=get_menu_health_area_with_subscription())






def get_menu_money_area_with_subscription():
    # Генерация клавиатуры меню Сферы "Деньги" с подпиской.
    buttons = [
        types.InlineKeyboardButton('Техника «Деньги в моей жизни»', callback_data='money_area_technique1'),
        types.InlineKeyboardButton('Техника «Моя денежная цель»', callback_data='money_area_technique2'),
        types.InlineKeyboardButton('← Назад', callback_data='area_back')
    ]
    menu_money_area_with_subscription = types.InlineKeyboardMarkup(row_width=1)
    menu_money_area_with_subscription.add(*buttons)
    return menu_money_area_with_subscription

def get_menu_money_area_without_subscription():
    # Генерация клавиатуры меню Сферы "Деньги" без платной подписки.
    buttons = [
        types.InlineKeyboardButton('Техника «Деньги в моей жизни» 🔐', callback_data='money_area_technique1'),
        types.InlineKeyboardButton('Техника «Моя денежная цель» 🔐', callback_data='money_area_technique2'),
        types.InlineKeyboardButton('← Назад', callback_data='area_back')
    ]
    menu_money_area_without_subscription = types.InlineKeyboardMarkup(row_width=1)
    menu_money_area_without_subscription.add(*buttons)
    return menu_money_area_without_subscription

@dp.callback_query_handler(text="money_area")  # вызов меню Сферы "Деньги"
async def money_area(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='*Вы выбрали сферу «Деньги»*\n'
                                             '\n'
                                             'Выберите нужную Технику:', reply_markup=get_menu_money_area_without_subscription())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='*Вы выбрали сферу «Деньги»*\n'
                                             '\n'
                                             'Выберите нужную Технику:',
                                        reply_markup=get_menu_money_area_with_subscription())






def get_menu_family_area_with_subscription():
    # Генерация клавиатуры меню Сферы "Семья" с подпиской.
    buttons = [
        types.InlineKeyboardButton('Техника «Я в семье»', callback_data='family_area_technique1'),
        types.InlineKeyboardButton('← Назад', callback_data='area_back')
    ]
    menu_family_area_with_subscription = types.InlineKeyboardMarkup(row_width=1)
    menu_family_area_with_subscription.add(*buttons)
    return menu_family_area_with_subscription

def get_menu_family_area_without_subscription():
    # Генерация клавиатуры меню Сферы "Семья" без платной подписки.
    buttons = [
        types.InlineKeyboardButton('Техника «Я в семье» 🔐', callback_data='family_area_technique1'),
        types.InlineKeyboardButton('← Назад', callback_data='area_back')
    ]
    menu_family_area_without_subscription = types.InlineKeyboardMarkup(row_width=1)
    menu_family_area_without_subscription.add(*buttons)
    return menu_family_area_without_subscription

@dp.callback_query_handler(text="family_area")  # вызов меню Сферы "Семья"
async def family_area(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='*Вы выбрали сферу «Семья»*\n'
                                             '\n'
                                             'Выберите нужную Технику:', reply_markup=get_menu_family_area_without_subscription())
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='*Вы выбрали сферу «Семья»*\n'
                                             '\n'
                                             'Выберите нужную Технику:',
                                        reply_markup=get_menu_family_area_with_subscription())





# Сфера карьера
@dp.callback_query_handler(text="job_area")
async def job_area(call: types.CallbackQuery):
    job_area_menu = types.InlineKeyboardMarkup()
    button_job_area_menu = types.InlineKeyboardButton(text='← Назад', callback_data='area_back')
    job_area_menu.add(button_job_area_menu)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Разработчики работают над добавлением этой Сферы и новых Техник\. Скоро они станут доступны\.\n'
                                                                                                       '\n'
                                                                                                       'Вернуться назад:', reply_markup=job_area_menu)



@dp.callback_query_handler(text="area_back")
async def area_back(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Вы в главном меню*\n'
                                                                                                       '\n'
                                                                                                       'Выберите нужную Сферу жизни:', reply_markup=get_mainmenu())









def get_subscription_menu():
    # Генерация клавиатуры меню платной подписки.
    buttons = [
        types.InlineKeyboardButton('Оформить подписку на месяц', callback_data='subscription_month'),
        types.InlineKeyboardButton('Оформить подписку на год', callback_data='subscription_year'),
        types.InlineKeyboardButton('В главное меню', callback_data='mainmenu')
    ]
    subscription_menu = types.InlineKeyboardMarkup(row_width=1)
    subscription_menu.add(*buttons)
    return subscription_menu


def get_first_subscription_menu():
    # Генерация клавиатуры меню платной подписки впервые, с особым предложением.
    buttons = [
        types.InlineKeyboardButton('Оформить подписку на месяц + 1', callback_data='first_subscription_month'),
        types.InlineKeyboardButton('Оформить подписку на год + 6мес', callback_data='first_subscription_year'),
        types.InlineKeyboardButton('В главное меню', callback_data='first_mainmenu')
    ]
    subscription_menu = types.InlineKeyboardMarkup(row_width=1)
    subscription_menu.add(*buttons)
    return subscription_menu


def get_yes_no_menu():
    # Генерация клавиатуры меню выбора, продлевать или нет подписку.
    buttons = [
        types.InlineKeyboardButton('Конечно, да', callback_data='subscription_yes'),
        types.InlineKeyboardButton('Спасибо, но нет', callback_data='subscription_no'),
    ]
    subscription_yes_no_menu = types.InlineKeyboardMarkup(row_width=1)
    subscription_yes_no_menu.add(*buttons)
    return subscription_yes_no_menu


def get_jamp_mainmenu():
    # Генерация клавиатуры с кнопкой "В главное меню".
    buttons = [types.InlineKeyboardButton(text='В главное меню', callback_data='mainmenu')]
    jamp_mainmenu = types.InlineKeyboardMarkup(row_width=1)
    jamp_mainmenu.add(*buttons)
    return jamp_mainmenu




@dp.callback_query_handler(text="mainmenu")  # вызов главного меню
async def mainmenu(call: types.CallbackQuery):
    await call.message.answer('*Вы в главном меню*\n'
                              '\n'
                              'Выберите нужную Сферу жизни:', reply_markup=get_mainmenu())


@dp.callback_query_handler(text="first_mainmenu")  # вызов главного меню после первого предложения платной подписки
async def first_mainmenu(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        db.Set('First').remove(call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='*Вы в главном меню*\n'
                                     '\n'
                                     'Выберите нужную Сферу жизни:', reply_markup=get_mainmenu())




back = types.InlineKeyboardButton(text='В главное меню', callback_data='mainmenu') # кнопка "В главное меню"




# список карт (колода) для техники 1

pict = ['https://www.dropbox.com/s/cekj0beskcwwydz/1.jpg?dl=0',
        'https://www.dropbox.com/s/u7882fkv3kpocr8/2.jpg?dl=0',
        'https://www.dropbox.com/s/p23l4tby472wv3t/3.jpg?dl=0',
        'https://www.dropbox.com/s/77h8jb8kfbhzmz7/4.jpg?dl=0',
        'https://www.dropbox.com/s/zszwp95wglldbib/10.jpg?dl=0',
        'https://www.dropbox.com/s/0au38jisnmu9t8p/11.jpg?dl=0',
        'https://www.dropbox.com/s/nn9nhd5blmnpfw5/12.jpg?dl=0',
        'https://www.dropbox.com/s/6436mcmj96isveb/13.jpg?dl=0',
        'https://www.dropbox.com/s/sfyj43zn5jwio1e/14.jpg?dl=0',
        'https://www.dropbox.com/s/m0nrrrvgxn2fen8/15.jpg?dl=0',
        'https://www.dropbox.com/s/fvsja29xfwgvhou/16.jpg?dl=0',
        'https://www.dropbox.com/s/ek3gcdu5f4vmluz/17.jpg?dl=0',
        'https://www.dropbox.com/s/r7xijxbw6v5v2hi/18.jpg?dl=0',
        'https://www.dropbox.com/s/we0we76i6jof1ma/19.jpg?dl=0',
        'https://www.dropbox.com/s/iaz2ihd6bwwm8d7/20.jpg?dl=0',
        'https://www.dropbox.com/s/nce6mh72pxakb1s/21.jpg?dl=0',
        'https://www.dropbox.com/s/flow1beno5678pn/22.jpg?dl=0',
        'https://www.dropbox.com/s/lkhzuvd3j05yu4z/23.jpg?dl=0',
        'https://www.dropbox.com/s/uqyctpu1bl7o9a3/24.jpg?dl=0',
        'https://www.dropbox.com/s/3qzk93dpduy9p36/25.jpg?dl=0',
        'https://www.dropbox.com/s/ez618ay28q6r4qo/26.jpg?dl=0',
        'https://www.dropbox.com/s/2d115uoe0khl6d8/27.jpg?dl=0',
        'https://www.dropbox.com/s/igynxr4fo4h4idj/28.jpg?dl=0',
        'https://www.dropbox.com/s/5y2af2cjs5y21sx/29.jpg?dl=0',
        'https://www.dropbox.com/s/u0vq84hts56dfla/30.jpg?dl=0',
        'https://www.dropbox.com/s/pddpnjx3aeksy8m/31.jpg?dl=0',
        'https://www.dropbox.com/s/kt5yy5w2h5ql2y4/32.jpg?dl=0',
        'https://www.dropbox.com/s/zg4p3kmuakcol4j/33.jpg?dl=0',
        'https://www.dropbox.com/s/dfgzxjgzhmjrxhx/34.jpg?dl=0',
        'https://www.dropbox.com/s/fzn5h2wng0jjput/35.jpg?dl=0',
        'https://www.dropbox.com/s/yd7w3zk2nrr9l1w/36.jpg?dl=0',
        'https://www.dropbox.com/s/pz05kw2pf5zd82r/37.jpg?dl=0',
        'https://www.dropbox.com/s/mlzbuxqy7d4ph2j/38.jpg?dl=0',
        'https://www.dropbox.com/s/4vah84b3nlt3lir/39.jpg?dl=0',
        'https://www.dropbox.com/s/85858wn9lwivioy/40.jpg?dl=0',
        'https://www.dropbox.com/s/c281vm8uror1gul/41.jpg?dl=0',
        'https://www.dropbox.com/s/wwaeqs2ivb13spp/42.jpg?dl=0',
        'https://www.dropbox.com/s/fxpzoe4xa26fqb7/43.jpg?dl=0',
        'https://www.dropbox.com/s/vil9amkx92aqwa4/44.jpg?dl=0',
        'https://www.dropbox.com/s/dzyano7ctnxb9u8/45.jpg?dl=0',
        'https://www.dropbox.com/s/2327v12cay07yux/1.jpg?dl=0',
        'https://www.dropbox.com/s/ischq2823o18j9f/2.jpg?dl=0',
        'https://www.dropbox.com/s/7fn1973y4f7bqmn/3.jpg?dl=0',
        'https://www.dropbox.com/s/g3lfhxo0uxuf4nu/4.jpg?dl=0',
        'https://www.dropbox.com/s/i293fihpneb57hu/5.jpg?dl=0',
        'https://www.dropbox.com/s/6g5mkdhimzk22qv/6.jpg?dl=0',
        'https://www.dropbox.com/s/0n7l49kkqb7mz29/7.jpg?dl=0',
        'https://www.dropbox.com/s/ze3lgsfqlgq2wrm/8.jpg?dl=0',
        'https://www.dropbox.com/s/0bhvcpdooiel8rc/9.jpg?dl=0',
        'https://www.dropbox.com/s/bggbi49281sirff/10.jpg?dl=0',
        'https://www.dropbox.com/s/igewq8f8c7r9gmt/11.jpg?dl=0',
        'https://www.dropbox.com/s/o380bvpti6vtyiy/12.jpg?dl=0',
        'https://www.dropbox.com/s/1oaqv4p129zcipq/13.jpg?dl=0',
        'https://www.dropbox.com/s/i25x9wzayhgc291/14.jpg?dl=0',
        'https://www.dropbox.com/s/ratvt8mp9zaamr9/15.jpg?dl=0',
        'https://www.dropbox.com/s/gex6hsn8y2glswe/17.jpg?dl=0',
        'https://www.dropbox.com/s/dd9444dyd5iry5w/18.jpg?dl=0',
        'https://www.dropbox.com/s/mpez827de4dsctw/19.jpg?dl=0',
        'https://www.dropbox.com/s/eg979svazt8rnd1/20.jpg?dl=0',
        'https://www.dropbox.com/s/43gne3jhqdcz1m9/21.jpg?dl=0',
        'https://www.dropbox.com/s/zlzkx28d32qt853/22.jpg?dl=0',
        'https://www.dropbox.com/s/6o6e0cwxoa4kllv/23.jpg?dl=0',
        'https://www.dropbox.com/s/vvox2ir3fhwaqr7/24.jpg?dl=0',
        'https://www.dropbox.com/s/9esh7iimot94ozv/25.jpg?dl=0',
        'https://www.dropbox.com/s/877sewqgec4ruk9/26.jpg?dl=0',
        'https://www.dropbox.com/s/ir8atu7b83btmz4/28.jpg?dl=0',
        'https://www.dropbox.com/s/tschlmkkk2gz1sz/29.jpg?dl=0',
        'https://www.dropbox.com/s/gt8k4wfs8h5d2bg/30.jpg?dl=0',
        'https://www.dropbox.com/s/cudus75cbbe91nq/31.jpg?dl=0',
        'https://www.dropbox.com/s/dtpa1b9kl4gg541/32.jpg?dl=0',
        'https://www.dropbox.com/s/a3ld9uwlrm73dla/33.jpg?dl=0',
        'https://www.dropbox.com/s/o2fimb37k5rqf1g/34.jpg?dl=0',
        'https://www.dropbox.com/s/7yvrna69ru6qci7/35.jpg?dl=0',
        'https://www.dropbox.com/s/l71r8bhhutlqv0q/36.jpg?dl=0',
        'https://www.dropbox.com/s/9h9xyextpmmq4cz/37.jpg?dl=0',
        'https://www.dropbox.com/s/q6ni6rmlxdb7a57/38.jpg?dl=0',
        'https://www.dropbox.com/s/st4eys9eb8ys2h3/39.jpg?dl=0',
        'https://www.dropbox.com/s/52fddh68ut9y13a/40.jpg?dl=0',
        'https://www.dropbox.com/s/wbquowa35cpg6ae/41.jpg?dl=0',
        'https://www.dropbox.com/s/amylj95cd3xc09y/42.jpg?dl=0',
        'https://www.dropbox.com/s/e820jdoowjf7se1/43.jpg?dl=0',
        'https://www.dropbox.com/s/87982wvvnzzwdnj/44.jpg?dl=0',
        'https://www.dropbox.com/s/ogwpnfwh15lzgsl/45.jpg?dl=0',
        'https://www.dropbox.com/s/cadkfscuot3p2mt/46.jpg?dl=0',
        'https://www.dropbox.com/s/7iab41ea8tej31h/47.jpg?dl=0',
        'https://www.dropbox.com/s/8xjn6who7rw3mvp/48.jpg?dl=0',
        'https://www.dropbox.com/s/ic1uzgwbymdnu41/49.jpg?dl=0',
        'https://www.dropbox.com/s/lk51attzlk304oa/50.jpg?dl=0',
        'https://www.dropbox.com/s/5u1g4akvn49ibwr/51.jpg?dl=0',
        'https://www.dropbox.com/s/tn70qzar54ohzsv/52.jpg?dl=0',
        'https://www.dropbox.com/s/moyka5r2u9ywr0g/53.jpg?dl=0',
        'https://www.dropbox.com/s/yjvd2sh8ocpsy1k/54.jpg?dl=0',
        'https://www.dropbox.com/s/wwvjz1k4d1xkjn7/55.jpg?dl=0',
        'https://www.dropbox.com/s/mk12lblk9t1dupd/56.jpg?dl=0',
        'https://www.dropbox.com/s/impdw07o5halg6t/57.jpg?dl=0',
        'https://www.dropbox.com/s/pv35p98x4v5eahx/58.jpg?dl=0',
        'https://www.dropbox.com/s/fnrlqgrtwkmg097/59.jpg?dl=0',
        'https://www.dropbox.com/s/iu8piaprxakn4rf/60.jpg?dl=0',
        'https://www.dropbox.com/s/qrxn8xge32gvhak/61.jpg?dl=0',
        'https://www.dropbox.com/s/xq9xvidl3bp4muu/62.jpg?dl=0',
        'https://www.dropbox.com/s/8y71zqavr461rjx/63.jpg?dl=0',
        'https://www.dropbox.com/s/ld1sebswbrw1tnj/64.jpg?dl=0',
        'https://www.dropbox.com/s/j07dzhhi5zs5igq/65.jpg?dl=0',
        'https://www.dropbox.com/s/ih7f1893o6s0w0m/66.jpg?dl=0',
        'https://www.dropbox.com/s/viw6genbdywhcjf/67.jpg?dl=0',
        'https://www.dropbox.com/s/wu69atpf2q8oji7/68.jpg?dl=0',
        'https://www.dropbox.com/s/czq0az3wrlsxs63/69.jpg?dl=0',
        'https://www.dropbox.com/s/tfujxqs62357mtb/70.jpg?dl=0',
        'https://www.dropbox.com/s/rjyjf0u1apwggk3/71.jpg?dl=0',
        'https://www.dropbox.com/s/byt7mzg5e237qz3/72.jpg?dl=0',
        'https://www.dropbox.com/s/2f5gxs0tmh3f50p/1.jpg?dl=0',
        'https://www.dropbox.com/s/9s8sviv2hq6o60x/2.jpg?dl=0',
        'https://www.dropbox.com/s/puj0syasdqxyoa6/3.jpg?dl=0',
        'https://www.dropbox.com/s/xp78a2ssuuq66c7/4.jpg?dl=0',
        'https://www.dropbox.com/s/qs0698yk8nhj61g/10.jpg?dl=0',
        'https://www.dropbox.com/s/m54798p9g4upy01/11.jpg?dl=0',
        'https://www.dropbox.com/s/aw0qb27ywvz8tpm/12.jpg?dl=0',
        'https://www.dropbox.com/s/iaj1h7l5rkg77jg/13.jpg?dl=0',
        'https://www.dropbox.com/s/xdit58mzehbxpn7/14.jpg?dl=0',
        'https://www.dropbox.com/s/w3g5dvwdhem0mn2/15.jpg?dl=0',
        'https://www.dropbox.com/s/kmt71tjdu244ns1/16.jpg?dl=0',
        'https://www.dropbox.com/s/tsqiqjd8fmst2c7/17.jpg?dl=0',
        'https://www.dropbox.com/s/jq2zjy1ruaq9khe/18.jpg?dl=0',
        'https://www.dropbox.com/s/9489gx7cyp92zz6/19.jpg?dl=0',
        'https://www.dropbox.com/s/mybd2mpmytsaar2/20.jpg?dl=0',
        'https://www.dropbox.com/s/xg4naoj60g6fby8/21.jpg?dl=0',
        'https://www.dropbox.com/s/w70o5nvf60krl9w/22.jpg?dl=0',
        'https://www.dropbox.com/s/ttvda0uehqfsvy4/23.jpg?dl=0',
        'https://www.dropbox.com/s/mkd8zi3erxlwj7f/24.jpg?dl=0',
        'https://www.dropbox.com/s/xpfbcrcalds15nl/25.jpg?dl=0',
        'https://www.dropbox.com/s/u26ecjyunwxa2f9/26.jpg?dl=0',
        'https://www.dropbox.com/s/o660it4mptyiimr/27.jpg?dl=0',
        'https://www.dropbox.com/s/8o7y1t95t90uhok/28.jpg?dl=0',
        'https://www.dropbox.com/s/dagmbuzicqyr8xv/29.jpg?dl=0',
        'https://www.dropbox.com/s/1gzlopljpko5obb/30.jpg?dl=0',
        'https://www.dropbox.com/s/5jldwa40hs4qeei/31.jpg?dl=0',
        'https://www.dropbox.com/s/xma9efi3i9ddjjm/32.jpg?dl=0',
        'https://www.dropbox.com/s/3oetymlm4tuk08v/33.jpg?dl=0',
        'https://www.dropbox.com/s/3y1r83mi8ccyf1u/34.jpg?dl=0',
        'https://www.dropbox.com/s/2xbomqyjhflk4sm/35.jpg?dl=0',
        'https://www.dropbox.com/s/jpliv3x8rrs9e4f/36.jpg?dl=0',
        'https://www.dropbox.com/s/p5yl8zl3v8oiai4/37.jpg?dl=0',
        'https://www.dropbox.com/s/9ecnh15o8734da5/38.jpg?dl=0',
        'https://www.dropbox.com/s/stv34jwv0ehpp8x/39.jpg?dl=0',
        'https://www.dropbox.com/s/pt4hczwfi7v92ov/40.jpg?dl=0',
        'https://www.dropbox.com/s/9teulbkwyuimo2g/41.jpg?dl=0',
        'https://www.dropbox.com/s/g86t0fv6c97u85o/42.jpg?dl=0',
        'https://www.dropbox.com/s/ygr5vm9dq7jalgi/43.jpg?dl=0',
        'https://www.dropbox.com/s/38pqd1z7syj5199/44.jpg?dl=0',
        'https://www.dropbox.com/s/pixqo5svfl9bbkc/45.jpg?dl=0',
        'https://www.dropbox.com/s/3gsi7utxqfj5ger/46.jpg?dl=0',
        'https://www.dropbox.com/s/1qcjjoh7c7dmp47/47.jpg?dl=0',
        'https://www.dropbox.com/s/lxgl0x7hrq81fki/48.jpg?dl=0',
        'https://www.dropbox.com/s/cd0tt2uyidplnlf/49.jpg?dl=0',
        'https://www.dropbox.com/s/8kqa3hi5pxvkas3/50.jpg?dl=0',
        'https://www.dropbox.com/s/v90jl2ndw1jho3q/51.jpg?dl=0',
        'https://www.dropbox.com/s/6ucp08vhw2rwvkj/52.jpg?dl=0',
        'https://www.dropbox.com/s/si56oqg086wvp91/53.jpg?dl=0',
        'https://www.dropbox.com/s/9lqwsodzayr3btw/54.jpg?dl=0',
        'https://www.dropbox.com/s/0yhutifsazkqy2k/55.jpg?dl=0',
        'https://www.dropbox.com/s/sghrzske6dj2su5/56.jpg?dl=0',
        'https://www.dropbox.com/s/jq8znsyf23dltnb/57.jpg?dl=0',
        'https://www.dropbox.com/s/uidyqetob95hi8f/58.jpg?dl=0',
        'https://www.dropbox.com/s/uvre0q9e7vbwknh/59.jpg?dl=0',
        'https://www.dropbox.com/s/0tedzbml9tzdgil/60.jpg?dl=0',
        'https://www.dropbox.com/s/r3hy64mu8assb20/61.jpg?dl=0',
        'https://www.dropbox.com/s/htm159pgbslv5yv/62.jpg?dl=0',
        'https://www.dropbox.com/s/lg3acbmwsukhl05/63.jpg?dl=0',
        'https://www.dropbox.com/s/dbw9kube5zgn7fj/64.jpg?dl=0',
        'https://www.dropbox.com/s/wtz5b1va3ychf7s/65.jpg?dl=0',
        'https://www.dropbox.com/s/cbxi1jtcp38zqn6/66.jpg?dl=0',
        'https://www.dropbox.com/s/f6ze6dxdg2txwyz/67.jpg?dl=0',
        'https://www.dropbox.com/s/cnha4zr2xr9vljq/68.jpg?dl=0',
        'https://www.dropbox.com/s/nhcom366ydrv4u0/69.jpg?dl=0',
        'https://www.dropbox.com/s/h57sx71bho62il6/70.jpg?dl=0',
        'https://www.dropbox.com/s/vtdkzagfg3z3jnb/71.jpg?dl=0',
        'https://www.dropbox.com/s/fdf5egua309q77v/72.jpg?dl=0',
        'https://www.dropbox.com/s/8ipls97hp8a8t0r/73.jpg?dl=0',
        'https://www.dropbox.com/s/ptti1rfdiuxravh/74.jpg?dl=0',
        'https://www.dropbox.com/s/9k7xb178wmob9z2/75.jpg?dl=0',
        'https://www.dropbox.com/s/5d7lfl1ewrofh2b/76.jpg?dl=0',
        'https://www.dropbox.com/s/wdoz72nwba2tndq/77.jpg?dl=0',
        'https://www.dropbox.com/s/tpn5l4jp17iz3p2/78.jpg?dl=0',
        'https://www.dropbox.com/s/2c5ksrfty1lcjdq/79.jpg?dl=0',
        'https://www.dropbox.com/s/d8f8zcnwdf8mt44/80.jpg?dl=0']

pict_money = ['https://www.dropbox.com/s/w71l837qfyzr97b/1.jpg?dl=0',
              'https://www.dropbox.com/s/4nwosnfs5tiew1o/2.jpg?dl=0',
              'https://www.dropbox.com/s/vv1dpu4m5grzsuc/3.jpg?dl=0',
              'https://www.dropbox.com/s/stvv7uzpjhuskjq/4.jpg?dl=0',
              'https://www.dropbox.com/s/utoltanp9s6erzi/5.jpg?dl=0',
              'https://www.dropbox.com/s/lpaum70jao92gpg/6.jpg?dl=0',
              'https://www.dropbox.com/s/gi1tu3z6dbiuqw2/7.jpg?dl=0',
              'https://www.dropbox.com/s/qgzusiqgzwkcq9y/8.jpg?dl=0',
              'https://www.dropbox.com/s/tiy7vklgw1rtxqr/9.jpg?dl=0',
              'https://www.dropbox.com/s/3zka57m58nppbeo/10.jpg?dl=0',
              'https://www.dropbox.com/s/wovnjiikw2tqedk/11.jpg?dl=0',
              'https://www.dropbox.com/s/g48gcur7kwdj5yo/12.jpg?dl=0',
              'https://www.dropbox.com/s/4ogdcczsyjcwuf0/13.jpg?dl=0',
              'https://www.dropbox.com/s/7l8fiw705y6qqr0/14.jpg?dl=0',
              'https://www.dropbox.com/s/9yebxujo9jdensj/15.jpg?dl=0',
              'https://www.dropbox.com/s/ptq9vl2lf250d5n/16.jpg?dl=0',
              'https://www.dropbox.com/s/dndbgk14lum7asr/17.jpg?dl=0',
              'https://www.dropbox.com/s/yke7g8qpdl023fm/18.jpg?dl=0',
              'https://www.dropbox.com/s/iyhkyopx019jet8/19.jpg?dl=0',
              'https://www.dropbox.com/s/hztbnw88b0pxolw/20.jpg?dl=0',
              'https://www.dropbox.com/s/76bc9an7ntdfzuw/21.jpg?dl=0',
              'https://www.dropbox.com/s/282292gno4fm7zp/22.jpg?dl=0',
              'https://www.dropbox.com/s/xpkwb9cmzpf7zei/23.jpg?dl=0',
              'https://www.dropbox.com/s/80mk9tgiv7idjjs/24.jpg?dl=0',
              'https://www.dropbox.com/s/2lwdzeo078338oy/25.jpg?dl=0',
              'https://www.dropbox.com/s/ex9rvay6p5itmqk/26.jpg?dl=0',
              'https://www.dropbox.com/s/j1ic1lmznbmpdw9/27.jpg?dl=0',
              'https://www.dropbox.com/s/gt6di8jyz8a22x4/28.jpg?dl=0',
              'https://www.dropbox.com/s/fltibk8hl9kk8sg/29.jpg?dl=0',
              'https://www.dropbox.com/s/slfsifj6o0fcbzc/30.jpg?dl=0',
              'https://www.dropbox.com/s/nq3czrvv4k5k9ge/31.jpg?dl=0',
              'https://www.dropbox.com/s/d74q38m1lqeiu96/32.jpg?dl=0',
              'https://www.dropbox.com/s/ceebppdjhr9g8eq/33.jpg?dl=0',
              'https://www.dropbox.com/s/6c1vl35quiupyph/34.jpg?dl=0',
              'https://www.dropbox.com/s/ai5rrsp7d3zbxt8/35.jpg?dl=0',
              'https://www.dropbox.com/s/syj40lx32ity510/36.jpg?dl=0',
              'https://www.dropbox.com/s/6s3azng7zeu535t/37.jpg?dl=0',
              'https://www.dropbox.com/s/fu1esx88huv6nu9/38.jpg?dl=0',
              'https://www.dropbox.com/s/dhv6z79520j4nwm/39.jpg?dl=0',
              'https://www.dropbox.com/s/1vugs737bhs3bxz/40.jpg?dl=0',
              'https://www.dropbox.com/s/igniot0tief5xsp/41.jpg?dl=0',
              'https://www.dropbox.com/s/ayxyffnhvexjcwu/42.jpg?dl=0',
              'https://www.dropbox.com/s/esdahjem0ajkkj6/43.jpg?dl=0',
              'https://www.dropbox.com/s/d3elaps9nmnrvy3/44.jpg?dl=0',
              'https://www.dropbox.com/s/qnk1x4cf76iht4v/45.jpg?dl=0',
              'https://www.dropbox.com/s/1lvlzu4fgjq6eps/46.jpg?dl=0',
              'https://www.dropbox.com/s/tbqogu9vi7kcjli/47.jpg?dl=0',
              'https://www.dropbox.com/s/34740rvlhxvplhw/48.jpg?dl=0',
              'https://www.dropbox.com/s/l9p826x502j2ko3/49.jpg?dl=0',
              'https://www.dropbox.com/s/b8evdj48w7y42fe/50.jpg?dl=0',
              'https://www.dropbox.com/s/1bkdfz5ycx6if8v/51.jpg?dl=0',
              'https://www.dropbox.com/s/n5w7q7yvcki85ik/52.jpg?dl=0',
              'https://www.dropbox.com/s/iv0pc0jst2mn8o6/53.jpg?dl=0',
              'https://www.dropbox.com/s/xiibak6uwqi0lmg/54.jpg?dl=0',
              'https://www.dropbox.com/s/937uw80si6wvi3q/55.jpg?dl=0',
              'https://www.dropbox.com/s/gmf57szjz3tt0hm/56.jpg?dl=0',
              'https://www.dropbox.com/s/79jhlsh8gv6n7zr/57.jpg?dl=0',
              'https://www.dropbox.com/s/akaxtznnpso9ws7/58.jpg?dl=0',
              'https://www.dropbox.com/s/ttoslnw6dpz495i/59.jpg?dl=0',
              'https://www.dropbox.com/s/9ml8miy1jz4cee1/60.jpg?dl=0',
              'https://www.dropbox.com/s/d2m3pha4nnz91vp/62.jpg?dl=0',
              'https://www.dropbox.com/s/adphhns2g0tnz3z/63.jpg?dl=0',
              'https://www.dropbox.com/s/raefb1fcvoousrk/64.jpg?dl=0',
              'https://www.dropbox.com/s/90luutqykx5fg7b/65.jpg?dl=0',
              'https://www.dropbox.com/s/dhm85zujfjmrav3/66.jpg?dl=0',
              'https://www.dropbox.com/s/gtp9rnxymeh0wvm/67.jpg?dl=0',
              'https://www.dropbox.com/s/o0te65lmxf9n7bf/68.jpg?dl=0',
              'https://www.dropbox.com/s/pv9ztii3x41k3r2/69.jpg?dl=0',
              'https://www.dropbox.com/s/q6c104sey2yfni0/70.jpg?dl=0',
              'https://www.dropbox.com/s/18hn4ta957jjc9z/71.jpg?dl=0',
              'https://www.dropbox.com/s/3cy98n6mjn69vds/72.jpg?dl=0',
              'https://www.dropbox.com/s/1nwcxprdoq970nw/73.jpg?dl=0',
              'https://www.dropbox.com/s/bgns5szprei37rx/74.jpg?dl=0',
              'https://www.dropbox.com/s/69vroln2n1yry55/75.jpg?dl=0',
              'https://www.dropbox.com/s/v5kdgqfp5ppihs0/76.jpg?dl=0',
              'https://www.dropbox.com/s/ll8mo7xie0kqd3z/77.jpg?dl=0',
              'https://www.dropbox.com/s/td1t96oa9njic9k/78.jpg?dl=0',
              'https://www.dropbox.com/s/won6o963nf7bt2h/79.jpg?dl=0',
              'https://www.dropbox.com/s/0s13428gstyt8xs/80.jpg?dl=0',
              'https://www.dropbox.com/s/nj5jfoitspsul7a/81.jpg?dl=0',
              'https://www.dropbox.com/s/76knsoe9byvw2pe/82.jpg?dl=0',
              'https://www.dropbox.com/s/wbvk1qnrbhrwsdt/83.jpg?dl=0',
              'https://www.dropbox.com/s/rqx2vjjfeff8h1s/84.jpg?dl=0',
              'https://www.dropbox.com/s/no4i5wb3qu4o7cv/85.jpg?dl=0',
              'https://www.dropbox.com/s/8jcnio5ar9056nu/86.jpg?dl=0',
              'https://www.dropbox.com/s/9ja80g08mwz3ez7/87.jpg?dl=0',
              'https://www.dropbox.com/s/gv5pucsj2avf0wv/88.jpg?dl=0',
              'https://www.dropbox.com/s/oqudknad50jzyxa/89.jpg?dl=0',
              'https://www.dropbox.com/s/x67baex2j4n2k07/90.jpg?dl=0',
              'https://www.dropbox.com/s/tf7xr65e1ob1mge/91.jpg?dl=0',
              'https://www.dropbox.com/s/p201wui59cxnbzb/92.jpg?dl=0',
              'https://www.dropbox.com/s/6kbalhaj6abihd5/93.jpg?dl=0',
              'https://www.dropbox.com/s/r2tyhs8icv43edp/94.jpg?dl=0',
              'https://www.dropbox.com/s/y4mxa0yr7jos4l1/95.jpg?dl=0',
              'https://www.dropbox.com/s/rq9qh7cugfw4tox/96.jpg?dl=0',
              'https://www.dropbox.com/s/w2np3hnwzmg92ar/97.jpg?dl=0',
              'https://www.dropbox.com/s/xymbqve5rr35vle/98.jpg?dl=0',
              'https://www.dropbox.com/s/fjij6uuimzcxpy5/99.jpg?dl=0',
              'https://www.dropbox.com/s/08wqd8org9xnndk/100.jpg?dl=0']







@dp.message_handler(commands=["start"]) # обработка команды start
async def cmd_start(message):
    user = str(message.chat.id)
    with Vedis(config.db_file) as db:
        if user not in db.Set('All_users'):
            await message.answer("*Искренне рад вас приветствовать\!*\n"
                                 "\n"
                                "И сильно постараюсь сделать вашу жизнь более счастливой\!\n"
                                "\n"
                                "Потому что, вряд ли найдется абсолютно счастливый человек, у которого нет никаких проблем или затыков хотя бы в одной из сфер жизни, да?\n"
                                "\n"
                                "\- У кого\-то проблемы в семье, \n"
                                 "\n"
                                 "\- кто\-то не может пробить потолок в доходах или карьере, \n"
                                 "\n"
                                 "\- кто\-то борется с болезнью \n"
                                 "\n"
                                 "\- или никак не может встретить свою вторую половинку…\n"
                                "\n"
                                "И у многих это происходит не один год\. Накапливается стресс, депрессия, растет неудовлетворенность жизнью, которая превращается в «День сурка»\. Нет развития и ничего не меняется\.\n"
                                "\n"
                                "Но в этом нет вашей вины\. К сожалению, никому из нас при рождении не вкладывают инструкцию по эксплуатации жизни\. Нам приходится самим подбирать к ней ключи\.\n"
                                "\n"
                                "*И я дам вам не просто один из ключей, я дам вам настоящий чит\-код, который выведет вас на новый уровень*\n"
                                "\n"
                                "Это быстрый и легкий способ разобраться с *истинными* причинами ваших проблем и избавиться от них\.\n"
                                "\n"
                                "И самое главное — всё, что для этого нужно, у вас уже есть\. Я лишь помогу достать это наружу, и вы увидите, насколько это просто\.\n"
                                "\n"
                                "И для этого нам понадобятся *Метафорические Ассоциативные Карты \(МАК\)*\.\n" 
                                "\n"
                                "Если вы впервые слышите, что это за карты такие, и сомневаетесь в том, что я вам наобещал, то сначала сходите в раздел «Как работают МАК» — вас ждут удивительные открытия\. "
                                 "Я расскажу, как и почему это работает\. Гарантирую — никакой магии или эзотерики, чистая наука\.\n"
                                "\n"
                                "Ну, а если вы уже знаете, что такое МАК, то просто нажмите на «Главное меню» и выберите нужную сферу жизни, а затем Технику из списка\.\n"
                                )
            db[user + 'start'] = date.today()
            db.Set('All_users').add(user)
            db.Set('First').add(user)

        else:
            await message.answer("*Вы вернулись в самое начало*\n"
                                 "\n"
                                 "Нажмите кнопку «Как работают МАК» или «Часто задаваемые вопросы», чтобы узнать больше о том, как работают Метафорические Ассоциативные Карты\.\n"
                                 "\n"
                                 "Или кнопку «Главное меню», чтобы начать сессию с нужной сферой жизни и доступными Техниками\.\n"
                                 )

    startmenu = types.InlineKeyboardMarkup(row_width=1)
    button_mainmenu = types.InlineKeyboardButton('Главное меню', callback_data='mainmenu')
    button_aboutMAK = types.InlineKeyboardButton('Как работают МАК', callback_data='aboutMAK')
    button_aboutFAQs = types.InlineKeyboardButton('Часто задаваемые вопросы', callback_data='FAQs')
    startmenu.add(button_mainmenu, button_aboutMAK, button_aboutFAQs)
    await message.answer('Итак, куда дальше?', reply_markup=startmenu)









# Обработка отправки боту любого текстового сообщения, кроме команд
@dp.message_handler(lambda message: message.from_user.id != config.admin and message.text.strip().lower() not in ('/start'))
async def cmd_sample_message(message):
    await message.answer("На самом деле, я хоть и умный бот, но не прям, чтобы уж очень\.\n"
                         "\n"
                              "Я не знаю, что вы хотели этим сказать\. Пожалуйста, пользуйтесь кнопками меню\.\n"
                         "\n"
                              "Или нажмите /start чтобы запустить новый диалог с самого начала\.\n", reply_markup=get_jamp_mainmenu())










# кнопки для администратора
def get_admin_menu():
    # Генерация клавиатуры меню администратора.
    buttons = [
        types.InlineKeyboardButton('Статистика', callback_data='stats'),
        types.InlineKeyboardButton('Рассылка', callback_data='newsletter'),
        types.InlineKeyboardButton('В главное меню', callback_data='mainmenu')
    ]
    admin_menu = types.InlineKeyboardMarkup(row_width=2)
    admin_menu.add(*buttons)
    return admin_menu


def get_newsletter_menu():
    # Генерация клавиатуры меню рассылки.
    buttons = [
        types.InlineKeyboardButton('Всем пользователям', callback_data='send_all'),
        types.InlineKeyboardButton('Тем, у кого нет платной подписки', callback_data='send_not_pay'),
        types.InlineKeyboardButton('← Назад', callback_data='admin_back1')
    ]
    newsletter_menu = types.InlineKeyboardMarkup(row_width=1)
    newsletter_menu.add(*buttons)
    return newsletter_menu


def back_to_admin_menu():
    # Генерация клавиатуры с кнопкой "Назад в меню администратора".
    buttons = [types.InlineKeyboardButton(text='← Назад', callback_data='admin_back1')]
    back_to_admin_menu = types.InlineKeyboardMarkup(row_width=1)
    back_to_admin_menu.add(*buttons)
    return back_to_admin_menu


def back_to_newsletter_menu():
    # Генерация клавиатуры с кнопкой "Назад в меню рассылки".
    buttons = [types.InlineKeyboardButton(text='← Назад', callback_data='admin_back2')]
    back_to_newsletter_menu = types.InlineKeyboardMarkup(row_width=1)
    back_to_newsletter_menu.add(*buttons)
    return back_to_newsletter_menu


@dp.message_handler(commands=["admin"]) # обработка команды admin
async def cmd_admin(message):
    if message.chat.id == config.admin:
        await message.answer('Что будем делать?', reply_markup=get_admin_menu())
    else:
        await message.answer('Кажется, у вас нет прав администратора', reply_markup=get_jamp_mainmenu())



@dp.callback_query_handler(text="newsletter")
async def newsletter(call: types.CallbackQuery):
    # Обработка меню "Рассылка"
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Кому будем рассылать сообщение?', reply_markup=get_newsletter_menu())


@dp.callback_query_handler(text="admin_back1")
async def admin_back1(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Что будем делать?', reply_markup=get_admin_menu())


@dp.callback_query_handler(text="admin_back2")
async def admin_back2(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Кому будем рассылать сообщение?', reply_markup=get_newsletter_menu())


@dp.callback_query_handler(text="send_all")
async def send_all(call: types.CallbackQuery):
    # Обработка меню "Рассылка всем"
    global send_all
    send_all = 1
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Пришли сообщение, которое будем рассылать', reply_markup=back_to_newsletter_menu())


@dp.callback_query_handler(text="send_not_pay")
async def send_not_pay(call: types.CallbackQuery):
    # Обработка меню "Рассылка тем, у кого нет платной подписки"
    global send_not_pay
    send_not_pay = 1
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Пришли сообщение, которое будем рассылать', reply_markup=back_to_newsletter_menu())


@dp.message_handler()
async def send_all_go(message: types.Message):
    global send_all
    global send_not_pay
    if message.from_user.id == config.admin and send_all == 1:
        text = message.text
        with Vedis(config.db_file) as db:
            for i in db.Set('All_users'):
                try:
                    await bot.send_message(i.decode(), text)
                    if i.decode() in db.Set('Blocked'):
                        db.Set('Blocked').remove(i.decode())
                except:
                    db.Set('Blocked').add(i.decode())
        await bot.send_message(message.from_user.id, 'Рассылка завершена', reply_markup=back_to_admin_menu())
        send_all = 0

    if message.from_user.id == config.admin and send_not_pay == 1:
        text = message.text
        with Vedis(config.db_file) as db:
            S = db.Set('All_users') - db.Set('Pay')
            for i in S:
                try:
                    await bot.send_message(i.decode(), text)
                    if i.decode() in db.Set('Blocked'):
                        db.Set('Blocked').remove(i.decode())
                except:
                    db.Set('Blocked').add(i.decode())
        await bot.send_message(message.from_user.id, 'Рассылка завершена', reply_markup=back_to_admin_menu())
        send_not_pay = 0


@dp.callback_query_handler(text="stats")
async def stats(call: types.CallbackQuery):
    # Обработка меню "Статистика"
    with Vedis(config.db_file) as db:
        Sum24, Sum72 = 0, 0
        Sum24_month, Sum72_month = 0, 0
        Sum24_year, Sum72_year = 0, 0
        try:
            All_month = len(db.Set('Month'))
        except:
            All_month = 0
        try:
            All_year = len(db.Set('Year'))
        except:
            All_year = 0
        try:
            All_extend_month = len(db.Set('Extend_status_month'))
        except:
            All_extend_month = 0
        try:
            All_extend_year = len(db.Set('Extend_status_year'))
        except:
            All_extend_year = 0
        try:
            All_blocked = len(db.Set('Blocked'))
        except:
            All_blocked = 0

        All = len(db.Set('All_users'))

        try:
            for user in db.Set('All_users'):
                datetime_str_year = datetime.strptime(str(db[user.decode() + 'start'].decode()), "%Y-%m-%d")
                db_date = datetime.date(datetime_str_year)
                if db_date == date.today() or db_date == (date.today() - timedelta(days=1)):
                    Sum24 += 1
                if db_date == date.today() or db_date == (date.today() - timedelta(days=1)) or db_date == (date.today() - timedelta(days=2)) or db_date == (date.today() - timedelta(days=3)):
                    Sum72 += 1
        except:
            pass

        try:
            for user in db.Set('Month'):
                datetime_str_year = datetime.strptime(str(db[user.decode() + 'pay_start'].decode()), "%Y-%m-%d")
                db_date = datetime.date(datetime_str_year)
                if db_date == date.today() or db_date == (date.today() - timedelta(days=1)):
                    Sum24_month += 1
                if db_date == date.today() or db_date == (date.today() - timedelta(days=1)) or db_date == (date.today() - timedelta(days=2)) or db_date == (date.today() - timedelta(days=3)):
                    Sum72_month += 1
        except:
            pass

        try:
            for user in db.Set('Year'):
                datetime_str_year = datetime.strptime(str(db[user.decode() + 'pay_start'].decode()), "%Y-%m-%d")
                db_date = datetime.date(datetime_str_year)
                if db_date == date.today()  or db_date == (date.today() - timedelta(days=1)):
                    Sum24_year += 1
                if db_date == date.today()  or db_date == (date.today() - timedelta(days=1)) or db_date == (date.today() - timedelta(days=2)) or db_date == (date.today() - timedelta(days=3)):
                    Sum72_year += 1
        except:
            pass

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'*Статистика:*\n \n'
                                                                                                           f'Всего человек в боте: *{All}*\n'
                                                                                                       f'Заблокировали бота: *{All_blocked}*\n'
                                                                                                           f'Подписалось за сутки: *{Sum24}*\n'
                                                                                                           f'Подписалось за трое суток: *{Sum72}*\n \n'
                                                                                                       f'Всего оплатили платную подписку: *{All_month + All_year}*\n'
                                                                                                       f'*Из них:*\n'
                                                                                                       f'Платных подписок на месяц: *{All_month}*\n'
                                                                                                       f'Платных подписок на год: *{All_year}*\n \n'
                                                                                                       f'*Детальнее:*\n'
                                                                                                       f'Платных подписок на месяц за сутки: *{Sum24_month}*\n'
                                                                                                       f'Платных подписок на месяц за 3 суток: *{Sum72_month}*\n \n'
                                                                                                       f'Платных подписок на год за сутки: *{Sum24_year}*\n'
                                                                                                       f'Платных подписок на год за 3 суток: *{Sum72_year}*\n \n*Продления подписки:*\n'
                                                                                                       f'Всего продлили подписку: *{All_extend_month + All_extend_year}*\n'
                                                                                                       f'*Из них:*\n'
                                                                                                       f'Продлили на месяц: *{All_extend_month}*\n'
                                                                                                       f'Продлили на год: *{All_extend_year}*\n \n', reply_markup=back_to_admin_menu())










def get_demonstration_menu():
    # Генерация клавиатуры меню выбора, демонстрировать или нет технику.
    buttons = [
        types.InlineKeyboardButton('Покажи', callback_data='about_mak_continue1'),
        types.InlineKeyboardButton('Пропустить', callback_data='about_mak_skip1'),
    ]
    demonstration_menu = types.InlineKeyboardMarkup(row_width=2)
    demonstration_menu.add(*buttons)
    return demonstration_menu

# 0 обработка меню "Как работают МАК" (после нажатия кнопки "Как работают МАК")
@dp.callback_query_handler(text="aboutMAK")
async def aboutMAK(call: types.CallbackQuery):
    await call.message.answer("*Итак\. Что такое МАК?*\n"
                              "\n"
                              "Чисто технически — это такие колоды карт, но не игральных или гадальных, типа «ТАРО», а карты с изображенными на них картинками\. "
                              "Самыми разными\. \n"
                              "\n"
                              "На самом деле, это может быть вообще любая картинка, чуть позже вы поймете почему\.\n"
                              "\n"
                              "А сейчас, вместо долгой болтовни, давайте я лучше сразу покажу на примере — и вам тут же станет понятно, как они выглядят и для чего нужны\. \n"
                              "\n"
                              "А уже потом расскажу, как и почему они работают, ок?", reply_markup=get_demonstration_menu())

@dp.callback_query_handler(text="about_mak_continue1")
# вызов техники "Заноза" из раздела "О МАК"
async def about_mak_continue1(call: types.CallbackQuery):
    await call.message.answer('Сейчас мы с вами проделаем Технику, которая называется *«Что меня беспокоит»*\. Это займёт буквально минуты 3\-4\.\n'
                                "\n"
                                "*Вот что нужно делать:*\n"
                                "\n"
                                "Задайте себе \(как бы внутрь себя\) вопрос: «Какая проблема меня сейчас беспокоит больше всего?»\n"
                                "\n"
                                "И, как будете готовы, нажмите кнопку «Показать карту»\.\n"
                                "\n"
                                "А я побуду вашей рукой и вытяну случайную карту из колоды\. Вам нужно будет посмотреть на картинку, и ответить себе на вопросы:\n"
                                "\n"
                                "\- Что я там вижу?\n"
                                "\- Что там происходит?\n"
                                "\- Что это за ситуация?\n"
                                "\- Где на карте я?\n"
                                "\- Как это связано с моим вопросом?\n"
                                "\- Что же меня действительно сейчас беспокоит больше всего?\n"
                                "\n"
                                "Не обязательно ответить прям на все вопросы, это общий алгоритм для понимания\. "
                              "Дальше вы будете делать это за доли секунды, просто отвечая на свой главный вопрос\.\n"
                                "\n"
                                "*Совет:* старайтесь долго не думать, отмечайте первое, что придёт в голову — обычно, это самый верный ответ\. "
                              "А лучше записывайте их на бумажку — так будет проще делать выводы и, особенно, следить за изменениями "
                              "в ваших запросах через какое\-то время\.\n")

    about_mak_next_menu1 = types.InlineKeyboardMarkup()
    about_mak_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='about_mak_ready1')
    about_mak_next_menu1.add(about_mak_key1)
    await call.message.answer('Итак, ещё раз — задайте внутрь себя вопрос: *«Какая проблема меня сейчас беспокоит больше всего?»* и нажмите кнопку «Показать карту»', reply_markup=about_mak_next_menu1)
@dp.callback_query_handler(text="about_mak_ready1")
async def about_mak_ready1(call: types.CallbackQuery):
    about_mak_pict1 = pict.copy()
    about_mak_next_menu2 = types.InlineKeyboardMarkup()
    about_mak_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='about_mak_next1')
    about_mak_next_menu2.add(about_mak_key2)
    x = about_mak_pict1[randint(0, len(about_mak_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что вы на ней видите? И что \(о чём\) это в вашей жизни? Какая проблема вас беспокоит?\n'
                              '\n'
                            'Как закончите, нажмите кнопку «Дальше»', reply_markup=about_mak_next_menu2)
    about_mak_pict1.remove(x)
    global about_mak_pict2
    about_mak_pict2 = about_mak_pict1.copy()
@dp.callback_query_handler(text="about_mak_next1")
async def about_mak_next1(call: types.CallbackQuery):
    await call.message.answer("Отлично\! Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*А что мне делать с этой проблемой?*")
    about_mak_next_menu3 = types.InlineKeyboardMarkup()
    about_mak_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='about_mak_ready2')
    about_mak_next_menu3.add(about_mak_key3)
    await call.message.answer('И затем нажмите кнопку «Показать карту»', reply_markup=about_mak_next_menu3)
@dp.callback_query_handler(text="about_mak_ready2")
async def about_mak_ready2(call: types.CallbackQuery):
    global about_mak_pict2
    about_mak_next_menu4 = types.InlineKeyboardMarkup()
    about_mak_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='about_mak_next2')
    about_mak_next_menu4.add(about_mak_key4)
    x = about_mak_pict2[randint(0, len(about_mak_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите здесь? И что вам надо сделать в вашей жизни?\n'
                              '\n'
                                'Как будете готовы, нажмите «Дальше»', reply_markup=about_mak_next_menu4)
    about_mak_pict2.remove(x)
    global about_mak_pict3
    about_mak_pict3 = about_mak_pict2.copy()
@dp.callback_query_handler(text="about_mak_next2")
async def about_mak_next2(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос, который вы себе задаёте:\n"
                     "\n"
                     "*Какой первый шаг мне нужно сделать?*")
    about_mak_next_menu5 = types.InlineKeyboardMarkup()
    about_mak_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='about_mak_ready3')
    about_mak_next_menu5.add(about_mak_key5)
    await call.message.answer('И снова нажимаете кнопку «Показать карту»', reply_markup=about_mak_next_menu5)
@dp.callback_query_handler(text="about_mak_ready3")
async def about_mak_ready3(call: types.CallbackQuery):
    global about_mak_pict3
    about_mak_next_menu6 = types.InlineKeyboardMarkup()
    about_mak_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='about_mak_next3')
    about_mak_next_menu6.add(about_mak_key6)
    x = about_mak_pict3[randint(0, len(about_mak_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Как закончите, нажмите «Дальше»', reply_markup=about_mak_next_menu6)
@dp.callback_query_handler(text="about_mak_next3")
async def about_mak_next3(call: types.CallbackQuery):
    await call.message.answer('Ну, как ощущения? 🙂\n'
                              "\n"
                              'Удалось найти ответ на вопрос? Если нет, не переживайте — не у всех получается с первого раза\. '
                              'Но точно работает у всех, после небольшой тренировки\.\n'
                              '\n'
                              '*А теперь я объясню, что с вами сейчас такое было*\n')
    about_mak_next_menu7 = types.InlineKeyboardMarkup()
    about_mak_key7 = types.InlineKeyboardButton(text='Продолжить', callback_data='about_mak_skip1')
    about_mak_next_menu7.add(about_mak_key7)
    await call.message.answer('Нажмите «Продолжить»', reply_markup=about_mak_next_menu7)

about_mak_key9 = types.InlineKeyboardButton(text='Пропустить', callback_data='about_mak_skip2')

@dp.callback_query_handler(text="about_mak_skip1")
async def about_mak_skip1(call: types.CallbackQuery):
    about_mak_next_menu8 = types.InlineKeyboardMarkup(row_width=1)
    about_mak_key8 = types.InlineKeyboardButton(text='Конечно! Рассказывай!', callback_data='about_mak_continue2')
    about_mak_next_menu8.add(about_mak_key8, about_mak_key9)
    await call.message.answer('Если не сильно умничать, то произошло с вами буквально следующее:\n'
                              '\n'
                              '1️⃣ Вы сознательно задали внутрь себя вопрос, обращаясь к бессознательной части психики\.\n'
                              '\n'
                              '2️⃣ Когда вы вытаскивали карту и смотрели на картинку, у вас включалось образное правое полушарие мозга\. '
                              'Картинка тут же начинала вызывать ассоциации, связанные с вашим вопросом, доставая их, опять таки, '
                              'из вашей бессознательной части психики, из глубин вашей долгосрочной памяти\.\n'
                              '\n'
                              'Кстати, в этот момент, ваше сознание почти не может этому помешать, если только вы не начинаете усиленно стараться\. '
                              'Именно поэтому, когда смотрите на карту, лучше не думать дольше 6\-10 секунд, '
                              'иначе это уже будет не ответ вашего бессознательного, а вы начнёте обманывать сами себя\.\n'
                              '\n'
                              '3️⃣ Дальше, уже снова сознательной частью психики, своим левым \(логическим\) полушарием мозга, '
                              'увиденные образы вы преобразовали в ответ на ваш вопрос\.\n'
                              '\n'
                              'И всё это за секунды, хотя скоро вы научитесь делать это ещё быстрее\.\n'
                              '\n'
                              '*И вот что здесь самое главное*\n'
                              '\n'
                              'Сама картинка тут совершенно не важна\!\n'
                              '\n'
                              'Одна и та же карта у разных людей будет вызывать разные образы и ассоциации, потому что '
                              'жизненный опыт и знания, хранящиеся в бессознательном, у каждого свои\.\n'
                              '\n'
                              'Более того\! Одна и та же картинка для одного человека, но с разными запросами, тоже будет вызывать разные ассоциации\.\n'
                              '\n'
                              'В картинках каждый человек ВСЕГДА увидит ровно то, что беспокоит только его, связанное только с его ситуацией и заданным вопросом\.\n'
                              '\n'
                              'Этим, кстати, МАК и отличаются, например, от карт ТАРО или гадания на любых других картах\. '
                              'В гадании каждая карта имеет какое\-то толкование, которое вам объясняет человек\-оператор и рассказывает, что вам с этим делать\.\n'
                              '\n'
                              'А в МАК вы сами растолковываете для себя, что увидели, и сами делаете выводы\. Это делает ваш собственный мозг, задействуя обе свои составляющие\.\n'
                              '\n'
                              'И это одинаково работает абсолютно для всех людей\.\n'
                              '\n'
                              'Интересно узнать поподробнее, почему наш мозг функционирует именно так?', reply_markup=about_mak_next_menu8)

@dp.callback_query_handler(text="about_mak_continue2")
async def about_mak_continue2(call: types.CallbackQuery):
    about_mak_next_menu9 = types.InlineKeyboardMarkup()
    about_mak_key10 = types.InlineKeyboardButton(text='Продолжай', callback_data='about_mak_continue3')
    about_mak_next_menu9.add(about_mak_key10, about_mak_key9)
    await call.message.answer('Смотрите, если сильно упростить, наш мозг, условно, можно разделить на две части:\n'
                              '\n'
                              '1️⃣ На верхнем этаже \(в неокортексе\) живёт Сознание\. Это самое последнее звено эволюции мозга\. '
                              'Это то, что отличает нас от животных\. Здесь формируются мысли, речь, логика, сила воли… '
                              'Короче, это такой умный умник, который нами управляет\. По крайней мере, он так думает \)\n'
                              '\n'
                              '2️⃣ На нижних этажах живет Бессознательное\. И здесь же располагается хранилище нашей долгосрочной памяти\. '
                              'В него наш мозг складывает буквально всё, что когда\-либо с нами происходило\. '
                              'Весь наш жизненный опыт с самого рождения, который, по его мнению, поможет нам в реализации '
                              'трёх главных целей нашего существования — выжить, размножиться и задоминировать\.\n'
                              '\n'
                              'Но складывает в ячейки памяти он не слова и предложения, а образы: '
                              'картинки, звуки, ощущения, запахи, вкусы — всё то, что получает от органов чувств\.\n'
                              '\n'
                              'И в этом ему, как раз, и помогает бессознательная часть психики \(мы делаем это неосознанно\)\. '
                              'Она постоянно собирает, анализирует и хранит все поступающие извне данные\. '
                              'И выдаёт только самое необходимое \(в конкретный момент времени\) на уровень Сознания, '
                              'которое, в свою очередь, вербализует полученные образы в понятные нам мысли и слова\.\n'
                              '\n'
                              'Множеством научных экспериментов доказано, что сознание в поле своего внимания может удерживать лишь 7±2 объекта\. '
                              'То есть не больше 9 объектов одновременно\. '
                              'Всё, что выше — перегружает сознание, и человек уже не может контролировать происходящее\.\n'
                              '\n'
                              'Бессознательное же может обрабатывать несколько миллионов \(а может и больше\) операций в секунду\. '
                              'Это настоящий суперкомпьютер у нас в голове\. И оно хранит просто колоссальный объем информации\! '
                              'Оно гораздо \(гораздо\!\) умнее Сознания\.\n'
                              '\n'
                              'И теперь самое главное\!\n'
                              '\n'
                              '*Что бы нас не беспокоило, какой бы вопрос нас не волновал, наше бессознательное уже с этим сталкивалось и знает ответ — он есть в его хранилище*\n'
                              '\n'
                              'Иначе этого вопроса просто не возникло бы у нас в Сознании\. Осталось только понять, как вытащить этот ответ наружу\. '
                              'И вот с этим, как раз, и помогают Метафорические Ассоциативные Карты\!\n'
                              '\n'
                              '*Как и почему это работает*\n'
                              '\n'
                              'Продолжаем или ну его? \)', reply_markup=about_mak_next_menu9)

@dp.callback_query_handler(text="about_mak_continue3")
async def about_mak_continue3(call: types.CallbackQuery):
    about_mak_next_menu10 = types.InlineKeyboardMarkup()
    about_mak_key10 = types.InlineKeyboardButton(text='Дальше', callback_data='about_mak_skip2')
    about_mak_next_menu10.add(about_mak_key10)
    await call.message.answer('Неокортекс думает, что он самый умный, потому что в нём рождаются мысли и слова\. '
                              'И не просто мысли, но и домыслы и попытки переосмыслить прошлое или предсказать \(выдумать\) будущее\. '
                              'Эта мыслемешалка никогда не останавливается\.\n'
                              '\n'
                              'Более того\. У него есть способность подавлять силой воли низлежащие этажи\. Сигналы от Бессознательного\.'
                              'И часто, вместе с этим он подавляет то, что у нас реально болит или что нам реально хочется\. '
                              'Заметает проблемы под ковер, глушит наши истинные эмоции и чувства в наших же \(как он думает\) интересах\.\n'
                              '\n'
                              'Но МАК позволяет обходить этот барьер, проскальзывая мимо неокортекса, и не вызывая у него подозрений\.\n'
                              '\n'
                              'Смотря на картинку, вы мгновенно проваливаетесь в Бессознательное именно потому, что это и есть его язык — язык образов\. '
                              'Сознание не успевает этому помешать, потому что Бессознательное намного быстрее, и вы видите то, что всплыло из него на ваш запрос\.'
                              'То, что оно хранило в своих закромах по этому вопросу\.\n'
                              '\n'
                              '*МАК — это проводник к вашему гиперумному суперкомпьютеру и его огромной памяти\.*\n'
                              '\n'
                              'Как шахматный компьютер анализирует каждый возможный ход из миллионов загруженных в него партий и выдает наиболее эффективный,\n'
                              '\n'
                              'так и\n'
                              '\n'
                              'Бессознательное прежде, чем сохранить информацию о чём\-то, на базе всех своих накопленных данных, анализирует все возможные '
                              'исходы по любым ситуациям, связанным с этим предметом\. '
                              'И сохраняет себе самое важное и главное, что только может быть по этому вопросу\.\n'
                              '\n'
                              'И когда мы к нему обращаемся, оно выдает именно это самое главное\.\n'
                              '\n'
                              '*И к этому, как минимум, стоит отнестись очень внимательно, правда?*\n'
                              '\n'
                              'Вот так они и работают\.\n'
                              '\n'
                              'И, если немного потренироваться, осечек не бывает\.', reply_markup=about_mak_next_menu10)

@dp.callback_query_handler(text="about_mak_skip2")
async def about_mak_skip2(call: types.CallbackQuery):
    await call.message.answer('*Вот почему МАК:*\n'
                              '\n'
                              '\- это универсальный, очень быстрый и безопасный метод, который можно использовать практически во всех ситуациях и даже детям;\n'
                              '\n'
                              '\- помогают преодолеть внутреннее сопротивление, которое часто не поддается больше никакой методике;\n'
                              '\n'
                              '\- так полюбились многим современным психологам, что они всё чаще применяют их в своей практике\.\n'
                              '\n'
                              '*И разве не круто, что вы теперь сможете использовать МАК самостоятельно?*\n'
                              '\n'
                              'Где угодно и когда угодно\! Дома, в пробке, в метро, на работе…\n'
                              '\n'
                              'Тогда, когда чувства и ситуация обострены, и нужно быстро и эффективно принять решение, '
                              'посоветовавшись со своим мудрым Бессознательным\.\n'
                              '\n'
                              'И вы можете быть абсолютно честны с собой, вам не придётся никому рассказывать о том, '
                              'что вы видите, и с какими событиями это связано\. Никто, кроме вас, не узнает то, что вы выяснили с помощью МАК\.\n'
                              '\n'
                              '*А значит вы получите максимально точные ответы и рекомендации к действию\!*\n'
                              '\n'
                              '✅ Вы сможете понять, в чём *истинная* причина ваших проблем\.\n'
                              '\n'
                              '✅ Подружитесь со своим внутренним «я», и будете чувствовать себя более гармоничным и счастливым человеком\.\n'
                              '\n'
                              '✅ Очень скоро увидите, как растет качество вашей жизни во всех сферах\.\n'
                              '\n'
                              '✅ Разовьёте своё абстрактное и креативное мышление и логические способности\.\n'
                              '\n'
                              '✅ Будете излучать энергию и спокойную сильную уверенность\.\n'
                              '\n'
                              'Ну что, готовы к удивительным открытиям?\n'
                              '\n'
                              'Тогда пора переходить к Техникам — нажмите кнопку «В главное меню»\n'
                              '\n'
                              'P\.S\. И… позвольте дать ещё один совет прежде, чем мы начнём… '
                              '*Чем чаще вы будете пользоваться этими Техниками, тем быстрее будут происходить невероятные изменения в вашей жизни\. Проверено\.*', reply_markup=get_jamp_mainmenu())








@dp.callback_query_handler(text="FAQs")
async def FAQs(call: types.CallbackQuery):
    await call.message.answer('*1\. Это что — эзотерика? Магия? Астрология? Гадания на картах? Я не верю в такие вещи*\n'
                              '\n'
                              'МАК — это полностью научный метод, основанный на особенностях работы нашего мозга\. '
                              'Сходите в раздел «Как работают МАК», там более подробно об этом\.\n'
                              '\n'
                              '*2\. Это точно работает? Больше похоже на какую\-то забаву, а не на серьёзный метод психологической помощи*\n'
                              '\n'
                              'Вот именно так описывают свое отношение к МАК большинство психологов до реального знакомства с ними\. '
                              'Но после изучения вопроса и небольшой практики, метафорические карты становятся для них чуть ли не основным инструментом '
                              'диагностики проблем клиентов\. Потому что убеждаются, что мало какой метод может сравниться с МАК в скорости, '
                              'безопасности и эффективности проникновения в самую суть проблемы, с которой обращается человек\. А значит быстрого её устранения\.\n'
                              '\n'
                              '*3\. Я смотрю на карты, но ничего, связанного с моей жизнью, не приходит на ум\. Я ничего не вижу*\n'
                              '\n'
                              'Тут могут быть несколько причин:\n'
                              '\n'
                              '\- Как и другие навыки, навык общения со своим Бессознательным нужно тренировать\. '
                              'Чем чаще вы будете это делать, тем быстрее и точнее будете получать ответы\.\n'
                              '\n'
                              '\- Часто, если ответ не приходит, вы \(ваше сознание\) сопротивляетесь\. Расслабьтесь\. '
                              'Останьтесь наедине, где вас никто не потревожит\. Отбросьте все сомнения\. Чего вам терять или бояться? Просто попробуйте\. '
                              'Всё, что вы выясните, останется лишь при вас\. И очень хотелось бы посмотреть, насколько сильно вы удивитесь, '
                              'когда мир вокруг вас скоро начнёт меняться…\n'
                              '\n'
                              'Как ещё с этим можно поработать\. Вы смотрите в карту и задаёте себе прямые буквальные вопросы: '
                              '«Что я там вижу?», «Что там происходит?», «Что это за ситуация?»… «А где в карте я?»…\n'
                              '\n'
                              '\- А бывает и так, что если у вас всё нормально в заданном вопросе, карты вам это и показывают — значит всё хорошо, продолжайте\.\n'
                              '\n'
                              '\- Если же вы чувствуете дискомфорт или негатив, возможно, Бессознательное блокирует доступ в эту область\. '
                              'Тогда стоит обратить на неё особое внимание\. И, если не получается поисследовать её самомстоятельно, может быть, стоит сходить с этим вопросом к психологу, чтобы выяснить причину\.\n'
                              '\n'
                              '*4\. Как понять, что я не обманываю себя, что это действительно ответ моего Бессознательного?*\n'
                              '\n'
                              'Очень важно постараться уловить эмоциональный отклик от картинки, реакцию тела, потому что тело \(эмоция\) никогда не врёт\.\n'
                              '\n'
                              '*5\. Можно ли использовать МАК детям?*\n'
                              '\n'
                              'Никаких противопоказаний для этого нет\. Наоборот — дети гораздо быстрее и легче налаживают связь со своим Бессознательным, '
                              'в силу, как раз, своего возраста и необременения жизненными проблемами и многолетним опытом\.\n'
                              '\n'
                              '*Если у вас есть вопросы, пожелания, критика… По работе бота, по добавлению новых Техник или карт… '
                              'вы можете написать в нашу [службу поддержки](https://t.me/M_S_L_assistant_bot) — мы обязательно рассмотрим все обращения*', reply_markup=get_jamp_mainmenu())











# Сфера "Жизнь, планы, направление"
# 1 вызов техники "Что меня беспокоит" (после нажатия кнопки выбора техники "Что меня беспокоит")
@dp.callback_query_handler(text="life_area_technique1")
async def life_area_technique1(call: types.CallbackQuery):
    await call.message.answer('Ок\. Вы выбрали Технику *«Что меня беспокоит»*\.\n'
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                              "\n"
                              "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
    await call.message.answer("Теперь задайте себе вопрос:\n"
                                 "\n"
                                 "*Какая проблема меня сейчас беспокоит больше всего?*")
    technique1_next_menu1 = types.InlineKeyboardMarkup()
    technique1_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique1_ready1')
    technique1_next_menu1.add(technique1_key1, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=technique1_next_menu1)
@dp.callback_query_handler(text="technique1_ready1")
async def technique1_ready1(call: types.CallbackQuery):
    technique1_pict1 = pict.copy()
    technique1_next_menu2 = types.InlineKeyboardMarkup()
    technique1_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='technique1_next1')
    technique1_next_menu2.add(technique1_key2, back)
    x = technique1_pict1[randint(0, len(technique1_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что вы на ней видите? И что \(о чём\) это в вашей жизни? Какая проблема вас беспокоит?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                                           'Как закончите, нажмите кнопку «Дальше»', reply_markup=technique1_next_menu2)
    technique1_pict1.remove(x)
    global technique1_pict2
    technique1_pict2 = technique1_pict1.copy()
@dp.callback_query_handler(text="technique1_next1")
async def technique1_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*А что мне делать с этой проблемой?*")
    technique1_next_menu3 = types.InlineKeyboardMarkup()
    technique1_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique1_ready2')
    technique1_next_menu3.add(technique1_key3, back)
    await call.message.answer('И затем нажмите кнопку «Показать карту»', reply_markup=technique1_next_menu3)

@dp.callback_query_handler(text="technique1_ready2")
async def technique1_ready2(call: types.CallbackQuery):
    technique1_next_menu4 = types.InlineKeyboardMarkup()
    technique1_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='technique1_next2')
    technique1_next_menu4.add(technique1_key4, back)
    x = technique1_pict2[randint(0, len(technique1_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите здесь? И что вам надо сделать в вашей жизни?\n'
                              '\n'
                                'Как будете готовы, нажмите кнопку «Дальше»', reply_markup=technique1_next_menu4)
    technique1_pict2.remove(x)
    global technique1_pict3
    technique1_pict3 = technique1_pict2.copy()
@dp.callback_query_handler(text="technique1_next2")
async def technique1_next2(call: types.CallbackQuery):
    await call.message.answer("Задайте себе следующий вопрос:\n"
                     "\n"
                     "*Какой первый шаг мне нужно сделать?*")
    technique1_next_menu5 = types.InlineKeyboardMarkup()
    technique1_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique1_ready3')
    technique1_next_menu5.add(technique1_key5, back)
    await call.message.answer('И снова нажимаете кнопку «Показать карту»', reply_markup=technique1_next_menu5)
@dp.callback_query_handler(text="technique1_ready3")
async def technique1_ready3(call: types.CallbackQuery):
    technique1_next_menu6 = types.InlineKeyboardMarkup()
    technique1_key6 = types.InlineKeyboardButton(text='Продолжить', callback_data='technique1_Continue')
    technique1_next_menu6.add(technique1_key6, back)
    x = technique1_pict3[randint(0, len(technique1_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=technique1_next_menu6)
    technique1_pict3.remove(x)
    global technique1_pict4
    technique1_pict4 = technique1_pict3.copy()
@dp.callback_query_handler(text="technique1_Continue")
async def technique1_Continue(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который приходит на ум после предыдущих ответов')
    technique1_next_menu7 = types.InlineKeyboardMarkup()
    technique1_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique1_ready4')
    technique1_next_menu7.add(technique1_key7, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=technique1_next_menu7)
@dp.callback_query_handler(text="technique1_ready4")
async def technique1_ready4(call: types.CallbackQuery):
    x = technique1_pict4[randint(0, len(technique1_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _"Что меня беспокоит"_ завершена\.\n'
                              '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())










# 2 обработка техники "Маяк" (после нажатия кнопки выбора техники "Маяк")
@dp.callback_query_handler(text="life_area_technique2")
async def life_area_technique2(call: types.CallbackQuery):
    await call.message.answer('Ок\. Вы выбрали Технику *«Маяк»*\.\n'
                              '\n'
                              'Эта Техника поможет вам, если вы потерялись по жизни\. Не знаете, каких целей достигать, куда идти…\n'
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                              "\n"
                              "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
    await call.message.answer("Теперь задайте себе вопрос:\n"
                     "\n"
                     "*Чего я хочу?*")
    technique2_next_menu1 = types.InlineKeyboardMarkup()
    technique2_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique2_ready1')
    technique2_next_menu1.add(technique2_key1, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=technique2_next_menu1)
@dp.callback_query_handler(text="technique2_ready1")
async def technique2_ready1(call: types.CallbackQuery):
    technique2_pict1 = pict.copy()
    technique2_next_menu2 = types.InlineKeyboardMarkup()
    technique2_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='technique2_next1')
    technique2_next_menu2.add(technique2_key2, back)
    x = technique2_pict1[randint(0, len(technique2_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? Как это связано с вашей жизнью, с вашим вопросом?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=technique2_next_menu2)
    technique2_pict1.remove(x)
    global technique2_pict2
    technique2_pict2 = technique2_pict1.copy()
@dp.callback_query_handler(text="technique2_next1")
async def technique2_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*Что у меня есть сейчас? Какие ресурсы, чтобы это получить?*")
    technique2_next_menu3 = types.InlineKeyboardMarkup()
    technique2_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique2_ready2')
    technique2_next_menu3.add(technique2_key3, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=technique2_next_menu3)
@dp.callback_query_handler(text="technique2_ready2")
async def technique2_ready2(call: types.CallbackQuery):
    technique2_next_menu4 = types.InlineKeyboardMarkup()
    technique2_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='technique2_next2')
    technique2_next_menu4.add(technique2_key4, back)
    x = technique2_pict2[randint(0, len(technique2_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на карте, какие ресурсы у вас есть, чтобы получить желаемое?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=technique2_next_menu4)
    technique2_pict2.remove(x)
    global technique2_pict3
    technique2_pict3 = technique2_pict2.copy()
@dp.callback_query_handler(text="technique2_next2")
async def technique2_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Как мне этого достичь?*")
    technique2_next_menu5 = types.InlineKeyboardMarkup()
    technique2_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique2_ready3')
    technique2_next_menu5.add(technique2_key5, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=technique2_next_menu5)
@dp.callback_query_handler(text="technique2_ready3")
async def technique2_ready3(call: types.CallbackQuery):
    technique2_next_menu6 = types.InlineKeyboardMarkup()
    technique2_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='technique2_next3')
    technique2_next_menu6.add(technique2_key6, back)
    x = technique2_pict3[randint(0, len(technique2_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=technique2_next_menu6)
    technique2_pict3.remove(x)
    global technique2_pict4
    technique2_pict4 = technique2_pict3.copy()
@dp.callback_query_handler(text="technique2_next3")
async def technique2_next3(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос, который вы адресуете своему Бессознательному:\n"
                     "\n"
                     "*Почему это для меня важно?*")
    technique2_next_menu7 = types.InlineKeyboardMarkup()
    technique2_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique2_ready4')
    technique2_next_menu7.add(technique2_key7, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=technique2_next_menu7)
@dp.callback_query_handler(text="technique2_ready4")
async def technique2_ready4(call: types.CallbackQuery):
    technique2_next_menu8 = types.InlineKeyboardMarkup()
    technique2_key8 = types.InlineKeyboardButton(text='Дальше', callback_data='technique2_next4')
    technique2_next_menu8.add(technique2_key8, back)
    x = technique2_pict4[randint(0, len(technique2_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=technique2_next_menu8)
    technique2_pict4.remove(x)
    global technique2_pict5
    technique2_pict5 = technique2_pict4.copy()
@dp.callback_query_handler(text="technique2_next4")
async def technique2_next4(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Как я пойму, что достиг\(ла\) желаемого?*")
    technique2_next_menu9 = types.InlineKeyboardMarkup()
    technique2_key9 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique2_ready5')
    technique2_next_menu9.add(technique2_key9, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=technique2_next_menu9)
@dp.callback_query_handler(text="technique2_ready5")
async def technique2_ready5(call: types.CallbackQuery):
    technique2_next_menu10 = types.InlineKeyboardMarkup()
    technique2_key10 = types.InlineKeyboardButton(text='Дальше', callback_data='technique2_next5')
    technique2_next_menu10.add(technique2_key10, back)
    x = technique2_pict5[randint(0, len(technique2_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Записали ответ? Нажмите кнопку «Дальше»', reply_markup=technique2_next_menu10)
    technique2_pict5.remove(x)
    global technique2_pict6
    technique2_pict6 = technique2_pict5.copy()
@dp.callback_query_handler(text="technique2_next5")
async def technique2_next5(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*А что мне мешает достигнуть желаемого?*")
    technique2_next_menu11 = types.InlineKeyboardMarkup()
    technique2_key11 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique2_ready6')
    technique2_next_menu11.add(technique2_key11, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=technique2_next_menu11)
@dp.callback_query_handler(text="technique2_ready6")
async def technique2_ready6(call: types.CallbackQuery):
    technique2_next_menu12 = types.InlineKeyboardMarkup()
    technique2_key12 = types.InlineKeyboardButton(text='Продолжить', callback_data='technique2_Continue')
    technique2_next_menu12.add(technique2_key12, back)
    x = technique2_pict6[randint(0, len(technique2_pict6) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=technique2_next_menu12)
    technique2_pict6.remove(x)
    global technique2_pict7
    technique2_pict7 = technique2_pict6.copy()
@dp.callback_query_handler(text="technique2_Continue")
async def technique2_Continue(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов')
    technique2_next_menu13 = types.InlineKeyboardMarkup()
    technique2_key13 = types.InlineKeyboardButton(text='Показать карту', callback_data='technique2_ready7')
    technique2_next_menu13.add(technique2_key13, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=technique2_next_menu13)
@dp.callback_query_handler(text="technique2_ready7")
async def technique2_ready7(call: types.CallbackQuery):
    x = technique2_pict7[randint(0, len(technique2_pict7) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Маяк»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())









# 3 обработка техники «Перспективы и планы» (после нажатия кнопки выбора техники «Перспективы и планы»)
@dp.callback_query_handler(text="life_area_technique3")
async def life_area_technique3(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id in db.Set('First'):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                      "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n"
                                      "\n"
                                      "А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer("*Ну, и вот ещё одно крутое предложение*\n"
                                      "\n"
                                      "Я делаю его только новым подписчикам и только один раз\.\n"
                                      "\n"
                                      "Если вы оформите подписку на месяц прямо сейчас, то я подарю вам ещё *плюс месяц бесплатно*\.\n"
                                      "\n"
                                      "А если на год — то плюс *6 месяцев в подарок*\.\n"
                                      "\n"
                                      "Оформить подписку на таких условиях можно только из этого меню\. "
                                      "И как только вы из него уйдёте, воспользоваться предложением больше будет невозможно\.\n"
                                      "\n"
                                      "Таков мой коварный, но выгодный для всех план \)\n")
            await call.message.answer("Вы можете оформить подписку, нажав на соответствующую кнопку ниже", reply_markup=get_first_subscription_menu())

        elif call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                   "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n")
            await call.message.answer("А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer('Вы можете оформить подписку, нажав на соответствующую кнопку ниже', reply_markup=get_subscription_menu())

        else:
            life_area_technique3_next_menu1 = types.InlineKeyboardMarkup()
            life_area_technique3_key1 = types.InlineKeyboardButton(text='Продолжить', callback_data='life_area_technique3_Continue1')
            life_area_technique3_next_menu1.add(life_area_technique3_key1, back)
            await call.message.answer("Ок\. Вы выбрали Технику *«Перспективы и планы»*\.\n"
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                                      "\n"
                                      "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n"
                                "\n"
                                "*И вот что нужно сделать в первую очередь*\n"
                                "\n"
                                "Выпишите три свои цели в таком порядке:\n"
                                "\n"
                                "\- моя ближайшая перспектива;\n"
                                "\- моя отдаленная перспектива;\n"
                                "\- моя дальняя перспектива\.\n"
                                "\n"
                                "То есть вы выписываете то, чего хотите достичь в ближайшее время, затем на средней дистанции, и в дальней перспективе\. "
                                "Это может быть обретение каких\-то материальных ценностей, или какого\-то статуса, или чего хотите\.\n")
            await call.message.answer("Как закончите, нажмите кнопку «Продолжить»", reply_markup=life_area_technique3_next_menu1)
@dp.callback_query_handler(text="life_area_technique3_Continue1")
async def life_area_technique3_Continue1(call: types.CallbackQuery):
    await call.message.answer('Отлично\! Теперь к каждой из ваших целей зададим три вопроса\. Начнём с ближайшей перспективы\.\n'
                              '\n'
                               "Поехали\! Задайте себе первый вопрос:\n"
                               "\n"
                                "*Какое состояние у меня будет, когда я достигну \<подставьте сюда свою ближайшую цель\>?*\n")
    life_area_technique3_next_menu2 = types.InlineKeyboardMarkup()
    life_area_technique3_key2 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique3_ready1')
    life_area_technique3_next_menu2.add(life_area_technique3_key2, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=life_area_technique3_next_menu2)
@dp.callback_query_handler(text="life_area_technique3_ready1")
async def life_area_technique3_ready1(call: types.CallbackQuery):
    life_area_technique3_pict1 = pict.copy()
    life_area_technique3_next_menu3 = types.InlineKeyboardMarkup()
    life_area_technique3_key3 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique3_next1')
    life_area_technique3_next_menu3.add(life_area_technique3_key3, back)
    x = life_area_technique3_pict1[randint(0, len(life_area_technique3_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? Как это связано с вашим вопросом?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=life_area_technique3_next_menu3)
    life_area_technique3_pict1.remove(x)
    global life_area_technique3_pict2
    life_area_technique3_pict2 = life_area_technique3_pict1.copy()
@dp.callback_query_handler(text="life_area_technique3_next1")
async def life_area_technique3_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*А что я буду чувствовать во время реализации \<подставьте сюда свою ближайшую цель\>?*")
    life_area_technique3_next_menu4 = types.InlineKeyboardMarkup()
    life_area_technique3_key4 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique3_ready2')
    life_area_technique3_next_menu4.add(life_area_technique3_key4, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=life_area_technique3_next_menu4)
@dp.callback_query_handler(text="life_area_technique3_ready2")
async def life_area_technique3_ready2(call: types.CallbackQuery):
    life_area_technique3_next_menu5 = types.InlineKeyboardMarkup()
    life_area_technique3_key5 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique3_next2')
    life_area_technique3_next_menu5.add(life_area_technique3_key5, back)
    x = life_area_technique3_pict2[randint(0, len(life_area_technique3_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на этой карте?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=life_area_technique3_next_menu5)
    life_area_technique3_pict2.remove(x)
    global life_area_technique3_pict3
    life_area_technique3_pict3 = life_area_technique3_pict2.copy()
@dp.callback_query_handler(text="life_area_technique3_next2")
async def life_area_technique3_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Как долго продлится моё состояние, когда я достигну \<подставьте сюда свою ближайшую цель\>?*")
    life_area_technique3_next_menu6 = types.InlineKeyboardMarkup()
    life_area_technique3_key6 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique3_ready3')
    life_area_technique3_next_menu6.add(life_area_technique3_key6, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=life_area_technique3_next_menu6)
@dp.callback_query_handler(text="life_area_technique3_ready3")
async def life_area_technique3_ready3(call: types.CallbackQuery):
    life_area_technique3_next_menu7 = types.InlineKeyboardMarkup()
    life_area_technique3_key7 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique3_next3')
    life_area_technique3_next_menu7.add(life_area_technique3_key7, back)
    x = life_area_technique3_pict3[randint(0, len(life_area_technique3_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=life_area_technique3_next_menu7)
    life_area_technique3_pict3.remove(x)
    global life_area_technique3_pict4
    life_area_technique3_pict4 = life_area_technique3_pict3.copy()
@dp.callback_query_handler(text="life_area_technique3_next3")
async def life_area_technique3_next3(call: types.CallbackQuery):
    await call.message.answer("Теперь мы зададим те же вопросы, но про отдаленную перспективу\.\n"
                              "\n"
                              "Следующий вопрос, который вы адресуете своему Бессознательному:\n"
                     "\n"
                     "*Какое состояние у меня будет, когда я достигну \<подставьте сюда свою отдаленную цель\>?*")
    life_area_technique3_next_menu8 = types.InlineKeyboardMarkup()
    life_area_technique3_key8 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique3_ready4')
    life_area_technique3_next_menu8.add(life_area_technique3_key8, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=life_area_technique3_next_menu8)
@dp.callback_query_handler(text="life_area_technique3_ready4")
async def life_area_technique3_ready4(call: types.CallbackQuery):
    life_area_technique3_next_menu9 = types.InlineKeyboardMarkup()
    life_area_technique3_key9 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique3_next4')
    life_area_technique3_next_menu9.add(life_area_technique3_key9, back)
    x = life_area_technique3_pict4[randint(0, len(life_area_technique3_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=life_area_technique3_next_menu9)
    life_area_technique3_pict4.remove(x)
    global life_area_technique3_pict5
    life_area_technique3_pict5 = life_area_technique3_pict4.copy()
@dp.callback_query_handler(text="life_area_technique3_next4")
async def life_area_technique3_next4(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Что я буду чувствовать во время реализации \<подставьте сюда свою отдаленную цель\>?*")
    life_area_technique3_next_menu10 = types.InlineKeyboardMarkup()
    life_area_technique3_key10 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique3_ready5')
    life_area_technique3_next_menu10.add(life_area_technique3_key10, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique3_next_menu10)
@dp.callback_query_handler(text="life_area_technique3_ready5")
async def life_area_technique3_ready5(call: types.CallbackQuery):
    life_area_technique3_next_menu11 = types.InlineKeyboardMarkup()
    life_area_technique3_key11 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique3_next5')
    life_area_technique3_next_menu11.add(life_area_technique3_key11, back)
    x = life_area_technique3_pict5[randint(0, len(life_area_technique3_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Записали ответ? Нажмите кнопку «Дальше»', reply_markup=life_area_technique3_next_menu11)
    life_area_technique3_pict5.remove(x)
    global life_area_technique3_pict6
    life_area_technique3_pict6 = life_area_technique3_pict5.copy()
@dp.callback_query_handler(text="life_area_technique3_next5")
async def life_area_technique3_next5(call: types.CallbackQuery):
    await call.message.answer("И ещё один вопрос:\n"
                     "\n"
                     "*Как долго продлится моё состояние, когда я достигну \<подставьте сюда свою отдаленную цель\>?*")
    life_area_technique3_next_menu12 = types.InlineKeyboardMarkup()
    life_area_technique3_key12 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique3_ready6')
    life_area_technique3_next_menu12.add(life_area_technique3_key12, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique3_next_menu12)
@dp.callback_query_handler(text="life_area_technique3_ready6")
async def life_area_technique3_ready6(call: types.CallbackQuery):
    life_area_technique3_next_menu13 = types.InlineKeyboardMarkup()
    life_area_technique3_key13 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique3_next6')
    life_area_technique3_next_menu13.add(life_area_technique3_key13, back)
    x = life_area_technique3_pict6[randint(0, len(life_area_technique3_pict6) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Нажмите кнопку «Дальше»', reply_markup=life_area_technique3_next_menu13)
    life_area_technique3_pict6.remove(x)
    global life_area_technique3_pict7
    life_area_technique3_pict7 = life_area_technique3_pict6.copy()
@dp.callback_query_handler(text="life_area_technique3_next6")
async def life_area_technique3_next6(call: types.CallbackQuery):
    await call.message.answer("Ну, и осталось задать те же вопросы, но про дальнюю перспективу\.\n"
                              "\n"
                              "Следующий вопрос, который вы себе задаёте:\n"
                     "\n"
                     "*Какое состояние у меня будет, когда я достигну \<подставьте сюда свою дальнюю цель\>?*")
    life_area_technique3_next_menu14 = types.InlineKeyboardMarkup()
    life_area_technique3_key14 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique3_ready7')
    life_area_technique3_next_menu14.add(life_area_technique3_key14, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=life_area_technique3_next_menu14)
@dp.callback_query_handler(text="life_area_technique3_ready7")
async def life_area_technique3_ready7(call: types.CallbackQuery):
    life_area_technique3_next_menu15 = types.InlineKeyboardMarkup()
    life_area_technique3_key15 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique3_next7')
    life_area_technique3_next_menu15.add(life_area_technique3_key15, back)
    x = life_area_technique3_pict7[randint(0, len(life_area_technique3_pict7) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=life_area_technique3_next_menu15)
    life_area_technique3_pict7.remove(x)
    global life_area_technique3_pict8
    life_area_technique3_pict8 = life_area_technique3_pict7.copy()
@dp.callback_query_handler(text="life_area_technique3_next7")
async def life_area_technique3_next7(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Что я буду чувствовать во время реализации \<подставьте сюда свою дальнюю цель\>?*")
    life_area_technique3_next_menu16 = types.InlineKeyboardMarkup()
    life_area_technique3_key16 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique3_ready8')
    life_area_technique3_next_menu16.add(life_area_technique3_key16, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique3_next_menu16)
@dp.callback_query_handler(text="life_area_technique3_ready8")
async def life_area_technique3_ready8(call: types.CallbackQuery):
    life_area_technique3_next_menu17 = types.InlineKeyboardMarkup()
    life_area_technique3_key17 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique3_next8')
    life_area_technique3_next_menu17.add(life_area_technique3_key17, back)
    x = life_area_technique3_pict8[randint(0, len(life_area_technique3_pict8) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Записали ответ? Нажмите кнопку «Дальше»', reply_markup=life_area_technique3_next_menu17)
    life_area_technique3_pict8.remove(x)
    global life_area_technique3_pict9
    life_area_technique3_pict9 = life_area_technique3_pict8.copy()
@dp.callback_query_handler(text="life_area_technique3_next8")
async def life_area_technique3_next8(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*Как долго продлится моё состояние, когда я достигну \<подставьте сюда свою дальнюю цель\>?*")
    life_area_technique3_next_menu18 = types.InlineKeyboardMarkup()
    life_area_technique3_key18 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique3_ready9')
    life_area_technique3_next_menu18.add(life_area_technique3_key18, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique3_next_menu18)

@dp.callback_query_handler(text="life_area_technique3_ready9")
async def life_area_technique3_ready9(call: types.CallbackQuery):
    life_area_technique3_next_menu19 = types.InlineKeyboardMarkup()
    life_area_technique3_key19 = types.InlineKeyboardButton(text='Продолжить', callback_data='life_area_technique3_Continue2')
    life_area_technique3_next_menu19.add(life_area_technique3_key19, back)
    x = life_area_technique3_pict9[randint(0, len(life_area_technique3_pict9) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Техника позволяет понять, действительно ли это ваши цели, которые вы наметили? Не обманываете ли вы сами себя? Может стоит их пересмотреть?\n'
                              '\n'
                              'Если Бессознательное откликается хорошо, положительными эмоциями, то всё отлично — вы на верном пути\!\n'
                              '\n'
                              'Можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=life_area_technique3_next_menu19)
    life_area_technique3_pict9.remove(x)
    global life_area_technique3_pict10
    life_area_technique3_pict10 = life_area_technique3_pict9.copy()
@dp.callback_query_handler(text="life_area_technique3_Continue2")
async def life_area_technique3_Continue2(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов')
    life_area_technique3_next_menu20 = types.InlineKeyboardMarkup()
    life_area_technique3_key20 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique3_ready10')
    life_area_technique3_next_menu20.add(life_area_technique3_key20, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=life_area_technique3_next_menu20)
@dp.callback_query_handler(text="life_area_technique3_ready10")
async def life_area_technique3_ready10(call: types.CallbackQuery):
    x = life_area_technique3_pict10[randint(0, len(life_area_technique3_pict10) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Перспективы и планы»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())











# 4 обработка техники «Познать себя» (после нажатия кнопки выбора техники «Познать себя»)
@dp.callback_query_handler(text="life_area_technique4")
async def life_area_technique4(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id in db.Set('First'):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                      "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n"
                                      "\n"
                                      "А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer("*Ну, и вот ещё одно крутое предложение*\n"
                                      "\n"
                                      "Я делаю его только новым подписчикам и только один раз\.\n"
                                      "\n"
                                      "Если вы оформите подписку на месяц прямо сейчас, то я подарю вам ещё *плюс месяц бесплатно*\.\n"
                                      "\n"
                                      "А если на год — то плюс *6 месяцев в подарок*\.\n"
                                      "\n"
                                      "Оформить подписку на таких условиях можно только из этого меню\. "
                                      "И как только вы из него уйдёте, воспользоваться предложением больше будет невозможно\.\n"
                                      "\n"
                                      "Таков мой коварный, но выгодный для всех план \)\n")
            await call.message.answer("Вы можете оформить подписку, нажав на соответствующую кнопку ниже", reply_markup=get_first_subscription_menu())

        elif call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                   "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n")
            await call.message.answer("А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer('Вы можете оформить подписку, нажав на соответствующую кнопку ниже', reply_markup=get_subscription_menu())
        else:
            life_area_technique4_next_menu1 = types.InlineKeyboardMarkup()
            life_area_technique4_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready1')
            life_area_technique4_next_menu1.add(life_area_technique4_key1, back)
            await call.message.answer("Ок\. Вы выбрали Технику *«Познать себя»*\.\n"
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                                      "\n"
                                      "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
            await call.message.answer("Задайте себе первый вопрос:\n"
                                      "\n"
                                      "*Как я вижу себя \(в жизни\)?*")
            await call.message.answer("Как будете готовы, нажмите кнопку «Показать карту»", reply_markup=life_area_technique4_next_menu1)

@dp.callback_query_handler(text="life_area_technique4_ready1")
async def life_area_technique4_ready1(call: types.CallbackQuery):
    life_area_technique4_pict1 = pict.copy()
    life_area_technique4_next_menu2 = types.InlineKeyboardMarkup()
    life_area_technique4_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next1')
    life_area_technique4_next_menu2.add(life_area_technique4_key2, back)
    x = life_area_technique4_pict1[randint(0, len(life_area_technique4_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? Как это связано с вами?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu2)
    life_area_technique4_pict1.remove(x)
    global life_area_technique4_pict2
    life_area_technique4_pict2 = life_area_technique4_pict1.copy()
@dp.callback_query_handler(text="life_area_technique4_next1")
async def life_area_technique4_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*Как меня видят другие?*")
    life_area_technique4_next_menu3 = types.InlineKeyboardMarkup()
    life_area_technique4_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready2')
    life_area_technique4_next_menu3.add(life_area_technique4_key3, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu3)
@dp.callback_query_handler(text="life_area_technique4_ready2")
async def life_area_technique4_ready2(call: types.CallbackQuery):
    life_area_technique4_next_menu4 = types.InlineKeyboardMarkup()
    life_area_technique4_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next2')
    life_area_technique4_next_menu4.add(life_area_technique4_key4, back)
    x = life_area_technique4_pict2[randint(0, len(life_area_technique4_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на этой карте?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu4)
    life_area_technique4_pict2.remove(x)
    global life_area_technique4_pict3
    life_area_technique4_pict3 = life_area_technique4_pict2.copy()
@dp.callback_query_handler(text="life_area_technique4_next2")
async def life_area_technique4_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Как я отношусь к себе?*")
    life_area_technique4_next_menu5 = types.InlineKeyboardMarkup()
    life_area_technique4_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready3')
    life_area_technique4_next_menu5.add(life_area_technique4_key5, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu5)
@dp.callback_query_handler(text="life_area_technique4_ready3")
async def life_area_technique4_ready3(call: types.CallbackQuery):
    life_area_technique4_next_menu6 = types.InlineKeyboardMarkup()
    life_area_technique4_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next3')
    life_area_technique4_next_menu6.add(life_area_technique4_key6, back)
    x = life_area_technique4_pict3[randint(0, len(life_area_technique4_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu6)
    life_area_technique4_pict3.remove(x)
    global life_area_technique4_pict4
    life_area_technique4_pict4 = life_area_technique4_pict3.copy()
@dp.callback_query_handler(text="life_area_technique4_next3")
async def life_area_technique4_next3(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос, который вы адресуете своему Бессознательному:\n"
                     "\n"
                     "*Как другие относятся ко мне?*")
    life_area_technique4_next_menu7 = types.InlineKeyboardMarkup()
    life_area_technique4_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready4')
    life_area_technique4_next_menu7.add(life_area_technique4_key7, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu7)
@dp.callback_query_handler(text="life_area_technique4_ready4")
async def life_area_technique4_ready4(call: types.CallbackQuery):
    life_area_technique4_next_menu8 = types.InlineKeyboardMarkup()
    life_area_technique4_key8 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next4')
    life_area_technique4_next_menu8.add(life_area_technique4_key8, back)
    x = life_area_technique4_pict4[randint(0, len(life_area_technique4_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu8)
    life_area_technique4_pict4.remove(x)
    global life_area_technique4_pict5
    life_area_technique4_pict5 = life_area_technique4_pict4.copy()
@dp.callback_query_handler(text="life_area_technique4_next4")
async def life_area_technique4_next4(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Что мне в себе нравится?*")
    life_area_technique4_next_menu9 = types.InlineKeyboardMarkup()
    life_area_technique4_key9 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready5')
    life_area_technique4_next_menu9.add(life_area_technique4_key9, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu9)
@dp.callback_query_handler(text="life_area_technique4_ready5")
async def life_area_technique4_ready5(call: types.CallbackQuery):
    life_area_technique4_next_menu10 = types.InlineKeyboardMarkup()
    life_area_technique4_key10 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next5')
    life_area_technique4_next_menu10.add(life_area_technique4_key10, back)
    x = life_area_technique4_pict5[randint(0, len(life_area_technique4_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Записали ответ? Нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu10)
    life_area_technique4_pict5.remove(x)
    global life_area_technique4_pict6
    life_area_technique4_pict6 = life_area_technique4_pict5.copy()
@dp.callback_query_handler(text="life_area_technique4_next5")
async def life_area_technique4_next5(call: types.CallbackQuery):
    await call.message.answer("Продолжаем\. Следующий вопрос:\n"
                     "\n"
                     "*Что другим нравится во мне?*")
    life_area_technique4_next_menu11 = types.InlineKeyboardMarkup()
    life_area_technique4_key11 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready6')
    life_area_technique4_next_menu11.add(life_area_technique4_key11, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu11)
@dp.callback_query_handler(text="life_area_technique4_ready6")
async def life_area_technique4_ready6(call: types.CallbackQuery):
    life_area_technique4_next_menu12 = types.InlineKeyboardMarkup()
    life_area_technique4_key12 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next6')
    life_area_technique4_next_menu12.add(life_area_technique4_key12, back)
    x = life_area_technique4_pict6[randint(0, len(life_area_technique4_pict6) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu12)
    life_area_technique4_pict6.remove(x)
    global life_area_technique4_pict7
    life_area_technique4_pict7 = life_area_technique4_pict6.copy()
@dp.callback_query_handler(text="life_area_technique4_next6")
async def life_area_technique4_next6(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос, который вы себе задаёте:\n"
                     "\n"
                     "*Что мне в себе не нравится?*")
    life_area_technique4_next_menu13 = types.InlineKeyboardMarkup()
    life_area_technique4_key13 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready7')
    life_area_technique4_next_menu13.add(life_area_technique4_key13, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu13)
@dp.callback_query_handler(text="life_area_technique4_ready7")
async def life_area_technique4_ready7(call: types.CallbackQuery):
    life_area_technique4_next_menu14 = types.InlineKeyboardMarkup()
    life_area_technique4_key14 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next7')
    life_area_technique4_next_menu14.add(life_area_technique4_key14, back)
    x = life_area_technique4_pict7[randint(0, len(life_area_technique4_pict7) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu14)
    life_area_technique4_pict7.remove(x)
    global life_area_technique4_pict8
    life_area_technique4_pict8 = life_area_technique4_pict7.copy()
@dp.callback_query_handler(text="life_area_technique4_next7")
async def life_area_technique4_next7(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Что во мне не нравится другим?*")
    life_area_technique4_next_menu15 = types.InlineKeyboardMarkup()
    life_area_technique4_key15 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready8')
    life_area_technique4_next_menu15.add(life_area_technique4_key15, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu15)
@dp.callback_query_handler(text="life_area_technique4_ready8")
async def life_area_technique4_ready8(call: types.CallbackQuery):
    life_area_technique4_next_menu16 = types.InlineKeyboardMarkup()
    life_area_technique4_key16 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next8')
    life_area_technique4_next_menu16.add(life_area_technique4_key16, back)
    x = life_area_technique4_pict8[randint(0, len(life_area_technique4_pict8) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Записали ответ? Нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu16)
    life_area_technique4_pict8.remove(x)
    global life_area_technique4_pict9
    life_area_technique4_pict9 = life_area_technique4_pict8.copy()
@dp.callback_query_handler(text="life_area_technique4_next8")
async def life_area_technique4_next8(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Что я хотел\(а\) бы изменить в себе?*")
    life_area_technique4_next_menu17 = types.InlineKeyboardMarkup()
    life_area_technique4_key17 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready9')
    life_area_technique4_next_menu17.add(life_area_technique4_key17, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu17)

@dp.callback_query_handler(text="life_area_technique4_ready9")
async def life_area_technique4_ready9(call: types.CallbackQuery):
    life_area_technique4_next_menu18 = types.InlineKeyboardMarkup()
    life_area_technique4_key18 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next9')
    life_area_technique4_next_menu18.add(life_area_technique4_key18, back)
    x = life_area_technique4_pict9[randint(0, len(life_area_technique4_pict9) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu18)
    life_area_technique4_pict9.remove(x)
    global life_area_technique4_pict10
    life_area_technique4_pict10 = life_area_technique4_pict9.copy()
@dp.callback_query_handler(text="life_area_technique4_next9")
async def life_area_technique4_next9(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*А что мне действительно нужно изменить в себе?*")
    life_area_technique4_next_menu19 = types.InlineKeyboardMarkup()
    life_area_technique4_key19 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready10')
    life_area_technique4_next_menu19.add(life_area_technique4_key19, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu19)

@dp.callback_query_handler(text="life_area_technique4_ready10")
async def life_area_technique4_ready10(call: types.CallbackQuery):
    life_area_technique4_next_menu20 = types.InlineKeyboardMarkup()
    life_area_technique4_key20 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next10')
    life_area_technique4_next_menu20.add(life_area_technique4_key20, back)
    x = life_area_technique4_pict10[randint(0, len(life_area_technique4_pict10) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы, нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu20)
    life_area_technique4_pict10.remove(x)
    global life_area_technique4_pict11
    life_area_technique4_pict11 = life_area_technique4_pict10.copy()
@dp.callback_query_handler(text="life_area_technique4_next10")
async def life_area_technique4_next10(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Каким\(ой\) я стану, если изменюсь, как хочу я?*")
    life_area_technique4_next_menu21 = types.InlineKeyboardMarkup()
    life_area_technique4_key21 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready11')
    life_area_technique4_next_menu21.add(life_area_technique4_key21, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu21)

@dp.callback_query_handler(text="life_area_technique4_ready11")
async def life_area_technique4_ready11(call: types.CallbackQuery):
    life_area_technique4_next_menu22 = types.InlineKeyboardMarkup()
    life_area_technique4_key22 = types.InlineKeyboardButton(text='Дальше', callback_data='life_area_technique4_next11')
    life_area_technique4_next_menu22.add(life_area_technique4_key22, back)
    x = life_area_technique4_pict11[randint(0, len(life_area_technique4_pict11) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=life_area_technique4_next_menu22)
    life_area_technique4_pict11.remove(x)
    global life_area_technique4_pict12
    life_area_technique4_pict12 = life_area_technique4_pict11.copy()
@dp.callback_query_handler(text="life_area_technique4_next11")
async def life_area_technique4_next11(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*Какой\(им\) я стану, если изменюсь так, как нужно измениться?*")
    life_area_technique4_next_menu23 = types.InlineKeyboardMarkup()
    life_area_technique4_key23 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready12')
    life_area_technique4_next_menu23.add(life_area_technique4_key23, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu23)

@dp.callback_query_handler(text="life_area_technique4_ready12")
async def life_area_technique4_ready12(call: types.CallbackQuery):
    life_area_technique4_next_menu24 = types.InlineKeyboardMarkup()
    life_area_technique4_key24 = types.InlineKeyboardButton(text='Продолжить', callback_data='life_area_technique4_Continue1')
    life_area_technique4_next_menu24.add(life_area_technique4_key24, back)
    x = life_area_technique4_pict12[randint(0, len(life_area_technique4_pict12) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Интересно, как много нового вы о себе узнали? \)\n'
                              '\n'
                              'Теперь можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=life_area_technique4_next_menu24)
    life_area_technique4_pict12.remove(x)
    global life_area_technique4_pict13
    life_area_technique4_pict13 = life_area_technique4_pict12.copy()
@dp.callback_query_handler(text="life_area_technique4_Continue1")
async def life_area_technique4_Continue1(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов')
    life_area_technique4_next_menu25 = types.InlineKeyboardMarkup()
    life_area_technique4_key25 = types.InlineKeyboardButton(text='Показать карту', callback_data='life_area_technique4_ready13')
    life_area_technique4_next_menu25.add(life_area_technique4_key25, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=life_area_technique4_next_menu25)
@dp.callback_query_handler(text="life_area_technique4_ready13")
async def life_area_technique4_ready13(call: types.CallbackQuery):
    x = life_area_technique4_pict13[randint(0, len(life_area_technique4_pict13) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Познать себя»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())









# Сфера "Отношения"
# 1 обработка техники «Моя половинка» (после нажатия кнопки выбора техники «Моя половинка»)
@dp.callback_query_handler(text="relations_area_technique1")
async def relations_area_technique1(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id in db.Set('First'):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                      "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n"
                                      "\n"
                                      "А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer("*Ну, и вот ещё одно крутое предложение*\n"
                                      "\n"
                                      "Я делаю его только новым подписчикам и только один раз\.\n"
                                      "\n"
                                      "Если вы оформите подписку на месяц прямо сейчас, то я подарю вам ещё *плюс месяц бесплатно*\.\n"
                                      "\n"
                                      "А если на год — то плюс *6 месяцев в подарок*\.\n"
                                      "\n"
                                      "Оформить подписку на таких условиях можно только из этого меню\. "
                                      "И как только вы из него уйдёте, воспользоваться предложением больше будет невозможно\.\n"
                                      "\n"
                                      "Таков мой коварный, но выгодный для всех план \)\n")
            await call.message.answer("Вы можете оформить подписку, нажав на соответствующую кнопку ниже", reply_markup=get_first_subscription_menu())

        elif call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                   "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n")
            await call.message.answer("А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer('Вы можете оформить подписку, нажав на соответствующую кнопку ниже', reply_markup=get_subscription_menu())
        else:
            relations_area_technique1_next_menu1 = types.InlineKeyboardMarkup()
            relations_area_technique1_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique1_ready1')
            relations_area_technique1_next_menu1.add(relations_area_technique1_key1, back)
            await call.message.answer("Ок\. Вы выбрали Технику *«Моя половинка»*\.\n"
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                                      "\n"
                                      "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
            await call.message.answer("Задайте себе первый вопрос:\n"
                                      "\n"
                                      "*Что мою половинку радует в наших отношениях?*")
            await call.message.answer("Как будете готовы, нажмите кнопку «Показать карту»", reply_markup=relations_area_technique1_next_menu1)

@dp.callback_query_handler(text="relations_area_technique1_ready1")
async def relations_area_technique1_ready1(call: types.CallbackQuery):
    relations_area_technique1_pict1 = pict.copy()
    relations_area_technique1_next_menu2 = types.InlineKeyboardMarkup()
    relations_area_technique1_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='relations_area_technique1_next1')
    relations_area_technique1_next_menu2.add(relations_area_technique1_key2, back)
    x = relations_area_technique1_pict1[randint(0, len(relations_area_technique1_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? Как это связано с вашим вопросом?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=relations_area_technique1_next_menu2)
    relations_area_technique1_pict1.remove(x)
    global relations_area_technique1_pict2
    relations_area_technique1_pict2 = relations_area_technique1_pict1.copy()
@dp.callback_query_handler(text="relations_area_technique1_next1")
async def relations_area_technique1_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*Что мою половинку печалит в наших отношениях?*")
    relations_area_technique1_next_menu3 = types.InlineKeyboardMarkup()
    relations_area_technique1_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique1_ready2')
    relations_area_technique1_next_menu3.add(relations_area_technique1_key3, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=relations_area_technique1_next_menu3)
@dp.callback_query_handler(text="relations_area_technique1_ready2")
async def relations_area_technique1_ready2(call: types.CallbackQuery):
    relations_area_technique1_next_menu4 = types.InlineKeyboardMarkup()
    relations_area_technique1_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='relations_area_technique1_next2')
    relations_area_technique1_next_menu4.add(relations_area_technique1_key4, back)
    x = relations_area_technique1_pict2[randint(0, len(relations_area_technique1_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на этой карте?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=relations_area_technique1_next_menu4)
    relations_area_technique1_pict2.remove(x)
    global relations_area_technique1_pict3
    relations_area_technique1_pict3 = relations_area_technique1_pict2.copy()
@dp.callback_query_handler(text="relations_area_technique1_next2")
async def relations_area_technique1_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Что моя половинка хочет от этих отношений?*")
    relations_area_technique1_next_menu5 = types.InlineKeyboardMarkup()
    relations_area_technique1_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique1_ready3')
    relations_area_technique1_next_menu5.add(relations_area_technique1_key5, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=relations_area_technique1_next_menu5)
@dp.callback_query_handler(text="relations_area_technique1_ready3")
async def relations_area_technique1_ready3(call: types.CallbackQuery):
    relations_area_technique1_next_menu6 = types.InlineKeyboardMarkup()
    relations_area_technique1_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='relations_area_technique1_next3')
    relations_area_technique1_next_menu6.add(relations_area_technique1_key6, back)
    x = relations_area_technique1_pict3[randint(0, len(relations_area_technique1_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=relations_area_technique1_next_menu6)
    relations_area_technique1_pict3.remove(x)
    global relations_area_technique1_pict4
    relations_area_technique1_pict4 = relations_area_technique1_pict3.copy()
@dp.callback_query_handler(text="relations_area_technique1_next3")
async def relations_area_technique1_next3(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*Чем наши отношения продолжатся/закончатся \(выберите сами\)?*")
    relations_area_technique1_next_menu7 = types.InlineKeyboardMarkup()
    relations_area_technique1_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique1_ready4')
    relations_area_technique1_next_menu7.add(relations_area_technique1_key7, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=relations_area_technique1_next_menu7)

@dp.callback_query_handler(text="relations_area_technique1_ready4")
async def relations_area_technique1_ready4(call: types.CallbackQuery):
    relations_area_technique1_next_menu8 = types.InlineKeyboardMarkup()
    relations_area_technique1_key8 = types.InlineKeyboardButton(text='Продолжить', callback_data='relations_area_technique1_Continue1')
    relations_area_technique1_next_menu8.add(relations_area_technique1_key8, back)
    x = relations_area_technique1_pict4[randint(0, len(relations_area_technique1_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Теперь можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=relations_area_technique1_next_menu8)
    relations_area_technique1_pict4.remove(x)
    global relations_area_technique1_pict5
    relations_area_technique1_pict5 = relations_area_technique1_pict4.copy()
@dp.callback_query_handler(text="relations_area_technique1_Continue1")
async def relations_area_technique1_Continue1(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов\.\n'
                              '\n'
                              'Или можно, например, задать вопрос: *Что с этим теперь делать прямо сейчас?*')
    relations_area_technique1_next_menu9 = types.InlineKeyboardMarkup()
    relations_area_technique1_key9 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique1_ready5')
    relations_area_technique1_next_menu9.add(relations_area_technique1_key9, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=relations_area_technique1_next_menu9)
@dp.callback_query_handler(text="relations_area_technique1_ready5")
async def relations_area_technique1_ready5(call: types.CallbackQuery):
    x = relations_area_technique1_pict5[randint(0, len(relations_area_technique1_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Моя половинка»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())










# 2 обработка техники «Я в отношениях» (после нажатия кнопки выбора техники «Я в отношениях»)
@dp.callback_query_handler(text="relations_area_technique2")
async def relations_area_technique2(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id in db.Set('First'):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                      "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n"
                                      "\n"
                                      "А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer("*Ну, и вот ещё одно крутое предложение*\n"
                                      "\n"
                                      "Я делаю его только новым подписчикам и только один раз\.\n"
                                      "\n"
                                      "Если вы оформите подписку на месяц прямо сейчас, то я подарю вам ещё *плюс месяц бесплатно*\.\n"
                                      "\n"
                                      "А если на год — то плюс *6 месяцев в подарок*\.\n"
                                      "\n"
                                      "Оформить подписку на таких условиях можно только из этого меню\. "
                                      "И как только вы из него уйдёте, воспользоваться предложением больше будет невозможно\.\n"
                                      "\n"
                                      "Таков мой коварный, но выгодный для всех план \)\n")
            await call.message.answer("Вы можете оформить подписку, нажав на соответствующую кнопку ниже", reply_markup=get_first_subscription_menu())

        elif call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                   "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n")
            await call.message.answer("А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer('Вы можете оформить подписку, нажав на соответствующую кнопку ниже', reply_markup=get_subscription_menu())
        else:
            relations_area_technique2_next_menu1 = types.InlineKeyboardMarkup()
            relations_area_technique2_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique2_ready1')
            relations_area_technique2_next_menu1.add(relations_area_technique2_key1, back)
            await call.message.answer("Ок\. Вы выбрали Технику *«Я в отношениях»*\.\n"
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                                      "\n"
                                      "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
            await call.message.answer("Задайте себе первый вопрос:\n"
                                      "\n"
                                      "*Как я себя чувствую в этих отношениях?*")
            await call.message.answer("Как будете готовы, нажмите кнопку «Показать карту»", reply_markup=relations_area_technique2_next_menu1)

@dp.callback_query_handler(text="relations_area_technique2_ready1")
async def relations_area_technique2_ready1(call: types.CallbackQuery):
    relations_area_technique2_pict1 = pict.copy()
    relations_area_technique2_next_menu2 = types.InlineKeyboardMarkup()
    relations_area_technique2_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='relations_area_technique2_next1')
    relations_area_technique2_next_menu2.add(relations_area_technique2_key2, back)
    x = relations_area_technique2_pict1[randint(0, len(relations_area_technique2_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? Как это связано с вашим вопросом?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=relations_area_technique2_next_menu2)
    relations_area_technique2_pict1.remove(x)
    global relations_area_technique2_pict2
    relations_area_technique2_pict2 = relations_area_technique2_pict1.copy()
@dp.callback_query_handler(text="relations_area_technique2_next1")
async def relations_area_technique2_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*Где бы я хотел\(а\) оказаться с партнершей \(партнером\)?*")
    relations_area_technique2_next_menu3 = types.InlineKeyboardMarkup()
    relations_area_technique2_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique2_ready2')
    relations_area_technique2_next_menu3.add(relations_area_technique2_key3, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=relations_area_technique2_next_menu3)
@dp.callback_query_handler(text="relations_area_technique2_ready2")
async def relations_area_technique2_ready2(call: types.CallbackQuery):
    relations_area_technique2_next_menu4 = types.InlineKeyboardMarkup()
    relations_area_technique2_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='relations_area_technique2_next2')
    relations_area_technique2_next_menu4.add(relations_area_technique2_key4, back)
    x = relations_area_technique2_pict2[randint(0, len(relations_area_technique2_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на этой карте?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=relations_area_technique2_next_menu4)
    relations_area_technique2_pict2.remove(x)
    global relations_area_technique2_pict3
    relations_area_technique2_pict3 = relations_area_technique2_pict2.copy()
@dp.callback_query_handler(text="relations_area_technique2_next2")
async def relations_area_technique2_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Какую сказку я бы хотел\(а\) написать партнерше или партнеру?*\n"
                              "\n"
                              "\(метафорически что\-то ему сообщить, как послание\)")
    relations_area_technique2_next_menu5 = types.InlineKeyboardMarkup()
    relations_area_technique2_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique2_ready3')
    relations_area_technique2_next_menu5.add(relations_area_technique2_key5, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=relations_area_technique2_next_menu5)
@dp.callback_query_handler(text="relations_area_technique2_ready3")
async def relations_area_technique2_ready3(call: types.CallbackQuery):
    relations_area_technique2_next_menu6 = types.InlineKeyboardMarkup()
    relations_area_technique2_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='relations_area_technique2_next3')
    relations_area_technique2_next_menu6.add(relations_area_technique2_key6, back)
    x = relations_area_technique2_pict3[randint(0, len(relations_area_technique2_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=relations_area_technique2_next_menu6)
    relations_area_technique2_pict3.remove(x)
    global relations_area_technique2_pict4
    relations_area_technique2_pict4 = relations_area_technique2_pict3.copy()
@dp.callback_query_handler(text="relations_area_technique2_next3")
async def relations_area_technique2_next3(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос, который вы задаёте себе:\n"
                     "\n"
                     "*Что меня больше всего напрягает в наших отношениях?*")
    relations_area_technique2_next_menu7 = types.InlineKeyboardMarkup()
    relations_area_technique2_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique2_ready4')
    relations_area_technique2_next_menu7.add(relations_area_technique2_key7, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=relations_area_technique2_next_menu7)
@dp.callback_query_handler(text="relations_area_technique2_ready4")
async def relations_area_technique2_ready4(call: types.CallbackQuery):
    relations_area_technique2_next_menu8 = types.InlineKeyboardMarkup()
    relations_area_technique2_key8 = types.InlineKeyboardButton(text='Дальше', callback_data='relations_area_technique2_next4')
    relations_area_technique2_next_menu8.add(relations_area_technique2_key8, back)
    x = relations_area_technique2_pict4[randint(0, len(relations_area_technique2_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=relations_area_technique2_next_menu8)
    relations_area_technique2_pict4.remove(x)
    global relations_area_technique2_pict5
    relations_area_technique2_pict5 = relations_area_technique2_pict4.copy()
@dp.callback_query_handler(text="relations_area_technique2_next4")
async def relations_area_technique2_next4(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Чего я хочу от отношений на самом деле?*")
    relations_area_technique2_next_menu9 = types.InlineKeyboardMarkup()
    relations_area_technique2_key9 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique2_ready5')
    relations_area_technique2_next_menu9.add(relations_area_technique2_key9, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=relations_area_technique2_next_menu9)

@dp.callback_query_handler(text="relations_area_technique2_ready5")
async def relations_area_technique2_ready5(call: types.CallbackQuery):
    relations_area_technique2_next_menu10 = types.InlineKeyboardMarkup()
    relations_area_technique2_key10 = types.InlineKeyboardButton(text='Дальше', callback_data='relations_area_technique2_next5')
    relations_area_technique2_next_menu10.add(relations_area_technique2_key10, back)
    x = relations_area_technique2_pict5[randint(0, len(relations_area_technique2_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы, нажмите кнопку «Дальше»', reply_markup=relations_area_technique2_next_menu10)
    relations_area_technique2_pict5.remove(x)
    global relations_area_technique2_pict6
    relations_area_technique2_pict6 = relations_area_technique2_pict5.copy()
@dp.callback_query_handler(text="relations_area_technique2_next5")
async def relations_area_technique2_next5(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Какая для меня ресурсная стихия в этих отношениях?*")
    relations_area_technique2_next_menu11 = types.InlineKeyboardMarkup()
    relations_area_technique2_key11 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique2_ready6')
    relations_area_technique2_next_menu11.add(relations_area_technique2_key11, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=relations_area_technique2_next_menu11)

@dp.callback_query_handler(text="relations_area_technique2_ready6")
async def relations_area_technique2_ready6(call: types.CallbackQuery):
    relations_area_technique2_next_menu12 = types.InlineKeyboardMarkup()
    relations_area_technique2_key12 = types.InlineKeyboardButton(text='Дальше', callback_data='relations_area_technique2_next6')
    relations_area_technique2_next_menu12.add(relations_area_technique2_key12, back)
    x = relations_area_technique2_pict6[randint(0, len(relations_area_technique2_pict6) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=relations_area_technique2_next_menu12)
    relations_area_technique2_pict6.remove(x)
    global relations_area_technique2_pict7
    relations_area_technique2_pict7 = relations_area_technique2_pict6.copy()
@dp.callback_query_handler(text="relations_area_technique2_next6")
async def relations_area_technique2_next6(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*С повадками какого животного я ассоциирую партнера\(шу\)?*")
    relations_area_technique2_next_menu13 = types.InlineKeyboardMarkup()
    relations_area_technique2_key13 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique2_ready7')
    relations_area_technique2_next_menu13.add(relations_area_technique2_key13, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=relations_area_technique2_next_menu13)

@dp.callback_query_handler(text="relations_area_technique2_ready7")
async def relations_area_technique2_ready7(call: types.CallbackQuery):
    relations_area_technique2_next_menu14 = types.InlineKeyboardMarkup()
    relations_area_technique2_key14 = types.InlineKeyboardButton(text='Продолжить', callback_data='relations_area_technique2_Continue1')
    relations_area_technique2_next_menu14.add(relations_area_technique2_key14, back)
    x = relations_area_technique2_pict7[randint(0, len(relations_area_technique2_pict7) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Теперь можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=relations_area_technique2_next_menu14)
    relations_area_technique2_pict7.remove(x)
    global relations_area_technique2_pict8
    relations_area_technique2_pict8 = relations_area_technique2_pict7.copy()
@dp.callback_query_handler(text="relations_area_technique2_Continue1")
async def relations_area_technique2_Continue1(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов\.\n'
                              '\n'
                              'Или можно, например, задать вопрос: *Что с этим теперь делать прямо сейчас? Какой первый шаг?*')
    relations_area_technique2_next_menu15 = types.InlineKeyboardMarkup()
    relations_area_technique2_key15 = types.InlineKeyboardButton(text='Показать карту', callback_data='relations_area_technique2_ready8')
    relations_area_technique2_next_menu15.add(relations_area_technique2_key15, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=relations_area_technique2_next_menu15)
@dp.callback_query_handler(text="relations_area_technique2_ready8")
async def relations_area_technique2_ready8(call: types.CallbackQuery):
    x = relations_area_technique2_pict8[randint(0, len(relations_area_technique2_pict8) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Я в отношениях»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())









# Сфера "Здоровье"
# 1 обработка техники «Моя любимая болячка» (после нажатия кнопки выбора техники «Моя любимая болячка»)
@dp.callback_query_handler(text="health_area_technique1")
async def health_area_technique1(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id in db.Set('First'):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                      "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n"
                                      "\n"
                                      "А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer("*Ну, и вот ещё одно крутое предложение*\n"
                                      "\n"
                                      "Я делаю его только новым подписчикам и только один раз\.\n"
                                      "\n"
                                      "Если вы оформите подписку на месяц прямо сейчас, то я подарю вам ещё *плюс месяц бесплатно*\.\n"
                                      "\n"
                                      "А если на год — то плюс *6 месяцев в подарок*\.\n"
                                      "\n"
                                      "Оформить подписку на таких условиях можно только из этого меню\. "
                                      "И как только вы из него уйдёте, воспользоваться предложением больше будет невозможно\.\n"
                                      "\n"
                                      "Таков мой коварный, но выгодный для всех план \)\n")
            await call.message.answer("Вы можете оформить подписку, нажав на соответствующую кнопку ниже", reply_markup=get_first_subscription_menu())

        elif call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                   "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n")
            await call.message.answer("А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer('Вы можете оформить подписку, нажав на соответствующую кнопку ниже', reply_markup=get_subscription_menu())
        else:
            health_area_technique1_next_menu1 = types.InlineKeyboardMarkup()
            health_area_technique1_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique1_ready1')
            health_area_technique1_next_menu1.add(health_area_technique1_key1, back)
            await call.message.answer("Ок\. Вы выбрали Технику *«Моя любимая болячка»*\.\n"
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                                      "\n"
                                      "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
            await call.message.answer("Задайте себе первый вопрос:\n"
                                      "\n"
                                      "*Моя любимая болячка?*"
                                      "\n"
                                      "\(в чем она состоит\)")
            await call.message.answer("Как будете готовы, нажмите кнопку «Показать карту»", reply_markup=health_area_technique1_next_menu1)

@dp.callback_query_handler(text="health_area_technique1_ready1")
async def health_area_technique1_ready1(call: types.CallbackQuery):
    health_area_technique1_pict1 = pict.copy()
    health_area_technique1_next_menu2 = types.InlineKeyboardMarkup()
    health_area_technique1_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique1_next1')
    health_area_technique1_next_menu2.add(health_area_technique1_key2, back)
    x = health_area_technique1_pict1[randint(0, len(health_area_technique1_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? Что за болячка вас беспокоит?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=health_area_technique1_next_menu2)
    health_area_technique1_pict1.remove(x)
    global health_area_technique1_pict2
    health_area_technique1_pict2 = health_area_technique1_pict1.copy()
@dp.callback_query_handler(text="health_area_technique1_next1")
async def health_area_technique1_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*Для чего она пришла \(приходит\)?*")
    health_area_technique1_next_menu3 = types.InlineKeyboardMarkup()
    health_area_technique1_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique1_ready2')
    health_area_technique1_next_menu3.add(health_area_technique1_key3, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=health_area_technique1_next_menu3)
@dp.callback_query_handler(text="health_area_technique1_ready2")
async def health_area_technique1_ready2(call: types.CallbackQuery):
    health_area_technique1_next_menu4 = types.InlineKeyboardMarkup()
    health_area_technique1_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique1_next2')
    health_area_technique1_next_menu4.add(health_area_technique1_key4, back)
    x = health_area_technique1_pict2[randint(0, len(health_area_technique1_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на этой карте?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=health_area_technique1_next_menu4)
    health_area_technique1_pict2.remove(x)
    global health_area_technique1_pict3
    health_area_technique1_pict3 = health_area_technique1_pict2.copy()
@dp.callback_query_handler(text="health_area_technique1_next2")
async def health_area_technique1_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Что я делаю по поводу моей болячки?*")
    health_area_technique1_next_menu5 = types.InlineKeyboardMarkup()
    health_area_technique1_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique1_ready3')
    health_area_technique1_next_menu5.add(health_area_technique1_key5, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=health_area_technique1_next_menu5)
@dp.callback_query_handler(text="health_area_technique1_ready3")
async def health_area_technique1_ready3(call: types.CallbackQuery):
    health_area_technique1_next_menu6 = types.InlineKeyboardMarkup()
    health_area_technique1_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique1_next3')
    health_area_technique1_next_menu6.add(health_area_technique1_key6, back)
    x = health_area_technique1_pict3[randint(0, len(health_area_technique1_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=health_area_technique1_next_menu6)
    health_area_technique1_pict3.remove(x)
    global health_area_technique1_pict4
    health_area_technique1_pict4 = health_area_technique1_pict3.copy()

@dp.callback_query_handler(text="health_area_technique1_next3")
async def health_area_technique1_next3(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*В чем польза моей болячки?*")
    health_area_technique1_next_menu7 = types.InlineKeyboardMarkup()
    health_area_technique1_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique1_ready4')
    health_area_technique1_next_menu7.add(health_area_technique1_key7, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=health_area_technique1_next_menu7)

@dp.callback_query_handler(text="health_area_technique1_ready4")
async def health_area_technique1_ready4(call: types.CallbackQuery):
    health_area_technique1_next_menu8 = types.InlineKeyboardMarkup()
    health_area_technique1_key8 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique1_next4')
    health_area_technique1_next_menu8.add(health_area_technique1_key8, back)
    x = health_area_technique1_pict4[randint(0, len(health_area_technique1_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=health_area_technique1_next_menu8)
    health_area_technique1_pict4.remove(x)
    global health_area_technique1_pict5
    health_area_technique1_pict5 = health_area_technique1_pict4.copy()

@dp.callback_query_handler(text="health_area_technique1_next4")
async def health_area_technique1_next4(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*А что нужно сделать, чтобы болячка прошла, а польза этой болячки осталась?*")
    health_area_technique1_next_menu9 = types.InlineKeyboardMarkup()
    health_area_technique1_key9 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique1_ready5')
    health_area_technique1_next_menu9.add(health_area_technique1_key9, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=health_area_technique1_next_menu9)

@dp.callback_query_handler(text="health_area_technique1_ready5")
async def health_area_technique1_ready5(call: types.CallbackQuery):
    health_area_technique1_next_menu10 = types.InlineKeyboardMarkup()
    health_area_technique1_key10 = types.InlineKeyboardButton(text='Продолжить', callback_data='health_area_technique1_Continue1')
    health_area_technique1_next_menu10.add(health_area_technique1_key10, back)
    x = health_area_technique1_pict5[randint(0, len(health_area_technique1_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Теперь можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=health_area_technique1_next_menu10)
    health_area_technique1_pict5.remove(x)
    global health_area_technique1_pict6
    health_area_technique1_pict6 = health_area_technique1_pict5.copy()
@dp.callback_query_handler(text="health_area_technique1_Continue1")
async def health_area_technique1_Continue1(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов\.\n'
                              '\n'
                              'Или можно, например, задать вопрос: *Что с этим теперь делать прямо сейчас?*')
    health_area_technique1_next_menu11 = types.InlineKeyboardMarkup()
    health_area_technique1_key11 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique1_ready6')
    health_area_technique1_next_menu11.add(health_area_technique1_key11, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=health_area_technique1_next_menu11)
@dp.callback_query_handler(text="health_area_technique1_ready6")
async def health_area_technique1_ready6(call: types.CallbackQuery):
    x = health_area_technique1_pict6[randint(0, len(health_area_technique1_pict6) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Моя любимая болячка»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())








# 2 обработка техники «Моё здоровье» (после нажатия кнопки выбора техники «Моё здоровье»)
@dp.callback_query_handler(text="health_area_technique2")
async def health_area_technique2(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id in db.Set('First'):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                      "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n"
                                      "\n"
                                      "А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer("*Ну, и вот ещё одно крутое предложение*\n"
                                      "\n"
                                      "Я делаю его только новым подписчикам и только один раз\.\n"
                                      "\n"
                                      "Если вы оформите подписку на месяц прямо сейчас, то я подарю вам ещё *плюс месяц бесплатно*\.\n"
                                      "\n"
                                      "А если на год — то плюс *6 месяцев в подарок*\.\n"
                                      "\n"
                                      "Оформить подписку на таких условиях можно только из этого меню\. "
                                      "И как только вы из него уйдёте, воспользоваться предложением больше будет невозможно\.\n"
                                      "\n"
                                      "Таков мой коварный, но выгодный для всех план \)\n")
            await call.message.answer("Вы можете оформить подписку, нажав на соответствующую кнопку ниже", reply_markup=get_first_subscription_menu())

        elif call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                   "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n")
            await call.message.answer("А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer('Вы можете оформить подписку, нажав на соответствующую кнопку ниже', reply_markup=get_subscription_menu())
        else:
            health_area_technique2_next_menu1 = types.InlineKeyboardMarkup()
            health_area_technique2_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique2_ready1')
            health_area_technique2_next_menu1.add(health_area_technique2_key1, back)
            await call.message.answer("Ок\. Вы выбрали Технику *«Моё здоровье»*\.\n"
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                                      "\n"
                                      "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
            await call.message.answer("Задайте себе первый вопрос:\n"
                                      "\n"
                                      "*Как я отношусь к своему здоровью?*")
            await call.message.answer("Как будете готовы, нажмите кнопку «Показать карту»", reply_markup=health_area_technique2_next_menu1)

@dp.callback_query_handler(text="health_area_technique2_ready1")
async def health_area_technique2_ready1(call: types.CallbackQuery):
    health_area_technique2_pict1 = pict.copy()
    health_area_technique2_next_menu2 = types.InlineKeyboardMarkup()
    health_area_technique2_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique2_next1')
    health_area_technique2_next_menu2.add(health_area_technique2_key2, back)
    x = health_area_technique2_pict1[randint(0, len(health_area_technique2_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? О чём это в вашей жизни? Как это связано с вашим вопросом?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=health_area_technique2_next_menu2)
    health_area_technique2_pict1.remove(x)
    global health_area_technique2_pict2
    health_area_technique2_pict2 = health_area_technique2_pict1.copy()
@dp.callback_query_handler(text="health_area_technique2_next1")
async def health_area_technique2_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*Как моё здоровье относится ко мне?*")
    health_area_technique2_next_menu3 = types.InlineKeyboardMarkup()
    health_area_technique2_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique2_ready2')
    health_area_technique2_next_menu3.add(health_area_technique2_key3, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=health_area_technique2_next_menu3)
@dp.callback_query_handler(text="health_area_technique2_ready2")
async def health_area_technique2_ready2(call: types.CallbackQuery):
    health_area_technique2_next_menu4 = types.InlineKeyboardMarkup()
    health_area_technique2_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique2_next2')
    health_area_technique2_next_menu4.add(health_area_technique2_key4, back)
    x = health_area_technique2_pict2[randint(0, len(health_area_technique2_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на этой карте?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=health_area_technique2_next_menu4)
    health_area_technique2_pict2.remove(x)
    global health_area_technique2_pict3
    health_area_technique2_pict3 = health_area_technique2_pict2.copy()
@dp.callback_query_handler(text="health_area_technique2_next2")
async def health_area_technique2_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Что я хочу сделать для своего здоровья?*")
    health_area_technique2_next_menu5 = types.InlineKeyboardMarkup()
    health_area_technique2_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique2_ready3')
    health_area_technique2_next_menu5.add(health_area_technique2_key5, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=health_area_technique2_next_menu5)
@dp.callback_query_handler(text="health_area_technique2_ready3")
async def health_area_technique2_ready3(call: types.CallbackQuery):
    health_area_technique2_next_menu6 = types.InlineKeyboardMarkup()
    health_area_technique2_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique2_next3')
    health_area_technique2_next_menu6.add(health_area_technique2_key6, back)
    x = health_area_technique2_pict3[randint(0, len(health_area_technique2_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=health_area_technique2_next_menu6)
    health_area_technique2_pict3.remove(x)
    global health_area_technique2_pict4
    health_area_technique2_pict4 = health_area_technique2_pict3.copy()

@dp.callback_query_handler(text="health_area_technique2_next3")
async def health_area_technique2_next3(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*А что мне нужно сделать для своего здоровья на самом деле?*")
    health_area_technique2_next_menu7 = types.InlineKeyboardMarkup()
    health_area_technique2_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique2_ready4')
    health_area_technique2_next_menu7.add(health_area_technique2_key7, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=health_area_technique2_next_menu7)

@dp.callback_query_handler(text="health_area_technique2_ready4")
async def health_area_technique2_ready4(call: types.CallbackQuery):
    health_area_technique2_next_menu8 = types.InlineKeyboardMarkup()
    health_area_technique2_key8 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique2_next4')
    health_area_technique2_next_menu8.add(health_area_technique2_key8, back)
    x = health_area_technique2_pict4[randint(0, len(health_area_technique2_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=health_area_technique2_next_menu8)
    health_area_technique2_pict4.remove(x)
    global health_area_technique2_pict5
    health_area_technique2_pict5 = health_area_technique2_pict4.copy()

@dp.callback_query_handler(text="health_area_technique2_next4")
async def health_area_technique2_next4(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Как я буду чувствовать себя, когда сделаю то, что хочу, для своего здоровья?*")
    health_area_technique2_next_menu9 = types.InlineKeyboardMarkup()
    health_area_technique2_key9 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique2_ready5')
    health_area_technique2_next_menu9.add(health_area_technique2_key9, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=health_area_technique2_next_menu9)

@dp.callback_query_handler(text="health_area_technique2_ready5")
async def health_area_technique2_ready5(call: types.CallbackQuery):
    health_area_technique2_next_menu10 = types.InlineKeyboardMarkup()
    health_area_technique2_key10 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique2_next5')
    health_area_technique2_next_menu10.add(health_area_technique2_key10, back)
    x = health_area_technique2_pict5[randint(0, len(health_area_technique2_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=health_area_technique2_next_menu10)
    health_area_technique2_pict5.remove(x)
    global health_area_technique2_pict6
    health_area_technique2_pict6 = health_area_technique2_pict5.copy()

@dp.callback_query_handler(text="health_area_technique2_next5")
async def health_area_technique2_next5(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*Как я буду чувствовать себя, когда сделаю то, что на самом деле надо, для моего здоровья?*")
    health_area_technique2_next_menu11 = types.InlineKeyboardMarkup()
    health_area_technique2_key11 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique2_ready6')
    health_area_technique2_next_menu11.add(health_area_technique2_key11, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=health_area_technique2_next_menu11)

@dp.callback_query_handler(text="health_area_technique2_ready6")
async def health_area_technique2_ready6(call: types.CallbackQuery):
    health_area_technique2_next_menu12 = types.InlineKeyboardMarkup()
    health_area_technique2_key12 = types.InlineKeyboardButton(text='Продолжить', callback_data='health_area_technique2_Continue1')
    health_area_technique2_next_menu12.add(health_area_technique2_key12, back)
    x = health_area_technique2_pict6[randint(0, len(health_area_technique2_pict6) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Теперь можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=health_area_technique2_next_menu12)
    health_area_technique2_pict6.remove(x)
    global health_area_technique2_pict7
    health_area_technique2_pict7 = health_area_technique2_pict6.copy()
@dp.callback_query_handler(text="health_area_technique2_Continue1")
async def health_area_technique2_Continue1(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов\.\n'
                              '\n'
                              'Или можно, например, задать вопрос: *Что с этим теперь делать прямо сейчас? Какой первый шаг мне нужно сделать?*')
    health_area_technique2_next_menu13 = types.InlineKeyboardMarkup()
    health_area_technique2_key13 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique2_ready7')
    health_area_technique2_next_menu13.add(health_area_technique2_key13, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=health_area_technique2_next_menu13)
@dp.callback_query_handler(text="health_area_technique2_ready7")
async def health_area_technique2_ready7(call: types.CallbackQuery):
    x = health_area_technique2_pict7[randint(0, len(health_area_technique2_pict7) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Моё здоровье»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())










# 1 обработка техники «Уроки моего тела» (после нажатия кнопки выбора техники «Уроки моего тела»)
@dp.callback_query_handler(text="health_area_technique3")
async def health_area_technique3(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id in db.Set('First'):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                      "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n"
                                      "\n"
                                      "А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer("*Ну, и вот ещё одно крутое предложение*\n"
                                      "\n"
                                      "Я делаю его только новым подписчикам и только один раз\.\n"
                                      "\n"
                                      "Если вы оформите подписку на месяц прямо сейчас, то я подарю вам ещё *плюс месяц бесплатно*\.\n"
                                      "\n"
                                      "А если на год — то плюс *6 месяцев в подарок*\.\n"
                                      "\n"
                                      "Оформить подписку на таких условиях можно только из этого меню\. "
                                      "И как только вы из него уйдёте, воспользоваться предложением больше будет невозможно\.\n"
                                      "\n"
                                      "Таков мой коварный, но выгодный для всех план \)\n")
            await call.message.answer("Вы можете оформить подписку, нажав на соответствующую кнопку ниже", reply_markup=get_first_subscription_menu())

        elif call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                   "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n")
            await call.message.answer("А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer('Вы можете оформить подписку, нажав на соответствующую кнопку ниже', reply_markup=get_subscription_menu())
        else:
            health_area_technique3_next_menu1 = types.InlineKeyboardMarkup()
            health_area_technique3_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique3_ready1')
            health_area_technique3_next_menu1.add(health_area_technique3_key1, back)
            await call.message.answer("Ок\. Вы выбрали Технику *«Уроки моего тела»*\.\n"
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                                      "\n"
                                      "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
            await call.message.answer("Задайте себе первый вопрос:\n"
                                      "\n"
                                      "*Какой жизненный урок преподносит мне моё тело?*")
            await call.message.answer("Как будете готовы, нажмите кнопку «Показать карту»", reply_markup=health_area_technique3_next_menu1)

@dp.callback_query_handler(text="health_area_technique3_ready1")
async def health_area_technique3_ready1(call: types.CallbackQuery):
    health_area_technique3_pict1 = pict.copy()
    health_area_technique3_next_menu2 = types.InlineKeyboardMarkup()
    health_area_technique3_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique3_next1')
    health_area_technique3_next_menu2.add(health_area_technique3_key2, back)
    x = health_area_technique3_pict1[randint(0, len(health_area_technique3_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? Как это связано с вашим вопросом?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=health_area_technique3_next_menu2)
    health_area_technique3_pict1.remove(x)
    global health_area_technique3_pict2
    health_area_technique3_pict2 = health_area_technique3_pict1.copy()
@dp.callback_query_handler(text="health_area_technique3_next1")
async def health_area_technique3_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*Как я реагирую на этот жизненный урок?*")
    health_area_technique3_next_menu3 = types.InlineKeyboardMarkup()
    health_area_technique3_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique3_ready2')
    health_area_technique3_next_menu3.add(health_area_technique3_key3, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=health_area_technique3_next_menu3)
@dp.callback_query_handler(text="health_area_technique3_ready2")
async def health_area_technique3_ready2(call: types.CallbackQuery):
    health_area_technique3_next_menu4 = types.InlineKeyboardMarkup()
    health_area_technique3_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique3_next2')
    health_area_technique3_next_menu4.add(health_area_technique3_key4, back)
    x = health_area_technique3_pict2[randint(0, len(health_area_technique3_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на этой карте?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=health_area_technique3_next_menu4)
    health_area_technique3_pict2.remove(x)
    global health_area_technique3_pict3
    health_area_technique3_pict3 = health_area_technique3_pict2.copy()
@dp.callback_query_handler(text="health_area_technique3_next2")
async def health_area_technique3_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Как мне отнестись к этому уроку правильно?*")
    health_area_technique3_next_menu5 = types.InlineKeyboardMarkup()
    health_area_technique3_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique3_ready3')
    health_area_technique3_next_menu5.add(health_area_technique3_key5, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=health_area_technique3_next_menu5)
@dp.callback_query_handler(text="health_area_technique3_ready3")
async def health_area_technique3_ready3(call: types.CallbackQuery):
    health_area_technique3_next_menu6 = types.InlineKeyboardMarkup()
    health_area_technique3_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique3_next3')
    health_area_technique3_next_menu6.add(health_area_technique3_key6, back)
    x = health_area_technique3_pict3[randint(0, len(health_area_technique3_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=health_area_technique3_next_menu6)
    health_area_technique3_pict3.remove(x)
    global health_area_technique3_pict4
    health_area_technique3_pict4 = health_area_technique3_pict3.copy()

@dp.callback_query_handler(text="health_area_technique3_next3")
async def health_area_technique3_next3(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Какое открытие ждет меня, если я отнесусь к уроку правильно?*")
    health_area_technique3_next_menu7 = types.InlineKeyboardMarkup()
    health_area_technique3_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique3_ready4')
    health_area_technique3_next_menu7.add(health_area_technique3_key7, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=health_area_technique3_next_menu7)

@dp.callback_query_handler(text="health_area_technique3_ready4")
async def health_area_technique3_ready4(call: types.CallbackQuery):
    health_area_technique3_next_menu8 = types.InlineKeyboardMarkup()
    health_area_technique3_key8 = types.InlineKeyboardButton(text='Дальше', callback_data='health_area_technique3_next4')
    health_area_technique3_next_menu8.add(health_area_technique3_key8, back)
    x = health_area_technique3_pict4[randint(0, len(health_area_technique3_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=health_area_technique3_next_menu8)
    health_area_technique3_pict4.remove(x)
    global health_area_technique3_pict5
    health_area_technique3_pict5 = health_area_technique3_pict4.copy()

@dp.callback_query_handler(text="health_area_technique3_next4")
async def health_area_technique3_next4(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*Как мне отблагодарить моё тело \(за урок\)?*")
    health_area_technique3_next_menu9 = types.InlineKeyboardMarkup()
    health_area_technique3_key9 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique3_ready5')
    health_area_technique3_next_menu9.add(health_area_technique3_key9, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=health_area_technique3_next_menu9)

@dp.callback_query_handler(text="health_area_technique3_ready5")
async def health_area_technique3_ready5(call: types.CallbackQuery):
    health_area_technique3_next_menu10 = types.InlineKeyboardMarkup()
    health_area_technique3_key10 = types.InlineKeyboardButton(text='Продолжить', callback_data='health_area_technique3_Continue1')
    health_area_technique3_next_menu10.add(health_area_technique3_key10, back)
    x = health_area_technique3_pict5[randint(0, len(health_area_technique3_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Теперь можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=health_area_technique3_next_menu10)
    health_area_technique3_pict5.remove(x)
    global health_area_technique3_pict6
    health_area_technique3_pict6 = health_area_technique3_pict5.copy()
@dp.callback_query_handler(text="health_area_technique3_Continue1")
async def health_area_technique3_Continue1(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов\.\n'
                              '\n'
                              'Или можно, например, задать вопрос: *Что с этим теперь делать прямо сейчас? Какой первый шаг мне нужно сделать?*')
    health_area_technique3_next_menu11 = types.InlineKeyboardMarkup()
    health_area_technique3_key11 = types.InlineKeyboardButton(text='Показать карту', callback_data='health_area_technique3_ready6')
    health_area_technique3_next_menu11.add(health_area_technique3_key11, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=health_area_technique3_next_menu11)
@dp.callback_query_handler(text="health_area_technique3_ready6")
async def health_area_technique3_ready6(call: types.CallbackQuery):
    x = health_area_technique3_pict6[randint(0, len(health_area_technique3_pict6) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Уроки моего тела»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())








# Сфера "Деньги"
# 1 обработка техники «Деньги в моей жизни» (после нажатия кнопки выбора техники «Деньги в моей жизни»)
@dp.callback_query_handler(text="money_area_technique1")
async def money_area_technique1(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id in db.Set('First'):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                      "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n"
                                      "\n"
                                      "А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer("*Ну, и вот ещё одно крутое предложение*\n"
                                      "\n"
                                      "Я делаю его только новым подписчикам и только один раз\.\n"
                                      "\n"
                                      "Если вы оформите подписку на месяц прямо сейчас, то я подарю вам ещё *плюс месяц бесплатно*\.\n"
                                      "\n"
                                      "А если на год — то плюс *6 месяцев в подарок*\.\n"
                                      "\n"
                                      "Оформить подписку на таких условиях можно только из этого меню\. "
                                      "И как только вы из него уйдёте, воспользоваться предложением больше будет невозможно\.\n"
                                      "\n"
                                      "Таков мой коварный, но выгодный для всех план \)\n")
            await call.message.answer("Вы можете оформить подписку, нажав на соответствующую кнопку ниже", reply_markup=get_first_subscription_menu())

        elif call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                   "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n")
            await call.message.answer("А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer('Вы можете оформить подписку, нажав на соответствующую кнопку ниже', reply_markup=get_subscription_menu())
        else:
            money_area_technique1_next_menu1 = types.InlineKeyboardMarkup()
            money_area_technique1_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique1_ready1')
            money_area_technique1_next_menu1.add(money_area_technique1_key1, back)
            await call.message.answer("Ок\. Вы выбрали Технику *«Деньги в моей жизни»*\.\n"
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                                      "\n"
                                      "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
            await call.message.answer("Задайте себе первый вопрос:\n"
                                      "\n"
                                      "*Как я отношусь к деньгам?*")
            await call.message.answer("Как будете готовы, нажмите кнопку «Показать карту»", reply_markup=money_area_technique1_next_menu1)

@dp.callback_query_handler(text="money_area_technique1_ready1")
async def money_area_technique1_ready1(call: types.CallbackQuery):
    money_area_technique1_pict1 = pict_money.copy()
    money_area_technique1_next_menu2 = types.InlineKeyboardMarkup()
    money_area_technique1_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='money_area_technique1_next1')
    money_area_technique1_next_menu2.add(money_area_technique1_key2, back)
    x = money_area_technique1_pict1[randint(0, len(money_area_technique1_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? Как это связано с вашим вопросом?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=money_area_technique1_next_menu2)
    money_area_technique1_pict1.remove(x)
    global money_area_technique1_pict2
    money_area_technique1_pict2 = money_area_technique1_pict1.copy()
@dp.callback_query_handler(text="money_area_technique1_next1")
async def money_area_technique1_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*Как деньги относятся ко мне?*")
    money_area_technique1_next_menu3 = types.InlineKeyboardMarkup()
    money_area_technique1_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique1_ready2')
    money_area_technique1_next_menu3.add(money_area_technique1_key3, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=money_area_technique1_next_menu3)
@dp.callback_query_handler(text="money_area_technique1_ready2")
async def money_area_technique1_ready2(call: types.CallbackQuery):
    money_area_technique1_next_menu4 = types.InlineKeyboardMarkup()
    money_area_technique1_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='money_area_technique1_next2')
    money_area_technique1_next_menu4.add(money_area_technique1_key4, back)
    x = money_area_technique1_pict2[randint(0, len(money_area_technique1_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на этой карте?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=money_area_technique1_next_menu4)
    money_area_technique1_pict2.remove(x)
    global money_area_technique1_pict3
    money_area_technique1_pict3 = money_area_technique1_pict2.copy()
@dp.callback_query_handler(text="money_area_technique1_next2")
async def money_area_technique1_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Что хорошего дают мне деньги?*")
    money_area_technique1_next_menu5 = types.InlineKeyboardMarkup()
    money_area_technique1_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique1_ready3')
    money_area_technique1_next_menu5.add(money_area_technique1_key5, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=money_area_technique1_next_menu5)
@dp.callback_query_handler(text="money_area_technique1_ready3")
async def money_area_technique1_ready3(call: types.CallbackQuery):
    money_area_technique1_next_menu6 = types.InlineKeyboardMarkup()
    money_area_technique1_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='money_area_technique1_next3')
    money_area_technique1_next_menu6.add(money_area_technique1_key6, back)
    x = money_area_technique1_pict3[randint(0, len(money_area_technique1_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=money_area_technique1_next_menu6)
    money_area_technique1_pict3.remove(x)
    global money_area_technique1_pict4
    money_area_technique1_pict4 = money_area_technique1_pict3.copy()
@dp.callback_query_handler(text="money_area_technique1_next3")
async def money_area_technique1_next3(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос, который вы задаёте себе:\n"
                     "\n"
                     "*Что плохого дают мне деньги?*")
    money_area_technique1_next_menu7 = types.InlineKeyboardMarkup()
    money_area_technique1_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique1_ready4')
    money_area_technique1_next_menu7.add(money_area_technique1_key7, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=money_area_technique1_next_menu7)
@dp.callback_query_handler(text="money_area_technique1_ready4")
async def money_area_technique1_ready4(call: types.CallbackQuery):
    money_area_technique1_next_menu8 = types.InlineKeyboardMarkup()
    money_area_technique1_key8 = types.InlineKeyboardButton(text='Дальше', callback_data='money_area_technique1_next4')
    money_area_technique1_next_menu8.add(money_area_technique1_key8, back)
    x = money_area_technique1_pict4[randint(0, len(money_area_technique1_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=money_area_technique1_next_menu8)
    money_area_technique1_pict4.remove(x)
    global money_area_technique1_pict5
    money_area_technique1_pict5 = money_area_technique1_pict4.copy()
@dp.callback_query_handler(text="money_area_technique1_next4")
async def money_area_technique1_next4(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Какие эмоции я буду испытывать, когда у меня будет много денег?*")
    money_area_technique1_next_menu9 = types.InlineKeyboardMarkup()
    money_area_technique1_key9 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique1_ready5')
    money_area_technique1_next_menu9.add(money_area_technique1_key9, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=money_area_technique1_next_menu9)

@dp.callback_query_handler(text="money_area_technique1_ready5")
async def money_area_technique1_ready5(call: types.CallbackQuery):
    money_area_technique1_next_menu10 = types.InlineKeyboardMarkup()
    money_area_technique1_key10 = types.InlineKeyboardButton(text='Дальше', callback_data='money_area_technique1_next5')
    money_area_technique1_next_menu10.add(money_area_technique1_key10, back)
    x = money_area_technique1_pict5[randint(0, len(money_area_technique1_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы, нажмите кнопку «Дальше»', reply_markup=money_area_technique1_next_menu10)
    money_area_technique1_pict5.remove(x)
    global money_area_technique1_pict6
    money_area_technique1_pict6 = money_area_technique1_pict5.copy()
@dp.callback_query_handler(text="money_area_technique1_next5")
async def money_area_technique1_next5(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Какие эмоции я буду испытывать, когда у меня будет мало денег?*")
    money_area_technique1_next_menu11 = types.InlineKeyboardMarkup()
    money_area_technique1_key11 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique1_ready6')
    money_area_technique1_next_menu11.add(money_area_technique1_key11, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=money_area_technique1_next_menu11)

@dp.callback_query_handler(text="money_area_technique1_ready6")
async def money_area_technique1_ready6(call: types.CallbackQuery):
    money_area_technique1_next_menu12 = types.InlineKeyboardMarkup()
    money_area_technique1_key12 = types.InlineKeyboardButton(text='Дальше', callback_data='money_area_technique1_next6')
    money_area_technique1_next_menu12.add(money_area_technique1_key12, back)
    x = money_area_technique1_pict6[randint(0, len(money_area_technique1_pict6) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=money_area_technique1_next_menu12)
    money_area_technique1_pict6.remove(x)
    global money_area_technique1_pict7
    money_area_technique1_pict7 = money_area_technique1_pict6.copy()
@dp.callback_query_handler(text="money_area_technique1_next6")
async def money_area_technique1_next6(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*Какие эмоции я буду испытывать, если у меня останется столько денег, сколько есть сейчас?*")
    money_area_technique1_next_menu13 = types.InlineKeyboardMarkup()
    money_area_technique1_key13 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique1_ready7')
    money_area_technique1_next_menu13.add(money_area_technique1_key13, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=money_area_technique1_next_menu13)

@dp.callback_query_handler(text="money_area_technique1_ready7")
async def money_area_technique1_ready7(call: types.CallbackQuery):
    money_area_technique1_next_menu14 = types.InlineKeyboardMarkup()
    money_area_technique1_key14 = types.InlineKeyboardButton(text='Продолжить', callback_data='money_area_technique1_Continue1')
    money_area_technique1_next_menu14.add(money_area_technique1_key14, back)
    x = money_area_technique1_pict7[randint(0, len(money_area_technique1_pict7) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Теперь можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=money_area_technique1_next_menu14)
    money_area_technique1_pict7.remove(x)
    global money_area_technique1_pict8
    money_area_technique1_pict8 = money_area_technique1_pict7.copy()
@dp.callback_query_handler(text="money_area_technique1_Continue1")
async def money_area_technique1_Continue1(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов\.\n'
                              '\n'
                              'Или можно, например, задать вопрос: *Что с этим теперь делать прямо сейчас? Какой первый шаг?*')
    money_area_technique1_next_menu15 = types.InlineKeyboardMarkup()
    money_area_technique1_key15 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique1_ready8')
    money_area_technique1_next_menu15.add(money_area_technique1_key15, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=money_area_technique1_next_menu15)
@dp.callback_query_handler(text="money_area_technique1_ready8")
async def money_area_technique1_ready8(call: types.CallbackQuery):
    x = money_area_technique1_pict8[randint(0, len(money_area_technique1_pict8) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Деньги в моей жизни»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())









# 2 обработка техники «Моя денежная цель» (после нажатия кнопки выбора техники «Моя денежная цель»)
@dp.callback_query_handler(text="money_area_technique2")
async def money_area_technique2(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id in db.Set('First'):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                      "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n"
                                      "\n"
                                      "А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer("*Ну, и вот ещё одно крутое предложение*\n"
                                      "\n"
                                      "Я делаю его только новым подписчикам и только один раз\.\n"
                                      "\n"
                                      "Если вы оформите подписку на месяц прямо сейчас, то я подарю вам ещё *плюс месяц бесплатно*\.\n"
                                      "\n"
                                      "А если на год — то плюс *6 месяцев в подарок*\.\n"
                                      "\n"
                                      "Оформить подписку на таких условиях можно только из этого меню\. "
                                      "И как только вы из него уйдёте, воспользоваться предложением больше будет невозможно\.\n"
                                      "\n"
                                      "Таков мой коварный, но выгодный для всех план \)\n")
            await call.message.answer("Вы можете оформить подписку, нажав на соответствующую кнопку ниже", reply_markup=get_first_subscription_menu())

        elif call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                   "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n")
            await call.message.answer("А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer('Вы можете оформить подписку, нажав на соответствующую кнопку ниже', reply_markup=get_subscription_menu())
        else:
            money_area_technique2_next_menu1 = types.InlineKeyboardMarkup()
            money_area_technique2_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique2_ready1')
            money_area_technique2_next_menu1.add(money_area_technique2_key1, back)
            await call.message.answer("Ок\. Вы выбрали Технику *«Моя денежная цель»*\.\n"
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                                      "\n"
                                      "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
            await call.message.answer("Задайте себе первый вопрос:\n"
                                      "\n"
                                      "*Какой доход я хочу получать в месяц?*")
            await call.message.answer("Как будете готовы, нажмите кнопку «Показать карту»", reply_markup=money_area_technique2_next_menu1)

@dp.callback_query_handler(text="money_area_technique2_ready1")
async def money_area_technique2_ready1(call: types.CallbackQuery):
    money_area_technique2_pict1 = pict_money.copy()
    money_area_technique2_next_menu2 = types.InlineKeyboardMarkup()
    money_area_technique2_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='money_area_technique2_next1')
    money_area_technique2_next_menu2.add(money_area_technique2_key2, back)
    x = money_area_technique2_pict1[randint(0, len(money_area_technique2_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? Как это связано с вашим вопросом?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=money_area_technique2_next_menu2)
    money_area_technique2_pict1.remove(x)
    global money_area_technique2_pict2
    money_area_technique2_pict2 = money_area_technique2_pict1.copy()
@dp.callback_query_handler(text="money_area_technique2_next1")
async def money_area_technique2_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*Какая главная причина, которая мешает мне получать столько денег?*")
    money_area_technique2_next_menu3 = types.InlineKeyboardMarkup()
    money_area_technique2_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique2_ready2')
    money_area_technique2_next_menu3.add(money_area_technique2_key3, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=money_area_technique2_next_menu3)
@dp.callback_query_handler(text="money_area_technique2_ready2")
async def money_area_technique2_ready2(call: types.CallbackQuery):
    money_area_technique2_next_menu4 = types.InlineKeyboardMarkup()
    money_area_technique2_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='money_area_technique2_next2')
    money_area_technique2_next_menu4.add(money_area_technique2_key4, back)
    x = money_area_technique2_pict2[randint(0, len(money_area_technique2_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на этой карте?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=money_area_technique2_next_menu4)
    money_area_technique2_pict2.remove(x)
    global money_area_technique2_pict3
    money_area_technique2_pict3 = money_area_technique2_pict2.copy()
@dp.callback_query_handler(text="money_area_technique2_next2")
async def money_area_technique2_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Как изменюсь я и моя жизнь, когда у меня уже будет этот доход?*")
    money_area_technique2_next_menu5 = types.InlineKeyboardMarkup()
    money_area_technique2_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique2_ready3')
    money_area_technique2_next_menu5.add(money_area_technique2_key5, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=money_area_technique2_next_menu5)
@dp.callback_query_handler(text="money_area_technique2_ready3")
async def money_area_technique2_ready3(call: types.CallbackQuery):
    money_area_technique2_next_menu6 = types.InlineKeyboardMarkup()
    money_area_technique2_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='money_area_technique2_next3')
    money_area_technique2_next_menu6.add(money_area_technique2_key6, back)
    x = money_area_technique2_pict3[randint(0, len(money_area_technique2_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=money_area_technique2_next_menu6)
    money_area_technique2_pict3.remove(x)
    global money_area_technique2_pict4
    money_area_technique2_pict4 = money_area_technique2_pict3.copy()
@dp.callback_query_handler(text="money_area_technique2_next3")
async def money_area_technique2_next3(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*Какие действия помогут мне прийти к этому доходу?*")
    money_area_technique2_next_menu7 = types.InlineKeyboardMarkup()
    money_area_technique2_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique2_ready4')
    money_area_technique2_next_menu7.add(money_area_technique2_key7, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=money_area_technique2_next_menu7)

@dp.callback_query_handler(text="money_area_technique2_ready4")
async def money_area_technique2_ready4(call: types.CallbackQuery):
    money_area_technique2_next_menu8 = types.InlineKeyboardMarkup()
    money_area_technique2_key8 = types.InlineKeyboardButton(text='Продолжить', callback_data='money_area_technique2_Continue1')
    money_area_technique2_next_menu8.add(money_area_technique2_key8, back)
    x = money_area_technique2_pict4[randint(0, len(money_area_technique2_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Теперь можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=money_area_technique2_next_menu8)
    money_area_technique2_pict4.remove(x)
    global money_area_technique2_pict5
    money_area_technique2_pict5 = money_area_technique2_pict4.copy()
@dp.callback_query_handler(text="money_area_technique2_Continue1")
async def money_area_technique2_Continue1(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов\.\n'
                              '\n'
                              'Или можно, например, задать вопрос: *Что с этим теперь делать прямо сейчас? Какой первый шаг мне сделать?*')
    money_area_technique2_next_menu9 = types.InlineKeyboardMarkup()
    money_area_technique2_key9 = types.InlineKeyboardButton(text='Показать карту', callback_data='money_area_technique2_ready5')
    money_area_technique2_next_menu9.add(money_area_technique2_key9, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=money_area_technique2_next_menu9)
@dp.callback_query_handler(text="money_area_technique2_ready5")
async def money_area_technique2_ready5(call: types.CallbackQuery):
    x = money_area_technique2_pict5[randint(0, len(money_area_technique2_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Моя денежная цель»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())










# Сфера "Семья"
# 1 обработка техники «Я в семье» (после нажатия кнопки выбора техники «Я в семье»)
@dp.callback_query_handler(text="family_area_technique1")
async def family_area_technique1(call: types.CallbackQuery):
    with Vedis(config.db_file) as db:
        if call.message.chat.id in db.Set('First'):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                      "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n"
                                      "\n"
                                      "А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer("*Ну, и вот ещё одно крутое предложение*\n"
                                      "\n"
                                      "Я делаю его только новым подписчикам и только один раз\.\n"
                                      "\n"
                                      "Если вы оформите подписку на месяц прямо сейчас, то я подарю вам ещё *плюс месяц бесплатно*\.\n"
                                      "\n"
                                      "А если на год — то плюс *6 месяцев в подарок*\.\n"
                                      "\n"
                                      "Оформить подписку на таких условиях можно только из этого меню\. "
                                      "И как только вы из него уйдёте, воспользоваться предложением больше будет невозможно\.\n"
                                      "\n"
                                      "Таков мой коварный, но выгодный для всех план \)\n")
            await call.message.answer("Вы можете оформить подписку, нажав на соответствующую кнопку ниже", reply_markup=get_first_subscription_menu())

        elif call.message.chat.id not in (db.Set('Pay') or db.Set('last_days')):
            await call.message.answer("*Техника будет доступна сразу после оплаты подписки*\n"
                                   "\n"
                                   "Стоимость подписки — *390* руб/мес\n"
                                   "\n"
                                   "Не буду сравнивать эту сумму с парой чашек кофе, слишком избито\. "
                                   "Скажу только, что я специально сделал стоимость настолько доступной, чтобы каждый мог попробовать и испытать на себе силу МАК\.\n"
                                   "\n"
                                   "Чтобы вы смогли, наконец, освободиться от своих проблем и барьеров и сделать прорыв в какой\-то из сфер жизни — вырасти по карьере "
                                   "или в доходах, или найти половинку мечты… "
                                   "Чтобы вы жили полной, гармоничной и счастливой жизнью, той жизнью, которую вы по\-настоящему хотите\!\n"
                                   "\n"
                                   "А эта сумма поможет мне покрыть расходы на оплату серверов, чтобы я мог работать и дальше\.\n"
                                   "\n"
                                   "Ну, и ещё периодически подсыпать корм разработчикам, чтобы они продолжали меня улучшать и добавлять новые крутые Техники "
                                   "и карты \)\n"
                                   "\n"
                                   "Разумеется, подписка открывает полный доступ ко всем Сферам и Техникам, в том числе и новым, которые регулярно добавляются\.\n")
            await call.message.answer("А если оплатить сразу за год, то в месяц выйдет ещё дешевле:\n"
                                   "\n"
                                   "~4680~ *3480* руб/год или ~390~ *290* руб/мес\.\n\(*экономия \-25%*\)")
            await call.message.answer('Вы можете оформить подписку, нажав на соответствующую кнопку ниже', reply_markup=get_subscription_menu())
        else:
            family_area_technique1_next_menu1 = types.InlineKeyboardMarkup()
            family_area_technique1_key1 = types.InlineKeyboardButton(text='Показать карту', callback_data='family_area_technique1_ready1')
            family_area_technique1_next_menu1.add(family_area_technique1_key1, back)
            await call.message.answer("Ок\. Вы выбрали Технику *«Я в семье»*\.\n"
                              '\n'
                               "Прежде, чем мы начнём, напомню, что:\n"
                               "\n"
                                "\- лучше приготовить ручку и бумажку, чтобы потом было легче следить за результатами по вашим записям;\n"
                              "\n"
                                "\- старайтесь записывать первое, что пришло на ум, не думайте дольше 6\-10 секунд;\n"
                                      "\n"
                                      "\- я побуду вашей рукой и буду вытягивать случайные карты из колоды\.\n")
            await call.message.answer("Задайте себе первый вопрос:\n"
                                      "\n"
                                      "*Как я себя вижу в семье?*")
            await call.message.answer("Как будете готовы, нажмите кнопку «Показать карту»", reply_markup=family_area_technique1_next_menu1)

@dp.callback_query_handler(text="family_area_technique1_ready1")
async def family_area_technique1_ready1(call: types.CallbackQuery):
    family_area_technique4_pict1 = pict.copy()
    family_area_technique1_next_menu2 = types.InlineKeyboardMarkup()
    family_area_technique1_key2 = types.InlineKeyboardButton(text='Дальше', callback_data='family_area_technique1_next1')
    family_area_technique1_next_menu2.add(family_area_technique1_key2, back)
    x = family_area_technique4_pict1[randint(0, len(family_area_technique4_pict1) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Посмотрите внимательно на карту\. Что на ней? Как это связано с вами?\n'
                              '\n'
                              'Запишите ответ\.\n'
                              '\n'
                              'Как закончите, нажмите кнопку «Дальше»', reply_markup=family_area_technique1_next_menu2)
    family_area_technique4_pict1.remove(x)
    global family_area_technique4_pict2
    family_area_technique4_pict2 = family_area_technique4_pict1.copy()
@dp.callback_query_handler(text="family_area_technique1_next1")
async def family_area_technique1_next1(call: types.CallbackQuery):
    await call.message.answer("Теперь задайте себе следующий вопрос:\n"
                     "\n"
                     "*Как меня видит в семье супруг\(а\)?*")
    family_area_technique1_next_menu3 = types.InlineKeyboardMarkup()
    family_area_technique1_key3 = types.InlineKeyboardButton(text='Показать карту', callback_data='family_area_technique1_ready2')
    family_area_technique1_next_menu3.add(family_area_technique1_key3, back)
    await call.message.answer('И нажмите кнопку «Показать карту»', reply_markup=family_area_technique1_next_menu3)
@dp.callback_query_handler(text="family_area_technique1_ready2")
async def family_area_technique1_ready2(call: types.CallbackQuery):
    family_area_technique1_next_menu4 = types.InlineKeyboardMarkup()
    family_area_technique1_key4 = types.InlineKeyboardButton(text='Дальше', callback_data='family_area_technique1_next2')
    family_area_technique1_next_menu4.add(family_area_technique1_key4, back)
    x = family_area_technique4_pict2[randint(0, len(family_area_technique4_pict2) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Что вы видите на этой карте?\n'
                              '\n'
                     'Как будете готовы к следующему вопросу, нажмите кнопку «Дальше»', reply_markup=family_area_technique1_next_menu4)
    family_area_technique4_pict2.remove(x)
    global family_area_technique4_pict3
    family_area_technique4_pict3 = family_area_technique4_pict2.copy()
@dp.callback_query_handler(text="family_area_technique1_next2")
async def family_area_technique1_next2(call: types.CallbackQuery):
    await call.message.answer("Дальше вы спрашиваете себя:\n"
                     "\n"
                     "*Как меня видят дети?*")
    family_area_technique1_next_menu5 = types.InlineKeyboardMarkup()
    family_area_technique1_key5 = types.InlineKeyboardButton(text='Показать карту', callback_data='family_area_technique1_ready3')
    family_area_technique1_next_menu5.add(family_area_technique1_key5, back)
    await call.message.answer('И нажимаете кнопку «Показать карту»', reply_markup=family_area_technique1_next_menu5)
@dp.callback_query_handler(text="family_area_technique1_ready3")
async def family_area_technique1_ready3(call: types.CallbackQuery):
    family_area_technique1_next_menu6 = types.InlineKeyboardMarkup()
    family_area_technique1_key6 = types.InlineKeyboardButton(text='Дальше', callback_data='family_area_technique1_next3')
    family_area_technique1_next_menu6.add(family_area_technique1_key6, back)
    x = family_area_technique4_pict3[randint(0, len(family_area_technique4_pict3) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Не забывайте записывать ответы, которые всплывают в сознании\.\n'
                              '\n'
                     'И затем нажмите кнопку «Дальше»', reply_markup=family_area_technique1_next_menu6)
    family_area_technique4_pict3.remove(x)
    global family_area_technique4_pict4
    family_area_technique4_pict4 = family_area_technique4_pict3.copy()
@dp.callback_query_handler(text="family_area_technique1_next3")
async def family_area_technique1_next3(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос, который вы адресуете своему Бессознательному:\n"
                     "\n"
                     "*Каким \(какой\) мне надо быть в семье?*")
    family_area_technique1_next_menu7 = types.InlineKeyboardMarkup()
    family_area_technique1_key7 = types.InlineKeyboardButton(text='Показать карту', callback_data='family_area_technique1_ready4')
    family_area_technique1_next_menu7.add(family_area_technique1_key7, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=family_area_technique1_next_menu7)
@dp.callback_query_handler(text="family_area_technique1_ready4")
async def family_area_technique1_ready4(call: types.CallbackQuery):
    family_area_technique1_next_menu8 = types.InlineKeyboardMarkup()
    family_area_technique1_key8 = types.InlineKeyboardButton(text='Дальше', callback_data='family_area_technique1_next4')
    family_area_technique1_next_menu8.add(family_area_technique1_key8, back)
    x = family_area_technique4_pict4[randint(0, len(family_area_technique4_pict4) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=family_area_technique1_next_menu8)
    family_area_technique4_pict4.remove(x)
    global family_area_technique4_pict5
    family_area_technique4_pict5 = family_area_technique4_pict4.copy()
@dp.callback_query_handler(text="family_area_technique1_next4")
async def family_area_technique1_next4(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*Что я чувствую в своей семье?*")
    family_area_technique1_next_menu9 = types.InlineKeyboardMarkup()
    family_area_technique1_key9 = types.InlineKeyboardButton(text='Показать карту', callback_data='family_area_technique1_ready5')
    family_area_technique1_next_menu9.add(family_area_technique1_key9, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=family_area_technique1_next_menu9)
@dp.callback_query_handler(text="family_area_technique1_ready5")
async def family_area_technique1_ready5(call: types.CallbackQuery):
    family_area_technique1_next_menu10 = types.InlineKeyboardMarkup()
    family_area_technique1_key10 = types.InlineKeyboardButton(text='Дальше', callback_data='family_area_technique1_next5')
    family_area_technique1_next_menu10.add(family_area_technique1_key10, back)
    x = family_area_technique4_pict5[randint(0, len(family_area_technique4_pict5) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Записали ответ? Нажмите кнопку «Дальше»', reply_markup=family_area_technique1_next_menu10)
    family_area_technique4_pict5.remove(x)
    global family_area_technique4_pict6
    family_area_technique4_pict6 = family_area_technique4_pict5.copy()
@dp.callback_query_handler(text="family_area_technique1_next5")
async def family_area_technique1_next5(call: types.CallbackQuery):
    await call.message.answer("Продолжаем\. Следующий вопрос:\n"
                     "\n"
                     "*Что я чувствую, общаясь с детьми?*")
    family_area_technique1_next_menu11 = types.InlineKeyboardMarkup()
    family_area_technique1_key11 = types.InlineKeyboardButton(text='Показать карту', callback_data='family_area_technique1_ready6')
    family_area_technique1_next_menu11.add(family_area_technique1_key11, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=family_area_technique1_next_menu11)
@dp.callback_query_handler(text="family_area_technique1_ready6")
async def family_area_technique1_ready6(call: types.CallbackQuery):
    family_area_technique1_next_menu12 = types.InlineKeyboardMarkup()
    family_area_technique1_key12 = types.InlineKeyboardButton(text='Дальше', callback_data='family_area_technique1_next6')
    family_area_technique1_next_menu12.add(family_area_technique1_key12, back)
    x = family_area_technique4_pict6[randint(0, len(family_area_technique4_pict6) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Нажмите кнопку «Дальше»', reply_markup=family_area_technique1_next_menu12)
    family_area_technique4_pict6.remove(x)
    global family_area_technique4_pict7
    family_area_technique4_pict7 = family_area_technique4_pict6.copy()
@dp.callback_query_handler(text="family_area_technique1_next6")
async def family_area_technique1_next6(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос, который вы себе задаёте:\n"
                     "\n"
                     "*Что я чувствую, общаясь с супругом\(ой\)?*")
    family_area_technique1_next_menu13 = types.InlineKeyboardMarkup()
    family_area_technique1_key13 = types.InlineKeyboardButton(text='Показать карту', callback_data='family_area_technique1_ready7')
    family_area_technique1_next_menu13.add(family_area_technique1_key13, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=family_area_technique1_next_menu13)
@dp.callback_query_handler(text="family_area_technique1_ready7")
async def family_area_technique1_ready7(call: types.CallbackQuery):
    family_area_technique1_next_menu14 = types.InlineKeyboardMarkup()
    family_area_technique1_key14 = types.InlineKeyboardButton(text='Дальше', callback_data='family_area_technique1_next7')
    family_area_technique1_next_menu14.add(family_area_technique1_key14, back)
    x = family_area_technique4_pict7[randint(0, len(family_area_technique4_pict7) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Когда будете готовы продолжать, нажмите кнопку «Дальше»', reply_markup=family_area_technique1_next_menu14)
    family_area_technique4_pict7.remove(x)
    global family_area_technique4_pict8
    family_area_technique4_pict8 = family_area_technique4_pict7.copy()
@dp.callback_query_handler(text="family_area_technique1_next7")
async def family_area_technique1_next7(call: types.CallbackQuery):
    await call.message.answer("Следующий вопрос:\n"
                     "\n"
                     "*А что я хочу чувствовать?*")
    family_area_technique1_next_menu15 = types.InlineKeyboardMarkup()
    family_area_technique1_key15 = types.InlineKeyboardButton(text='Показать карту', callback_data='family_area_technique1_ready8')
    family_area_technique1_next_menu15.add(family_area_technique1_key15, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=family_area_technique1_next_menu15)
@dp.callback_query_handler(text="family_area_technique1_ready8")
async def family_area_technique1_ready8(call: types.CallbackQuery):
    family_area_technique1_next_menu16 = types.InlineKeyboardMarkup()
    family_area_technique1_key16 = types.InlineKeyboardButton(text='Дальше', callback_data='family_area_technique1_next8')
    family_area_technique1_next_menu16.add(family_area_technique1_key16, back)
    x = family_area_technique4_pict8[randint(0, len(family_area_technique4_pict8) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Записали ответ? Нажмите кнопку «Дальше»', reply_markup=family_area_technique1_next_menu16)
    family_area_technique4_pict8.remove(x)
    global family_area_technique4_pict9
    family_area_technique4_pict9 = family_area_technique4_pict8.copy()
@dp.callback_query_handler(text="family_area_technique1_next8")
async def family_area_technique1_next8(call: types.CallbackQuery):
    await call.message.answer("И последний вопрос:\n"
                     "\n"
                     "*А что мне надо для этого сделать \(чтобы чувствовать себя так, как я хочу\)?*")
    family_area_technique1_next_menu17 = types.InlineKeyboardMarkup()
    family_area_technique1_key17 = types.InlineKeyboardButton(text='Показать карту', callback_data='family_area_technique1_ready9')
    family_area_technique1_next_menu17.add(family_area_technique1_key17, back)
    await call.message.answer('Нажмите кнопку «Показать карту»', reply_markup=family_area_technique1_next_menu17)

@dp.callback_query_handler(text="family_area_technique1_ready9")
async def family_area_technique1_ready9(call: types.CallbackQuery):
    family_area_technique1_next_menu18 = types.InlineKeyboardMarkup()
    family_area_technique1_key18 = types.InlineKeyboardButton(text='Продолжить', callback_data='family_area_technique1_Continue1')
    family_area_technique1_next_menu18.add(family_area_technique1_key18, back)
    x = family_area_technique4_pict9[randint(0, len(family_area_technique4_pict9) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Это последняя карта в этой Технике\. \n'
                              '\n'
                              'Теперь можно подвести итог и записать выводы, которые вы для себя сделали — короткое резюме\. \n'
                              '\n'
                              'Но если вы чувствуете, что вам нужна ещё подсказка, то можете попросить её у Бессознательного\.\n'
                              '\n'
                                'Если это необходимо, нажмите кнопку «Продолжить»\. Или вернитесь в главное меню к выбору Техник', reply_markup=family_area_technique1_next_menu18)
    family_area_technique4_pict9.remove(x)
    global family_area_technique4_pict10
    family_area_technique4_pict10 = family_area_technique4_pict9.copy()
@dp.callback_query_handler(text="family_area_technique1_Continue1")
async def family_area_technique1_Continue1(call: types.CallbackQuery):
    await call.message.answer('Хорошо, задайте внутрь себя вопрос, который пришёл на ум после предыдущих ответов\.\n'
                              '\n'
                              'Или можно, например, задать вопрос: *Что с этим теперь делать прямо сейчас? Какой первый шаг?*')
    family_area_technique1_next_menu19 = types.InlineKeyboardMarkup()
    family_area_technique1_key19 = types.InlineKeyboardButton(text='Показать карту', callback_data='family_area_technique1_ready10')
    family_area_technique1_next_menu19.add(family_area_technique1_key19, back)
    await call.message.answer('Как будете готовы, нажмите кнопку «Показать карту»', reply_markup=family_area_technique1_next_menu19)
@dp.callback_query_handler(text="family_area_technique1_ready10")
async def family_area_technique1_ready10(call: types.CallbackQuery):
    x = family_area_technique4_pict10[randint(0, len(family_area_technique4_pict10) - 1)]
    await bot.send_photo(call.message.chat.id, x)
    await call.message.answer('Запишите полученный ответ\.\n'
                              '\n'
                              'На этом Техника _«Я в семье»_ завершена\.\n'
                                '\n'
                              'Подведите итог и запишите выводы, которые вы для себя сделали — короткое резюме\.\n'
                              '\n'
                     'Затем вернитесь в главное меню к выбору Техник',
                     reply_markup=get_jamp_mainmenu())








# Обрабтка нажатия кнопки "Оформить подписку на месяц"
@dp.callback_query_handler(text="subscription_month")
async def process_buy_month(call: types.CallbackQuery):
    if config.PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await call.message.answer('Так как сейчас я запущен в тестовом режиме, для оплаты нужно использовать карту: 1111 1111 1111 1026, 12/22, CVC 000')

    await bot.send_invoice(call.message.chat.id,
                           title='Оплатить подписку на месяц',
                           description='Полный доступ ко всем техникам бота «Метафорические карты» на месяц',
                           provider_token=config.PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[PRICES[0]],
                           start_parameter='subscription_month_parameter',
                           payload='month'
                           )

# Обрабтка нажатия кнопки "Оформить подписку на год"
@dp.callback_query_handler(text="subscription_year")
async def process_buy_year(call: types.CallbackQuery):
    if config.PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await call.message.answer('Так как сейчас я запущен в тестовом режиме, для оплаты нужно использовать карту: 1111 1111 1111 1026, 12/22, CVC 000')

    await bot.send_invoice(call.message.chat.id,
                           title='Оплатить подписку на год',
                           description='Полный доступ ко всем техникам бота «Метафорические карты» на год',
                           provider_token=config.PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[PRICES[1]],
                           start_parameter='subscription_year_parameter',
                           payload='year'
                           )


# Обрабтка нажатия кнопки "Оформить подписку на месяц + 1"
@dp.callback_query_handler(text="first_subscription_month")
async def process_buy_month_1(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='*Вы в меню оплаты*\n')

    with Vedis(config.db_file) as db:
        db.Set('First').remove(call.message.chat.id)
    if config.PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await call.message.answer('Так как сейчас я запущен в тестовом режиме, для оплаты нужно использовать карту: 1111 1111 1111 1026, 12/22, CVC 000')

    await bot.send_invoice(call.message.chat.id,
                           title='Оплатить подписку на месяц',
                           description='Полный доступ ко всем техникам бота «Метафорические карты» на месяц. Оплачивая сейчас, в подарок вы получаете + 1 месяц подписки',
                           provider_token=config.PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[PRICES1[0]],
                           start_parameter='subscription_month_parameter',
                           payload='month_month'
                           )

# Обрабтка нажатия кнопки "Оформить подписку на год + 6мес"
@dp.callback_query_handler(text="first_subscription_year")
async def process_buy_year_6(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='*Вы в меню оплаты*\n')

    with Vedis(config.db_file) as db:
        db.Set('First').remove(call.message.chat.id)
    if config.PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await call.message.answer('Так как сейчас я запущен в тестовом режиме, для оплаты нужно использовать карту: 1111 1111 1111 1026, 12/22, CVC 000')

    await bot.send_invoice(call.message.chat.id,
                           title='Оплатить подписку на год',
                           description='Полный доступ ко всем техникам бота «Метафорические карты» на год. Оплачивая сейчас, в подарок вы получаете + 6 месяцев подписки',
                           provider_token=config.PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[PRICES[1]],
                           start_parameter='subscription_year_parameter',
                           payload='year_6month'
                           )



# Отправка боту служебного сообщения, что оплата произведена
@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Ловим сообщение бота об успешной оплате
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    user_id = str(message.chat.id)
    if message.successful_payment.invoice_payload == 'month': # если оплачена месячная подписка
        remember_date_month = date.today() + timedelta(days=2) # запоминаем дату завершения подписки
        with Vedis(config.db_file) as db:
            db[user_id + 'pay_start'] = date.today()  # запоминаем в базе дату начала подписки
            db.Set('Month').add(user_id) # добавляем юзера в множество тех, кто подписался на месяц
            if user_id not in db.Set('Pay'): # проверяем, нет ли юзера уже в базе людей, кто оформил платную подписку (например, когда он продлевает подписку)
                db[user_id + 'pay_end'] = remember_date_month # если нет, запоминаем его в базе: ключ - 'юзер айди + pay_end', значение - дата завершения подписки
                db.Set('Pay').add(user_id)
            else:
                db.Set('Year').remove(user_id)
                db.Set('Extend_status_year').remove(user_id)
                db.Set('Extend_status_month').add(user_id)
                delta = remember_date_month - date.today()
                db_datetime = datetime.strptime(str(db[user_id + 'pay_end'].decode()), "%Y-%m-%d") # если юзер уже есть в базе, достаем записанную дату
                db_date = datetime.date(db_datetime)
                db[user_id + 'pay_end'] = db_date + delta # прибавляем к оставшимся дням новую дату завершения подписки

    elif message.successful_payment.invoice_payload == 'year': # аналогично месячной подписки
        remember_date_year = date.today() + timedelta(days=1)
        with Vedis(config.db_file) as db:
            db[user_id + 'pay_start'] = date.today()  # запоминаем в базе дату начала подписки
            db.Set('Year').add(user_id)
            if user_id not in db.Set('Pay'):
                db[user_id + 'pay_end'] = remember_date_year
                db.Set('Pay').add(user_id)
            else:
                db.Set('Month').remove(user_id)
                db.Set('Extend_status_month').remove(user_id)
                db.Set('Extend_status_year').add(user_id)
                delta = remember_date_year - date.today()
                db_datetime = datetime.strptime(str(db[user_id + 'pay_end'].decode()), "%Y-%m-%d")
                db_date = datetime.date(db_datetime)
                db[user_id + 'pay_end'] = db_date + delta

    elif message.successful_payment.invoice_payload == 'month_month': # если оплачена месячная подписка с подарком
        remember_date_month_1 = date.today() + timedelta(days=4) # запоминаем дату завершения подписки + подарок 1мес
        with Vedis(config.db_file) as db:
            db[user_id + 'pay_start'] = date.today()  # запоминаем в базе дату начала подписки
            db.Set('Month').add(user_id) # добавляем юзера в множество тех, кто подписался на месяц
            db[user_id + 'pay_end'] = remember_date_month_1 # запоминаем его в базе: ключ - 'юзер айди + pay_end', значение - дата завершения подписки
            db.Set('Pay').add(user_id)

    elif message.successful_payment.invoice_payload == 'year_6month': # аналогично месячной подписки
        remember_date_year_6 = date.today() + timedelta(days=2) # запоминаем дату завершения подписки + подарок 6мес
        with Vedis(config.db_file) as db:
            db[user_id + 'pay_start'] = date.today()  # запоминаем в базе дату начала подписки
            db.Set('Year').add(user_id)
            db[user_id + 'pay_end'] = remember_date_year_6
            db.Set('Pay').add(user_id)


    # print('successful_payment:')
    # pmnt = message.successful_payment.to_python()
    # for key, val in pmnt.items():
    #     print(f'{key} = {val}')
    with Vedis(config.db_file) as db:
        d = db[user_id + 'pay_end'].decode()
        await message.answer(text=f'Спасибо! Платеж совершен успешно!\n'
                             f'\n'
                             f'Дата окончания вашей подписки: {d}\n'
                                  f'\n'
                             f'Приятного пользования!', parse_mode='')
    await message.answer('Вернуться в главное меню', reply_markup=get_jamp_mainmenu())








# декоратор для отлова исключений повторяющихся действий
# def catch_exceptions(cancel_on_failure=False):
#     def catch_exceptions_decorator(job_func):
#         @functools.wraps(job_func)
#         def wrapper(*args, **kwargs):
#             try:
#                 return job_func(*args, **kwargs)
#             except:
#                 import traceback
#                 print(traceback.format_exc())
#                 if cancel_on_failure:
#                     return aioschedule.CancelJob

#         return wrapper

#     return catch_exceptions_decorator

# # Проверяем и напоминаем о завершении подписки
# @catch_exceptions(cancel_on_failure=True)
async def repeat():
    with Vedis(config.db_file) as db:
        try:
            for i in db.Set('Pay'):
                datetime_str_year = datetime.strptime(str(db[i.decode() + 'pay_end'].decode()), "%Y-%m-%d")
                db_date = datetime.date(datetime_str_year)
                if date.today() == (db_date - timedelta(days=2)):
                    try:
                        await bot.send_message(i.decode(), 'Мне очень жаль, но ваша подписка закончится через 2 дня\. Хотите продлить?', reply_markup=get_yes_no_menu())
                        if i.decode() in db.Set('Blocked'):
                            db.Set('Blocked').remove(i.decode())
                    except:
                        db.Set('Blocked').add(i.decode())
                elif date.today() == (db_date - timedelta(days=1)):
                    try:
                        await bot.send_message(i.decode(), 'Просто напоминаю, что ваша подписка закончится через 1 день\. Будем продлять?', reply_markup=get_yes_no_menu())
                        if i.decode() in db.Set('Blocked'):
                            db.Set('Blocked').remove(i.decode())
                    except:
                        db.Set('Blocked').add(i.decode())
                elif db_date == date.today():
                    try:
                        await bot.send_message(i.decode(), 'Так как вы до сих пор не определились, на всякий случай, напомню в последний \(честно\!\) раз, что ваша подписка закончится сегодня\. Может захотите продлить?', reply_markup=get_yes_no_menu())
                        if i.decode() in db.Set('Blocked'):
                            db.Set('Blocked').remove(i.decode())
                    except:
                        db.Set('Blocked').add(i.decode())
                elif date.today() >= (db_date + timedelta(days=1)):
                    try:
                        await bot.send_message(i.decode(), 'Ваша подписка закончилась\. Если захотите, можете подписаться снова в любой момент', reply_markup=get_jamp_mainmenu())
                        if i.decode() in db.Set('Blocked'):
                            db.Set('Blocked').remove(i.decode())
                    except:
                        db.Set('Blocked').add(i.decode())
                    try:
                        db.Set('Month').remove(i.decode()) # удаляем из множества
                    except:
                        pass
                    try:
                        db.Set('Year').remove(i.decode())  # удаляем из множества
                    except:
                        pass
                    db.Set('Pay').remove(i.decode())  # удаляем из множества
                    try:
                        db.Set('Extend_status_month').remove(i.decode())  # и удаляем из множества "Продливших на месяц"
                    except:
                        pass
                    try:
                        db.Set('Extend_status_year').remove(i.decode())  # удаляем из множества
                    except:
                        pass
                    del db[i.decode() + 'pay_end'] # и удаляем из базы
                    del db[i.decode() + 'pay_start']  # и удаляем из базы
            await asyncio.sleep(0.2)
        except:
            pass

        try:
            for n in db.Set('last_days'):
                datetime_str_month = datetime.strptime(str(db[n.decode() + 'pay_end'].decode()), "%Y-%m-%d")
                db_date = datetime.date(datetime_str_month)
                if date.today() >= (db_date + timedelta(days=1)): # Если текущая дата равна (дате в базе + 1 день)
                    try:
                        await bot.send_message(n.decode(), 'Ваша подписка закончилась\. Если захотите, можете подписаться снова в любой момент', reply_markup=get_jamp_mainmenu())
                        if n.decode() in db.Set('Blocked'):
                            db.Set('Blocked').remove(n.decode())
                    except:
                        db.Set('Blocked').add(n.decode())
                    db.Set('last_days').remove(n.decode()) # удаляем из множества
                    # for l in db.Set('last_days'):
                    #     print(l)
                    del db[n.decode() + 'pay_end'] # и удаляем из базы
                    del db[n.decode() + 'pay_start']  # и удаляем из базы
            await asyncio.sleep(0.2)
        except:
            pass








# Обработка кнопки согласия продления подписки
@dp.callback_query_handler(text="subscription_yes")
async def subscription_yes(call: types.CallbackQuery):
    await call.message.answer(
        'Отлично\! Вы можете продлить подписку, нажав на соответствующую кнопку ниже',
        reply_markup=get_subscription_menu())

# Обработка кнопки отказа от продления подписки
@dp.callback_query_handler(text="subscription_no")
async def subscription_no(call: types.CallbackQuery):
    user_id = str(call.message.chat.id)
    with Vedis(config.db_file) as db:
        if user_id in db.Set('Pay'):
            datetime_str_month = datetime.strptime(str(db[user_id + 'pay_end'].decode()), "%Y-%m-%d")
            db_date = datetime.date(datetime_str_month)
            if date.today() == (db_date - timedelta(days=2)) or date.today() == (db_date - timedelta(days=1)) or date.today() == db_date:
                db.Set('last_days').add(user_id) # если юзер отказался продлять подписку, но у него еще есть оставшиеся дни, записываем его в новое множество "Последние дни"
                try:
                    db.Set('Month').remove(user_id)  # удаляем из множества "Месяц"
                except:
                    pass
                try:
                    db.Set('Year').remove(user_id)
                except:
                    pass
                db.Set('Pay').remove(user_id)  # и удаляем из множества "Платников" (оплативших платную подписку)
                try:
                    db.Set('Extend_status_month').remove(user_id)  # и удаляем из множества "Продливших на месяц"
                except:
                    pass
                try:
                    db.Set('Extend_status_yaer').remove(user_id)  # и удаляем из множества "Продливших на год"
                except:
                    pass
    await call.message.answer('Хорошо\. Если передумаете, всегда можете подписаться снова в любой момент')
    await call.message.answer('Вернуться в главное меню', reply_markup=get_jamp_mainmenu())









# запускаем повторяющийся процесс (проверку окончания подписки)
async def scheduler():
    aioschedule.every().day.at("10:00").do(repeat)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    await asyncio.create_task(scheduler())
    await bot.set_webhook(config.WEBHOOK_URL)

# drop_pending_updates=True
    
async def on_shutdown(_):
    await bot.delete_webhook()

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT
    )
    
#     loop=loop,
    
