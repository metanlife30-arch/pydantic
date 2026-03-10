from __future__ import annotations
from typing import Any, Dict, List, Optional, Type
from uuid import UUID
from pydantic import ValidationError
from .schemas import Deal
from .db import DatabaseContextManager

#Репозиторий для работы со сделками
class DealsRepository:

    def __init__(
        self,
        deal_model: Type[Deal],
        db_manager: DatabaseContextManager,
    ) -> None:
        self.__deal_model: Optional[Type[Deal]] = None
        self.__db_manager: DatabaseContextManager = db_manager
        # Используем сеттер — он проверяет однократность установки
        self.deal_model = deal_model

    #  Геттер / сеттер / делиттер для __deal_model
    @property
    def deal_model(self) -> Optional[Type[Deal]]:
        """Возвращает текущую Pydantic-модель сделки."""
        return self.__deal_model

    @deal_model.setter
    def deal_model(self, model: Type[Deal]) -> None:
        """Устанавливает модель сделки."""
        if self.__deal_model is not None:
            raise AttributeError(
                "Модель сделки уже установлена и не может быть заменена другой моделью."
            )
        self.__deal_model = model

    @deal_model.deleter
    def deal_model(self) -> None:
        """Сбрасывает модель сделки (устанавливает None)."""
        print("[DealsRepository] Модель сделки удалена.")
        self.__deal_model = None

    #  CRUD-методы 

    def create_deal(self, *deals_data: Dict[str, Any]) -> None:
        """Создаёт одну или несколько сделок и сохраняет их в хранилище."""
        errors: List[str] = []

        with self.__db_manager as store:
            for idx, data in enumerate(deals_data):
                try:
                    deal: Deal = self.__deal_model(**data)  # type: ignore[misc]
                    store.set_store_data(str(deal.id), deal.model_dump())
                    print(f"[create_deal] Сделка '{deal.title}' (id={deal.id}) успешно создана.")
                except ValidationError as exc:
                    errors.append(
                        f"  • Сделка #{idx + 1} (данные: {data})\n    {exc}"
                    )
                except Exception as exc:
                    errors.append(f"  • Сделка #{idx + 1}: непредвиденная ошибка — {exc}")

        if errors:
            print("\n[create_deal] ⚠️  Ошибки при создании следующих сделок:")
            for err in errors:
                print(err)

    def get_deals(self) -> List[Deal]:
        """Возвращает все сделки как список Pydantic-схем Deal."""
        with self.__db_manager as store:
            raw_store = store.get_store()
            return [self.__deal_model(**v) for v in raw_store.values()]  # type: ignore[misc]

    def get_deals_dicts(self) -> List[Dict[str, Any]]:
        """Возвращает все сделки как список словарей."""
        with self.__db_manager as store:
            return list(store.get_store().values())

    def get_deal(self, deal_id: UUID) -> Optional[Deal]:
        """Возвращает одну сделку по её UUID или None, если не найдена."""
        with self.__db_manager as store:
            raw = store.get_store().get(str(deal_id))
            if raw is None:
                print(f"[get_deal] Сделка с id={deal_id} не найдена.")
                return None
            return self.__deal_model(**raw)  # type: ignore[misc]

    def delete_deal(self, deal_id: UUID) -> bool:
        """Удаляет сделку по UUID."""
        with self.__db_manager as store:
            raw = store.get_store().get(str(deal_id))
            if raw is None:
                print(f"[delete_deal] Сделка с id={deal_id} не найдена.")
                return False
            store.delete_from_store(str(deal_id))
            print(f"[delete_deal] Сделка с id={deal_id} удалена.")
            return True

    def update_deal(
        self,
        deal_id: UUID,
        deal_data: Optional[Dict[str, Any]] = None,
        user_id: Optional[UUID] = None,
        user_data: Optional[Dict[str, Any]] = None,
    ) -> Optional[Deal]:
        """
        Обновляет сделку ИЛИ данные пользователя, связанного со сделкой.

        Args:
            deal_id:    UUID сделки для обновления.
            deal_data:  Словарь с новыми данными сделки (опционально).
            user_id:    UUID пользователя внутри сделки (опционально).
            user_data:  Новые данные пользователя (опционально, требует user_id).

        Returns:
            Обновлённая сделка или None, если сделка не найдена.
        """
        with self.__db_manager as store:
            raw = store.get_store().get(str(deal_id))
            if raw is None:
                print(f"[update_deal] Сделка с id={deal_id} не найдена.")
                return None

            # Обновляем поля самой сделки
            if deal_data:
                raw.update(deal_data)

            # Обновляем пользователя внутри сделки
            if user_id is not None and user_data is not None:
                persons = raw.get("persons_in_charge", [])
                updated_persons = []
                for person in persons:
                    if str(person.get("id")) == str(user_id):
                        person.update(user_data)
                    updated_persons.append(person)
                raw["persons_in_charge"] = updated_persons

            try:
                updated_deal: Deal = self.__deal_model(**raw)  # type: ignore[misc]
                store.set_store_data(str(deal_id), updated_deal.model_dump())
                print(f"[update_deal] Сделка с id={deal_id} обновлена.")
                return updated_deal
            except ValidationError as exc:
                print(f"[update_deal] Ошибка валидации при обновлении сделки:\n{exc}")
                return None
