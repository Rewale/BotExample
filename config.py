# Токен бота
TOKEN = ''

# Тестовая схема api
test_schema = {
    'TELEGRAMBOT': {
        'AMQP': {
            'config': {
                'address': '127.0.0.1',
                'port': 5672,
                'username': 'guest',
                'password': 'guest',
                'exchange': 'telegrambot',
                'quenue': 'telegrambot',
                'virtualhost': '/',
                'timeout': 30000
            },
        }

    },
    'THIRDSERVICE': {
        'AMQP': {
            'config': {
                'address': '127.0.0.1',
                'port': 5672,
                'username': 'guest',
                'password': 'guest',
                'exchange': 'thirdservice',
                'quenue': 'thirdservice',
                'virtualhost': '/',
                'timeout': 30000
            },
            'methods': {
                'write': {
                    'test_method': {
                        'test_str': ['str', 32, True],
                        'test_bool': ['bool', None, False]

                    }
                }
            }
        }

    }

}
