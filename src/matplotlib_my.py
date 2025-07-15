import asyncio
import datetime
import io

import matplotlib.pyplot as plt
from google_api import read
from create import db, bot

fig, ax = plt.subplots()

# x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
# y1 = [5.3, 7.1, 4, 5, 9, 9.2, 7.1, 3, 5, 4.3, 10.2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
#
# x2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# y2 = [2.3, 3.1, 7, 4, 9, 2.2, 5.1, 6, 2, 1.3, 15.2]


async def design(x1, y1, x2, y2, maxx, tg_id):
    try:
        # plt.clf()
        ax.plot(x1, y1, color='red')
        ax.plot(x2, y2, color='green')

        ax.set_xlabel('Дни', fontsize=15, color='blue')
        ax.set_ylabel('Ваша оценка', fontsize=15, color='blue')
        plt.text(0.5, maxx + 0.55, 'Красный - физическое состояние', color='red', fontsize=13)
        plt.text(0.5, maxx + 1.1, "Зеленый - духовно-эмоциональное состояние", color='green', fontsize=13)

        with io.BytesIO() as buffer:  # use buffer memory
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image = buffer.getvalue()
            await bot.send_photo(tg_id, image)
            await bot.send_message(tg_id, 'Бот прислал вам график, основанный на ваших показаниях в течении месяца.')
    except Exception as e:
        print('Error matplotlib_1, ', e)


async def preparation(tg_id):
    records = await read(db.get_id_sheets(tg_id))
    now = datetime.datetime.now()
    phys = []
    emotional = []
    for record in records:
        if len(record[0].split('-')) == 3 and (int(record[0].split('-')[1]) == now.month):
            emotional.append(int(record[1]))
            phys.append(int(record[3]))
    maxx = max(max(phys), max(emotional))
    await design([i for i in range(1, len(phys) + 1)], phys, [i for i in range(1, len(emotional) + 1)], emotional, maxx, tg_id)
    # print(records)

# asyncio.run(design(x1, y1, x2, y2, 15.2, ...))