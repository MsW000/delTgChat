from telethon.sync import TelegramClient
from tqdm import tqdm

# 🔐 Твои данные API
api_id = 24585917
api_hash = '402600655279206f54d3a32af08d5161'

# Счётчики
deleted_count = 0
batch = []

with TelegramClient('session_name', api_id, api_hash) as client:
    me = client.get_me()

    # Выбираем группу
    dialogs = client.get_dialogs()
    groups = [d for d in dialogs if d.is_group]

    if not groups:
        print("❗ Не найдено ни одной группы.")
        exit()

    print("\n📋 Выбери группу:")
    for i, group in enumerate(groups):
        print(f"{i + 1}. {group.name}")

    try:
        index = int(input("\nВведите номер группы: ")) - 1
        if not (0 <= index < len(groups)):
            raise ValueError()
    except ValueError:
        print("❌ Неверный номер.")
        exit()

    target_group = groups[index]
    print(f"\n🔍 Обрабатываю группу: {target_group.name} (ID: {target_group.id})")

    # Считаем количество твоих сообщений
    print("📦 Подсчитываю сообщения...")
    total = sum(1 for m in client.iter_messages(target_group, reverse=True, limit=None)
                if m.sender_id == me.id)

    if total == 0:
        print("ℹ️ В этой группе нет твоих сообщений.")
        exit()

    confirm = input(f"⚠️ Удалить {total} твоих сообщений из «{target_group.name}»? (y/n): ").lower()
    if confirm != "y":
        print("🚫 Отменено.")
        exit()

    # Удаляем с прогресс-баром
    for message in tqdm(client.iter_messages(target_group, reverse=True, limit=None), total=total):
        if message.sender_id == me.id:
            batch.append(message.id)
            if len(batch) >= 100:
                try:
                    client.delete_messages(target_group, batch)
                    deleted_count += len(batch)
                    batch = []
                except Exception as e:
                    print(f"⚠️ Ошибка при удалении: {e}")

    # Удалить остаток
    if batch:
        try:
            client.delete_messages(target_group, batch)
            deleted_count += len(batch)
        except Exception as e:
            print(f"⚠️ Ошибка при финальном удалении: {e}")

    print(f"\n✅ Удалено твоих сообщений: {deleted_count} из {total}")