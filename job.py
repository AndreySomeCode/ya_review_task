# review:
# можно упрядочить импорты (это не обязательно, для этого даже есть утилита isort)
# вначале import после них разместить from
import shutil
from urllib.request import urlopen
from pathlib import Path
import ssl
import json
from logger import logger  # review: поправить не првальный импорт и получение логгера
                           # советую посмотреть бибилиотку loguru она более простая
                           # чем logging из стандартной библиотки (и подходит для простых
                           # небольших программ)

# review: удалить, не используется
def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


def get_and_write_data(condition, url): # review: async def, убрать condition
    # review:
    # в асихронноми коде лучше испльзовать асинхонные бибилиотеки
    # как вариант httpx вметсо стандартной urllib3
    # 
    # но оставим urllib3, злые люди в условия нашей задачи сказали
    # "2. Использовать встроенные библиотеки и модули языка."
    # (╮°-°)╮┳━━┳ ( ╯°□°)╯ ┻━━┻ 
    # 
    # рекомендую ознакомится с различием между синхронными (блокирующими)
    # и асинхронными (не блокирующими) операциями
    context = ssl._create_unverified_context()
    file = 'punchline.txt' # review: т.к. имя файла общее на все методы можно его 
                           # вынести в константы
    with condition: # review: убираем на уровень Job реализуем проверку в методе run
        #review:  можно всю работу с запросом и файлом поместить в try except
        with urlopen(url, context=context) as req:
            resp = req.read().decode("utf-8")
            resp = json.loads(resp)
        if req.status != 200:
            raise Exception(
                "Error during execute request. {}: {}".format(
                    resp.status, resp.reason
                )
            )
        data = resp
        if isinstance(data, dict):
            path = Path(file)
            setup = data['setup']
            punchline = data['punchline']
            print( # reveiw: заменить на логирование
                f'Setup: {setup} \n'
                f'Punchline: {punchline}'
            )
            with open(path, mode='a') as config:
                config.write(str(data))
        else:
            # review: заменить на raise ValueError("text {}".fromat(data))
            logger.error(type(data))
            logger.error(ValueError)
            raise ValueError
        # reivew: 
        # в except логировать исключение logger.exception(err)
        # и если надо прокидывать его дальше делая его raise


def copy_file(condition, x=None):  # review: async def, убрать condition
    file = 'punchline.txt' # review: использовать константу
    to_path = './jokes/' # review: создавать дирректорию 
    with condition: # review: убираем на уровень Job.run
        condition.wait(timeout=1)
        try:
            shutil.copy(file, to_path)
        except FileNotFoundError as ex:
            logger.error('Файл не найден %s', ex)


def delete_file(condition, x=None):  # review: async def, убрать condition
    file = 'punchline.txt' # review: использовать константу
    obj = Path(file)
    with condition: # review: убираем на уровень Job.run
        condition.wait(timeout=1)
        try:
            obj.unlink()
            logger.info('Удалил файл')
        except FileNotFoundError as ex:
            logger.error(ex)


class Job:
    def __init__(
            self,
            func=None,
            name=None,
            args=None,
    ):
        # review:
        # параметры запуска (tries, start_at, max_working_time из Scheduler)
        # должны находиться в Job т.к. являются
        self.args = args
        self.name = name
        self.func = func

    def run(self, *args): # review: async
        # review: 
        # перезапуск, обрабку исключений, и обработку зависимостей (condition)
        # можно реализовать в этом месть
        tar = self.func(*args) # review: т.к. фунции стали асинхрронные добавить await
        logger.info('тип объекта в Job.run %s', type(tar))
        logger.debug('запуск объекта %s', tar)
        return tar
