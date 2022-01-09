import psutil
import subprocess
from time import sleep
import datetime
import csv



def proc(way):
    for el in psutil.pids()[1:]:
        pid = psutil.Process(el).exe()
        if pid == way:
            return el
        else:
            continue


w = input('Ведите полный путь к исполняемому процессу: ')
n = int(input('Задайте интервал сбора статистики: '))

process_for_test = subprocess.run([w], stdout=subprocess.PIPE)
print('Запуск...')
sleep(7)
print('Скрипт запущен.\n'
      'Для прекращения сбора статистики закройте окно.\n'
      '\n'
      'После прекращения работы приложения, файлы сохраняются в директорию "Statistic files"')
now = datetime.datetime.now()
p = psutil.Process(proc(w))

with open(f'Statistic files/{p.name()} {now.strftime("%d-%m-%Y %H-%M")}.csv', 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';')
    csv_writer.writerow(['Загрузка CPU', 'Потребление памяти: Private Bytes', 'Потребление памяти: Working Set', 'Количество открытых хендлов'])

while True:
    with p.oneshot():
        with open(f'Statistic files/{p.name()} {now.strftime("%d-%m-%Y %H-%M")}.csv', 'a', encoding='UTF-8', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow([p.cpu_percent(interval=n), p.memory_info().private / 1024, p.memory_info().wset / 1024, p.num_handles()])
