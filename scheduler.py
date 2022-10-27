# Привет! В общем что смог, то сделал. Остальное даже загуглить не могу.
# По факту просто трачу время, сидя и пялясь в экран. На эту реализацию неделя потрачена))
# Я просто не понимаю даже что гуглить, что бы сделать всё задание.
# Не знаю, может после ревью я с мёртвой точки сдвинусь, поэтому отправляю пока так...


# review: 
#
# Для начала предлагаю ознакомиться со стандартной библиотекой asyncio
# https://docs.python.org/3/library/asyncio.html
# и с современным синтаксисом async / await который был добавлен 
# (в версии python 3.5) для работы с асинхроныыми кодом (корутинами)    
# async def func(param1, param2):
#    do_stuff()
#    await some_coroutine()
#  


# review:
#
# Иcходя из присланного кода тебе попалась старая статья про создание
# корутин при помощи генераторов, что сложно и не удобно и сейчас 
# предпочтителен вариант с использованием "нативные" корутины async def 
#  
# >>> async def other_coro(): 
# >>>    return "Result"
# >>>
# >>>
# >>> async def main(): 
# >>>    result = await other_coro()
# >>> 
# >>> main()
# <coroutine object main at 0x1053bb7c8>
# 
# обрати внимание, что был создан объект корутины, а не выполнена фукция
# для ее выполнения используется библиотека asyncio
# >>> asyncio.run(main())
# "Result"
#
# подробнее об этом сказано в докуменации
# https://docs.python.org/3/library/asyncio-task.html#coroutine


# review: 
# Данное задание можно выполнить используя асинхронный код (async/await)
#  и обойтись без использования multiprocessing
# в задании как подсказка были даны примитивы синхронизации 
# из бибилиотеки multiprocessing, но аналогичные есть и в библиотеки  asyncio

# review: 
# также для выполнения работы ознакомься с механизмом для отмены корутин
# async with asyncio.timeout, asyncio.wait_for и другими в документации


from job import Job, get_and_write_data, delete_file, copy_file
# review:
# рекомендую всегда хотя раз запустить код чтобы проверить, что он работает
# ошибка в импорте и получении логгера
# import logging
# logger =  logging.getLogger()
from logger import logger
import multiprocessing


# review:
# часть многие вещи уже есть в стандатной библиотеке 
# в ней был готовый декоратор для этого случая
# https://docs.python.org/3.10/library/asyncio-task.html#asyncio.coroutine
# но в актуальной версии языка (python3.11) он удален так для создания
# корутин надо испльзовать синтаксис async def
# удалить это декратор, и тоже истьпльзовать async def
def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap

# review: можно просто class Scheduler: т.к. в python 3 классы по умолчанию
# наследуются от object
class Scheduler(object): 
    def __init__(
            self,
# review: 
# tries, start_at, max_working_time перенести в класс Job
# так как они по заданию являются параметрами задачи а не планировщика 
            max_working_time=1,
            tries=0, # review: можно назвать retry_count
            dependencies=(), # review: по умолчанию None, а не пустой tuple 
            start_at=None,
    ):
        super().__init__() # review: не нужен, удалить
        self.task_list: list[Job] = []
        # review: dependencies tries, start_at, max_working_time не должны быть параметрами
        # шедулера, т.к. если они будут в этом классе то будут общие
        # для всех задач, а не конкретной задачи
        self.start_at = start_at 
        self.max_working_time = max_working_time
        self.tries = tries # review: можно назвать retry_count
        self.dependencies = dependencies if dependencies is not None else None

    
    @coroutine # удалить декоратор 
    def schedule(self): # async def удалить декоратор 
        # отказаться от multiprocessing в пользу async / await
        # result = await task.run()    
        # в методе реализовать передачу аргуметов в задачу, ее запуск, и сохранение
        # результатов согласно задания
        # доабвить отмену корутины (смотри способы отмены корутины в asyncio в документации)
        # обработать "перезапуск" задачи
        processes = [] 
        while True: # убрать цикл while
            task_list = (yield) # убрать т.к. мы будет использовать async / await
            print(task_list) # отладочный print заменить на логирование
            for task in task_list: # задачи брать из self.task_list     
                logger.info(f'Планировщик: запускаю задачу - {task.name}')
                p = multiprocessing.Process(target=task.run, args=(condition, url),)
                p.start()
                processes.append(p)
            for process in processes:
                logger.info(process)
                process.join()
                logger.info(f' process {process} stopped!')

    # review: для добавления задач в планировщик можно 
    # реализовать метод add где можно добавть задачу по одной в self.task_list
    # добавить валидацию на число задач согласно условию
    def run(self, jobs: tuple):
        gen = self.schedule() 
        gen.send(jobs) # убрать т.к. async / await 


if __name__ == '__main__':
    # для начала рекомендую выполнить задание разбив его на части
    # выполения его без condition т.е. без зависимых между собой задач задач
    # и только после выполенения основной части работы
    # добавить зависимые между собой задачи
    # и в конце доработать сохранение статуса выполнения задач в файл
    #
    # и после выполения задания проверить код на соответсвие pep8
    # добпвть аннотации типов (при помощи утилит pep8, flake8, mypy)  


    # можно перенести в функцию asyn main
    # а тут только оставить ее запуск asyncio.run

    condition = multiprocessing.Condition()
    url = 'https://official-joke-api.appspot.com/random_joke' # review: можно вынести в константы
    job1 = Job(
        func=get_and_write_data,
        name='Запрос в сеть',
        args=(condition, url), # review: не передвать condition в функцию 
                               # т.к. это она должна быть частью класса Job
    )
    job2 = Job(
        func=copy_file,
        name='Удалить файл',
        args=(condition, ), # review: не передвать condition в функцию 
                            # т.к. это она должна быть частью класса Job
    )
    job3 = Job(
        func=delete_file,
        name='Скопировать файл',
        args=(condition,), # review: не передвать condition в функцию 
                           # т.к. это она должна быть частью класса Job 
    )
    g = Scheduler()  # лучше избегать коротких названий такик как g
    g.run((job1, job2, job3)) 
    # предлагаю разделить добавление задач и их забпус
    # sheduler.add(job)
    # await sheduler.condition(job)
