import re, uuid
from enum import Enum
from datetime import datetime
from pydantic import BaseModel,ConfigDict, Field,field_validator,model_validator
from files.task_3.db import Session

def camel_case(string: str) -> str:
    words = string.split('_')
    return words[0] + ''.join(w.title() for w in words[1:])


class DealType(Enum):
    BUY = "покупка"
    SELL = "продажа"


_PHONE_PATTERN = re.compile(r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$")

def _generate_username() -> str:
    return f"user_{uuid.uuid4().hex[:8]}"

class User(BaseModel):
    model_config = ConfigDict(
        title = "Model User",
        description = "A model for storing users.",
        alias_generator = camel_case,
        populate_by_name=True)

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        title="Идентификатор",
        description="Уникальный идентификатор пользователя.",
    )
    name: str = Field(
        ...,
        title="Имя",
        description="Имя пользователя. Не может быть пустым.",
        min_length=1,
    )
    username: str = Field(
        default_factory=_generate_username,
        title="Никнейм",
        description="Никнейм пользователя. Генерируется автоматически, если не указан.",
    )
    age: int = Field(
        ...,
        title="Возраст",
        description="Возраст пользователя. Должен быть положительным числом.",
        gt=0,
    )
    is_supervisor: bool = Field(
        default=False,
        title="Супервизор",
        description="Флаг: является ли пользователь супервизором.",
    )
    email: str = Field(
        ...,
        title="Email",
        description="Адрес электронной почты пользователя.",
    )
    phone_number: str = Field(
        ...,
        title="Номер телефона",
        description="Номер телефона в формате +7 (000) 000-00-00.",
    )

    

    @field_validator('email')
    def email_is_correct(cls, email):
        if email is None:
            raise ValueError('The email address not specified!')
        
        if '@' not in email:
            raise ValueError('The email address is incorrect!')

        return email

    @field_validator('phone_number')
    def validate_phone_number(cls,value: str) -> str:
        """Проверяет соответствие номера телефона формату +7 (000) 000-00-00."""
        if not _PHONE_PATTERN.match(value):
            raise ValueError(
                "Номер телефона должен соответствовать формату: +7 (000) 000-00-00"
            )
        return value


class Deal(BaseModel):
    model_config = ConfigDict(
        title="Model Deal ",
        description = "The model where user transactions are stored.",
        alias_generator = camel_case,
        populate_by_name=True)

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        title="Идентификатор",
        description="Уникальный идентификатор пользователя.",
    )
    title: str = Field(
        ...,
        title="Название",
        description="Название сделки.",
        min_length=1,
    )
    comment: str = Field(...,
        title="Комментарий",
        description="Произвольный текстовый комментарий к сделке.",
    )
    created_at: datetime = Field(
        ...,
        title="Дата создания",
        description="Дата и время создания сделки. Не может быть раньше сегодняшнего дня.",
    )
    persons_in_charge: list[User] = Field(
        default_factory=list,
        title="Ответственные",
        description="Список пользователей, ответственных за сделку.",
    )
    deal_type: DealType = Field(
        ...,
        title="Тип сделки",
        description="Тип сделки: покупка или продажа.",
    )

    @field_validator('created_at')
    def datetime_is_correct(cls, created_at):
        if created_at <= datetime.today() :
            raise ValueError('The creation date cannot be earlier than the current time.')

        return created_at

