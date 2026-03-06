from __future__ import annotations

from typing import Any, Dict, List, Optional, Type

from config.config import settings

# Дескриптор для защиты хранилища
class _StoreDescriptor:

    def __set_name__(self, owner: Type, name: str) -> None:
        self._private_name = f"_{name}_data"

    def __get__(self, obj: Any, objtype: Any = None) -> Optional[Dict[str, Any]]:
        if obj is None:
            return None
        return getattr(obj, self._private_name, None)

    def __set__(self, obj: Any, value: Optional[Dict[str, Any]]) -> None:
        setattr(obj, self._private_name, value)

    def __delete__(self, obj: Any) -> None:
        setattr(obj, self._private_name, None)


# Singleton: хранилище сделок 
class DealsStore:

    _instance: Optional["DealsStore"] = None

    # Защищённый дескриптором атрибут хранилища
    _store = _StoreDescriptor()

    def __new__(cls) -> "DealsStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._store = {}   # инициализируем пустым словарём
        return cls._instance

    def get_store(self) -> Dict[str, Any]:
        """Возвращает текущее содержимое хранилища."""
        return self._store or {}

    def set_store_data(self, key: str, value: Any) -> None:
        """Добавляет или обновляет запись в хранилище по ключу."""
        store = self._store or {}
        store[key] = value
        self._store = store

    def delete_from_store(self, key: str) -> None:
        """Удаляет запись из хранилища по ключу."""
        store = self._store or {}
        store.pop(key, None)
        self._store = store


# Контекстный менеджер: имитация подключения к БД 
class DatabaseContextManager:
    def __init__(self) -> None:
        self._db_url: str = settings.database_url
        self._store: Optional[DealsStore] = None

    def __enter__(self) -> DealsStore:
        self._store = DealsStore()
        print(f"\n[DB] Адрес подключения: {self._db_url}")
        print("[DB] ✅ Соединение с базой данных установлено. Добро пожаловать!")
        return self._store

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> bool:
        print(f"\n[DB] Адрес подключения: {self._db_url}")
        print("[DB] 🔌 Соединение с базой данных закрыто. До свидания!")
        return False   # не подавляем исключения