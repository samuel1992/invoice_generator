import datetime
import decimal
import uuid
from dataclasses import dataclass
from typing import List

MONTHS = (
    "",
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
)


@dataclass
class Company:
    name: str = ""
    document: str = ""
    address: str = ""


@dataclass
class Product:
    name: str
    description: str
    quantity: int
    price: decimal.Decimal


@dataclass
class Invoice:
    id: uuid.UUID
    total: decimal.Decimal
    sub_total: decimal.Decimal
    discount: decimal.Decimal
    penalty: decimal.Decimal
    due_date: datetime.date
    issue_date: datetime.date
    products: List[Product]

    @property
    def due_date_str(self):
        return self.due_date.strftime("%d/%m/%Y")

    @property
    def issue_date_str(self):
        return self.issue_date.strftime("%d/%m/%Y")

    @property
    def due_month(self):
        return MONTHS[self.due_date.month]


@dataclass
class Client:
    name: str
    document: str
    address: str
