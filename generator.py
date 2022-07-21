import datetime
import os
import uuid
import jinja2

from models import Company, Client, Invoice


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(f'{os.path.dirname(__file__)}/templates/'),
    autoescape=jinja2.select_autoescape()
)
INVOICE = env.get_template('invoice.html')


def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of
    # current month, or said programattically said, the previous day of
    # the first of next month
    return next_month - datetime.timedelta(days=next_month.day)


def generate_facobras_invoice():
    facobras = Client(
        name='FACOBRAS INDUSTRIA E COMERCIO LTDA',
        document='60.691.***/****-14',
        address='Avenida Cachoeira, 667, Barueri/SP'
    )

    vili = Company()

    invoice = Invoice(
        id=uuid.uuid4(),
        total=1000.00,
        sub_total=1000.00,
        discount=0.00,
        penalty=0.00,
        due_date=last_day_of_month(datetime.date.today()),
        issue_date=datetime.date.today()
    )

    content = INVOICE.render(client=facobras, company=vili, invoice=invoice)

    invoice_file = f'{os.path.dirname(__file__)}/invoices/facobras_{datetime.date.today()}_{invoice.id}.html'
    with open(invoice_file, 'a') as file:
        file.write(content)

    return invoice_file


if __name__ == '__main__':
    print('FACOBRAS',
          datetime.date.today(),
          'file:///' + generate_facobras_invoice())
