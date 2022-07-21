import datetime
import os
import uuid
import jinja2
import json
import argparse

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


DUE_DATES = {
    'last_day_of_month': last_day_of_month
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
    invoice = Invoice(
        id=uuid.uuid4(),
        total=client_data['invoice_data']['total'],
        sub_total=client_data['invoice_data']['sub_total'],
        discount=client_data['invoice_data']['discount'],
        penalty=client_data['invoice_data']['penalty'],
        due_date=due_date_function(today),
        issue_date=today
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

    print(f'{client_name}',
          f'file:///{generate_invoice(client_name, client_data)}')


if __name__ == '__main__':
    main()
