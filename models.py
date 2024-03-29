import datetime
import decimal
import uuid
from dataclasses import dataclass
from typing import List, Optional

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
    id: str = ""
    name: str = ""
    document: str = ""
    address: str = ""


@dataclass
class Invoice:
    id: uuid.UUID
    discount: decimal.Decimal
    penalty: decimal.Decimal
    due_date: datetime.date
    issue_date: datetime.date
    bank_account_details: dict
    company: Company
    client: Company
    products: Optional[List[Product]] = None

    def add_products(self, products_data: List[dict]):
        self.products = [
            Product(
                name=p["name"],
                description=p["description"],
                quantity=p["quantity"],
                price=p["price"],
            )
            for p in products_data
        ]

    @property
    def total(self) -> decimal.Decimal:
        if not self.products:
            raise ValueError("No products added to the invoice")

        return decimal.Decimal(
            sum(p.price * p.quantity for p in self.products)
            - self.discount
            + self.penalty
        )

    @property
    def sub_total(self) -> decimal.Decimal:
        if not self.products:
            raise ValueError("No products added to the invoice")

        return decimal.Decimal(sum(p.price * p.quantity for p in self.products))

    @property
    def due_date_str(self):
        return self.due_date.strftime("%d/%m/%Y")

    @property
    def issue_date_str(self):
        return self.issue_date.strftime("%d/%m/%Y")

    @property
    def due_month(self):
        return MONTHS[self.due_date.month]
