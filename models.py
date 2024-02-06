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
class Product:
    name: str
    description: str
    quantity: int
    price: decimal.Decimal


@dataclass
class Company:
    id: str
    name: str = ""
    document: str = ""
    address: str = ""
    products: List[Product] | List[str] | None = None

    def parse_products(self, products_data: dict):
        if self.products is not None:
            self.products = [
                Product(
                    name=products_data[p]["name"],
                    description=products_data[p]["description"],
                    quantity=products_data[p]["quantity"],
                    price=products_data[p]["price"],
                )
                for p in self.products
            ]


@dataclass
class Invoice:
    id: uuid.UUID
    total: decimal.Decimal
    sub_total: decimal.Decimal
    discount: decimal.Decimal
    penalty: decimal.Decimal
    due_date: datetime.date
    issue_date: datetime.date
    bank_account_details: dict
    _from: Company
    _to: Company

    @property
    def due_date_str(self):
        return self.due_date.strftime("%d/%m/%Y")

    @property
    def issue_date_str(self):
        return self.issue_date.strftime("%d/%m/%Y")

    @property
    def due_month(self):
        return MONTHS[self.due_date.month]
