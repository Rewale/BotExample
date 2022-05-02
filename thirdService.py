""" Код стороннего сервиса с задержкой в отправке сообщения в 5 секунд """
import datetime
from time import sleep


import config
from api_lib.sync_api import ApiSync
from api_lib.utils.messages import IncomingMessage, CallbackMessage


def method(message: IncomingMessage) -> CallbackMessage:
    # Все методы обработчики должны принимать аргумент с типом IncomingMessage
    # и возвращать либо None, либо CallbackMessage
    sleep(5)
    return message.callback_message(param={'answer': message.params['test_str']*2, 'date': datetime.datetime.now()},
                                    result=True)


api = ApiSync('THIRDSERVICE',
              user_api='',
              pass_api='',
              methods={'test_method': method},
              schema=config.test_schema,
              is_test=False)

if __name__ == '__main__':
    api.listen_queue()
