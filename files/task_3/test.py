from .schemas import Deal
from .db import DatabaseContextManager, DealsStore
from .repository import DealsRepository
from .const import DEALS_DATA


def run_deals_tests() -> None:
    db_manager = DatabaseContextManager()
    repo = DealsRepository(deal_model=Deal, db_manager=db_manager)
    #  1. Создание сделок (одна некорректная) 
    print("Создание сделок ─")
    repo.create_deal(*DEALS_DATA)
    #  2. Получение всех сделок (Pydantic-схемы) 
    print(" Все сделки (Pydantic) ─")
    deals = repo.get_deals()
    for deal in deals:
        print(f"  id={deal.id}  title='{deal.title}'  type={deal.deal_type.value}")
    # 3. Получение всех сделок (словари)
    print(" Все сделки (словари) ─")
    dicts = repo.get_deals_dicts()
    for d in dicts:
        print(f"  {d}")
    #4. Получение одной сделки 
    if deals:
        first_id = deals[0].id
        print(f" Получить сделку id={first_id} ─")
        single = repo.get_deal(first_id)
        if single:
            print(f"  Найдена: '{single.title}'")

    #  5. Обновление сделки 
    if deals:
        first_id = deals[0].id
        print(f" Обновить сделку id={first_id} ─")
        updated = repo.update_deal(
            deal_id=first_id,
            deal_data={"comment": "Комментарий обновлён в ходе теста."},
        )
        if updated:
            print(f"  Обновлённый комментарий: '{updated.comment}'")

    #  6. Обновление пользователя внутри сделки 
    if deals:
        first_deal = deals[0]
        if first_deal.persons_in_charge:
            user_id = first_deal.persons_in_charge[0].id
            print(f"Обновить пользователя id={user_id} в сделке ─")
            updated = repo.update_deal(
                deal_id=first_deal.id,
                user_id=user_id,
                user_data={"is_supervisor": False},
            )
            if updated:
                for p in updated.persons_in_charge:
                    if p.id == user_id:
                        print(f"  Пользователь '{p.name}' — is_supervisor={p.is_supervisor}")

    #  7. Удаление сделки 
    if deals:
        last_id = deals[-1].id
        print(f"Удалить сделку id={last_id} ─")
        repo.delete_deal(last_id)
        print(f"  Сделок после удаления: {len(repo.get_deals())}")


