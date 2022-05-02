import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from api_lib.async_api import ApiAsync
from api_lib.utils.messages import CallbackMessage
from api_lib.utils.validation_utils import InputParam
from config import TOKEN, test_schema

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
# Для обработки колбеков необходим редис,
# данные для получения схемы
# апи(в данном случае используется тестовая зашитая
# в коде)
api = ApiAsync(service_name='TELEGRAMBOT',
               user_api='guest',
               pass_api='guest',
               redis_url='redis://localhost',
               schema=test_schema)


@api.callback_func(name="test_callback")
async def process_callback(message: CallbackMessage):
    # Все методы обработчики должны принимать аргумент с типом IncomingMessage
    # и возвращать либо None, либо CallbackMessage.

    # Обрабатываем сообщение пришедшее от сервиса
    # И отправляем ответ пользователю
    user_id = message.incoming_message.additional_data['user_id']
    await bot.send_message(user_id, text=f'Сообщение обработано: {message.response}')


@dp.message_handler(commands=['send_thirdservice'])
async def process_start_command(message: types.Message):
    # Отправляем сообщение в сторонний сервис в один из его методов,
    # записываем доп. информацию в редис(она будет доступна после при
    # обработке)
    # callback_method_name - метод из словаря api.methods_callback
    await api.send_request_api('test_method',
                               [InputParam('test_str', '2222')],
                               callback_method_name='test_callback',
                               requested_service='THIRDSERVICE',
                               additional_data={'user_id': message.chat.id})
    await message.reply("Отправка в THIRDSERVICE")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Слушаем очередь "в фоне"
    loop.create_task(api.listen_queue())
    executor.start_polling(dp, loop=loop)
