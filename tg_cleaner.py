import os
import sys
import asyncio
from telethon import TelegramClient
from tqdm.asyncio import tqdm_asyncio

# 🧠 Кодировка: включаем UTF-8 для Windows
if sys.platform.startswith("win"):
    os.system("chcp 65001 >nul")

# ⚙️ Символы: флаг на случай --ascii
USE_ASCII = "--ascii" in sys.argv

def mark(emoji: str, fallback: str = "") -> str:
    return fallback if USE_ASCII else emoji

# 🔐 Telegram API
api_id = 24585917
api_hash = '402600655279206f54d3a32af08d5161'

session = 'session_name'
batch_size = 100

async def main():
    deleted_count = 0
    batch = []

    async with TelegramClient(session, api_id, api_hash) as client:
        me = await client.get_me()
        dialogs = await client.get_dialogs()
        groups = [d for d in dialogs if d.is_group]

        if not groups:
            print(f"{mark('❗','[!]')} Группы не найдены.")
            return

        print(f"\n{mark('📋','[Group List]')} Выбери группу:")
        for i, group in enumerate(groups):
            print(f"{i + 1}. {group.name}")

        try:
            index = int(input(f"\n{mark('📥','>>')} Введите номер группы: ")) - 1
            if not (0 <= index < len(groups)):
                raise ValueError()
        except ValueError:
            print(f"{mark('❌','[X]')} Неверный номер.")
            return

        target_group = groups[index]
        print(f"\n{mark('🔍','>')} Обрабатываю: {target_group.name}")

        # Считаем кол-во сообщений
        print(f"{mark('📦','[~]')} Считаю сообщения...")
        total = 0
        async for message in client.iter_messages(target_group, reverse=True):
            if message.sender_id == me.id:
                total += 1

        if total == 0:
            print(f"{mark('ℹ️','[i]')} В этой группе нет твоих сообщений.")
            return

        confirm = input(f"{mark('⚠️','[!!!]')} Удалить {total} сообщений? (y/n): ").lower()
        if confirm != "y":
            print(f"{mark('🚫','[X]')} Отменено.")
            return

        # Удаление с прогресс-баром
        print(f"{mark('🧹','[deleting]')} Удаление сообщений...")
        async for message in tqdm_asyncio(
            client.iter_messages(target_group, reverse=True), total=total
        ):
            if message.sender_id == me.id:
                batch.append(message.id)
                if len(batch) >= batch_size:
                    try:
                        await client.delete_messages(target_group, batch)
                        deleted_count += len(batch)
                        batch.clear()
                    except Exception as e:
                        print(f"{mark('⚠️','[!]')} Ошибка: {e}")

        if batch:
            try:
                await client.delete_messages(target_group, batch)
                deleted_count += len(batch)
            except Exception as e:
                print(f"{mark('⚠️','[!]')} Финальная ошибка: {e}")

        print(f"\n{mark('✅','[OK]')} Удалено сообщений: {deleted_count} из {total}")

if __name__ == "__main__":
    asyncio.run(main())
