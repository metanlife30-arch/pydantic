from datetime import datetime

# ── Корректный пользователь 1 ──────────────────────────────────────────────
USER_1 = {
    "name": "Алексей Иванов",
    "username": "alex_ivanov",
    "age": 35,
    "is_supervisor": True,
    "email": "alex.ivanov@example.com",
    "phone_number": "+7 (916) 123-45-67",
}

# ── Корректный пользователь 2 ──────────────────────────────────────────────
USER_2 = {
    "name": "Мария Петрова",
    "age": 28,
    # username не указан — будет сгенерирован автоматически
    "is_supervisor": False,
    "email": "m.petrova@company.ru",
    "phone_number": "+7 (495) 999-00-11",
}

# ── Данные сделок ──────────────────────────────────────────────────────────
DEALS_DATA = [
    # Сделка 1 — корректные данные
    {
        "title": "Покупка офисного здания",
        "comment": "Приоритетная сделка квартала.",
        "created_at": datetime.now(),
        "persons_in_charge": [USER_1, USER_2],
        "deal_type": "покупка",
    },
    # Сделка 2 — корректные данные
    {
        "title": "Продажа склада в Подмосковье",
        "comment": None,
        "created_at": datetime.now(),
        "persons_in_charge": [USER_1],
        "deal_type": "продажа",
    },
    # Сделка 3 — НЕКОРРЕКТНЫЕ ДАННЫЕ (вызовет ValidationError):
    #   • created_at в прошлом
    #   • email невалидный
    #   • phone_number не соответствует формату
    {
        "title": "Сделка с ошибками",
        "comment": "Эта сделка не должна быть создана.",
        "created_at": datetime(2020, 1, 1),          # дата в прошлом — ошибка
        "persons_in_charge": [
            {
                "name": "Ошибочный Юзер",
                "age": -5,                            # отрицательный возраст — ошибка
                "email": "not-an-email",              # невалидный email — ошибка
                "phone_number": "89161234567",        # неверный формат — ошибка
            }
        ],
        "deal_type": "покупка",
    },
]
