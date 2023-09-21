import disnake
import os
import sqlite3
from disnake.ext import commands

# Создаем бота
bot = commands.Bot(command_prefix='/')

# Создаем соединение с базой данных
conn = sqlite3.connect('scores.db')
cursor = conn.cursor()

# Создаем таблицу для хранения очков для каждого пользователя, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS scores (
    user_id INTEGER PRIMARY KEY,
    active_points INTEGER NOT NULL,
    inactive_points INTEGER NOT NULL
);
''')
conn.commit()

# Функция для получения очков пользователя из базы данных
def get_scores(user_id: int):
    cursor.execute('SELECT active_points, inactive_points FROM scores WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    if row:
        active_points, inactive_points = row
    else:
        active_points, inactive_points = 0, 0
    return active_points, inactive_points

# Функция для изменения очков пользователя в базе данных
def set_scores(user_id:int, active_points: int, inactive_points: int):
    cursor.execute('''
    INSERT OR REPLACE INTO scores (user_id, active_points, inactive_points)
    VALUES (?, ?, ?)
    ''', (user_id, active_points, inactive_points))
    conn.commit()

# Команда для вывода очков пользователя
@bot.slash_command()
async def ochki(inter, member: disnake.Member = None):
    if member is None:
        member = inter.author
    user_id = member.id
    active_points, inactive_points = get_scores(user_id)
    embed = disnake.Embed(title=f"Очки пользователя {member.display_name}", description=f"Очки активности: {active_points}\nОчки неактивности: {inactive_points}")
    await inter.response.send_message(embed=embed)

# Команда для выдачи очка активности
@bot.slash_command()
async def addoa(inter, member: disnake.Member):
    if not inter.author.guild_permissions.manage_roles:
        return await inter.response.send_message("Вы не можете использовать эту команду.")
    user_id = member.id
    active_points, inactive_points = get_scores(user_id)
    active_points += 1
    set_scores(user_id, active_points, inactive_points)
    await inter.response.send_message(f"1 очко активности было выдано {member.display_name}")

# Команда для выдачи очка неактивности
@bot.slash_command()
async def addona(inter, member: disnake.Member):
    if not inter.author.guild_permissions.manage_roles:
        return await inter.response.send_message("Вы не можете использовать эту команду.")
    user_id = member.id
    active_points, inactive_points = get_scores(user_id)
    inactive_points += 1
    set_scores(user_id, active_points, inactive_points)
    await inter.response.send_message(f"1 очко неактивности было выдано {member.display_name}")

@bot.slash_command()
async def hi(inter):
    await inter.response.send_message("хуй пизда хуй пизда")

@bot.slash_command()
async def help(inter):
    embed = disnake.Embed(title="Что дают очки активности:", description="в разработке...")
    await inter.response.send_message(embed=embed)

bot.run("YOUR BOT TOKEN")
