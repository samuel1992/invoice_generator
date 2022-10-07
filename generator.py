import datetime
import os
import uuid
import jinja2
import json
import argparse

from models import Company, Client, Invoice, Product


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


def next_month_fifth(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day - 5)


DUE_DATES = {
    'last_day_of_month': last_day_of_month,
    'next_month_fifth': next_month_fifth,
    # 'specified_bunisess_day': business_day
}


def generate_invoice(client_name, client_data):
    vili = Company()

    facobras = Client(
        name=client_data['name'],
        document=client_data['document'],
        address=client_data['address']
    )

    due_date_function = DUE_DATES[client_data['invoice_data']['due_date']]
    today = datetime.date.today()
    total = sum(i['total'] for i in client_data['invoice_data']['products'])
    sub_total = sum(
        i['sub_total'] for i in client_data['invoice_data']['products']
    )
    discount = sum(
        i['discount'] for i in client_data['invoice_data']['products']
    )
    penalty = sum(
        i['penalty'] for i in client_data['invoice_data']['products']
    )
    products = [Product(name=i['name'], total=i['total']) for i in
                client_data['invoice_data']['products']]
    invoice = Invoice(
        id=uuid.uuid4(),
        total=total,
        sub_total=sub_total,
        discount=discount,
        penalty=penalty,
        due_date=due_date_function(today),
        issue_date=today,
        products=products
    )

    content = INVOICE.render(client=facobras, company=vili, invoice=invoice)

    invoice_file = (
        f'{os.path.dirname(__file__)}/'
        f'invoices/{client_name}_{today}_{invoice.id}.html'
    )
    with open(invoice_file, 'a') as file:
        file.write(content)

    return invoice_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client-name', help='The client to generate invoice')
    args = parser.parse_args()

    client_name = args.client_name
    data = json.load(open('data.json', 'r'))
    client_data = data.get(client_name)
    if not client_data:
        raise Exception(f'No client {client_name} found in our data.json')

    invoice = generate_invoice(client_name, client_data)
    print(f'{client_name}', f'file:///{invoice}')


if __name__ == '__main__':
    main()
