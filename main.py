from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from clockify import task_with_highest_time, hours_worked, calculate_hours_worked


bot = Bot(token='6011974332:AAHBMIANcxxbDpKKAD8B8Yzmk5toetgqyAU')
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

workspace_id = '648b6ba2120abb5b98c51126'
api_key = 'ZWVlYzcwMGEtYmE0Zi00MjRhLTlhNDgtOGFkZDVhY2Y2ODEz'


@dp.message_handler(Command("start"))
async def hours_worked_command(message: types.Message):
    await message.answer(text='Здравствуйте, чтобы получить информацию о сотрудниках введите команду /info')


@dp.message_handler(Command("info"))
async def hours_worked_command(message: types.Message):
    task_with_highest_time, hours_worked = calculate_hours_worked(api_key, workspace_id)
    for user_name, task_info in task_with_highest_time.items():
        info_message = f"User: {user_name}\n" \
                       f"Task Name: {task_info['task_name']}\n" \
                       f"Hours: {task_info['hours']}\n" \
                       f"Total hours: {hours_worked[user_name]['total']}\n" \
                       f"Hourly Rate: {hours_worked[user_name]['hourly_rate']}\n" \
                       f"Currency: {hours_worked[user_name]['currency']}\n" \
                       f"Total Amount: {hours_worked[user_name]['total_amount']} {hours_worked[user_name]['currency']}\n"
        await message.answer(info_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
