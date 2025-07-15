import datetime

from aiogram.utils import executor
from create import dp
from handlers import client, admin, analysis


client.register_client_handlers(dp)
# admin.register_admin_handlers(dp)


if __name__ == '__main__':
    dp.loop.create_task(analysis.check_time())
    executor.start_polling(dp)
