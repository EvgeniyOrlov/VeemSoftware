import psutil
import subprocess
from time import sleep
import datetime


def proc(way):
    for el in psutil.pids()[1:]:
        pid = psutil.Process(el).exe()
        if pid == way:
            return el
        else:
            continue


w = input('Ведите полный путь к исполняемому процессу: ')
n = int(input('Задайте интервал сбора статистики: '))

process_for_test = subprocess.Popen([w])
print('Запуск...')
sleep(3)
print('Скрипт запущен.\n'
      'Для прекращения сбора статистики закройте окно.\n'
      '\n'
      'После прекращения работы приложения, файлы сохраняются в директорию "Statistic files"')
now = datetime.datetime.now()
p = psutil.Process(proc(w))

while True:
    ls = []
    with p.oneshot():
        ls.append(f'Загрузка CPU - {p.cpu_percent(interval=n)}%')
        ls.append(f'Потребление памяти: Private Bytes - {p.memory_info().private / 1024} Mb')
        ls.append(f'Потребление памяти: Working Set - {p.memory_info().wset / 1024} Mb')
        ls.append(f'Количество открытых хендлов - {p.num_handles()}\n')
    with open(f'Statistic files/{p.name()} {now.strftime("%d-%m-%Y %H-%M")}', 'a', encoding='UTF-8') as f:
        for line in ls:
            f.write(f'{line}\n')
        ls.clear()
