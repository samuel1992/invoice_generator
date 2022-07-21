import datetime
import decimal
import uuid

from dataclasses import dataclass

MONTHS = (
    '',
    'Janeiro',
    'Fevereiro',
    'Março',
    'Abril',
    'Maio',
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro'
)


@dataclass
class Company:
    name: str = 'VILI TECNOLOGIA LTDA'
    document: str = '24.935.528/0001-10'
    address: str = 'R CARMEM MIRANDA, Carapicuíba/SP, 06395420'


@dataclass
class Invoice:
    id: uuid.UUID
    total: decimal
    sub_total: decimal
    discount: decimal
    penalty: decimal
    due_date: datetime.date
    issue_date: datetime.date

    @property
    def due_date_str(self):
        return '10/07/2022'
        # return self.due_date.strftime("%d/%m/%Y")

    @property
    def issue_date_str(self):
        return self.issue_date.strftime("%d/%m/%Y")

    @property
    def due_month(self):
        return 'Maio'
        #return MONTHS[self.due_date.month]


@dataclass
class Client:
    name: str
    document: str
    address: str
