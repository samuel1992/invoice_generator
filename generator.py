import argparse
import datetime
import json
import os
import uuid

import jinja2
from dateutil import relativedelta

from models import Company, Invoice

TODAY = datetime.date.today()


def last_day_of_month() -> datetime.date:
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = TODAY.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of
    # current month, or said programattically said, the previous day of
    # the first of next month
    return next_month - datetime.timedelta(days=next_month.day)


def next_month_at(day) -> datetime.date:
    next_month = TODAY.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day - int(day))


def specific_date(any_date: str) -> datetime.date:
    return datetime.datetime.strptime(any_date, "%Y-%m-%d").date()


def in_months(months) -> datetime.date:
    return TODAY + relativedelta.relativedelta(months=int(months))


DUE_DATES = {
    "last_day_of_month": last_day_of_month,
    "next_month_at": next_month_at,
    "specific_date": specific_date,
    "in_months": in_months,
}


def _get_due_date_function_and_arg(due_date):
    due_date_function_name = due_date.split("-")
    if len(due_date_function_name) > 1:
        due_date_function = DUE_DATES[due_date_function_name[0]]
        due_date_arg = due_date_function_name[1]
    else:
        due_date_function = DUE_DATES[due_date]
        due_date_arg = None
    return due_date_function, due_date_arg


def _get_due_date(due_date) -> datetime.date:
    due_date_function, due_date_arg = _get_due_date_function_and_arg(due_date)
    return (
        due_date_function(due_date_arg)
        if due_date_arg is not None
        else due_date_function()
    )


def generate_invoice(invoice, template):
    content = template.render(invoice=invoice, client=invoice.client, company=invoice.company)

    invoice_file = (
        f"{os.path.dirname(__file__)}/"
        f"invoices/{invoice.client.id}_{TODAY}_{invoice.due_date}_{invoice.id}.html"
    )
    with open(invoice_file, "a") as file:
        file.write(content)

    return invoice_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", help="The client to generate invoice")
    parser.add_argument("--invoice-number", help="Invoice number")
    parser.add_argument("--template", help="Template for invoice")
    args = parser.parse_args()

    client_name_key = args.client
    invoice_number = args.invoice_number
    template = args.template

    data = json.load(open("data.json", "r"))

    client_data = data.get(client_name_key)
    company_data = data.get("mycompany")
    bank_accounts_data = data.get("bank_accounts")
    products_data = data.get("products")

    if not client_data:
        raise Exception(f"No client {client_name_key} found in our data.json")

    if not company_data:
        raise Exception("No company found in our data.json")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(f"{os.path.dirname(__file__)}/templates/"),
        autoescape=jinja2.select_autoescape(),
    )
    template = env.get_template(template)

    my_company = Company(
        id="mycompany",
        name=company_data["name"],
        document=company_data["document"],
        address=company_data["address"],
    )

    client = Company(
        id=client_name_key,
        name=client_data["name"],
        document=client_data["document"],
        address=client_data["address"],
        products=client_data["products"],
    )
    client.parse_products(products_data)

    invoice = Invoice(
        id=invoice_number or uuid.uuid4(),
        discount=client_data["discount"],
        penalty=client_data["penalty"],
        due_date=_get_due_date(client_data["due_date"]),
        issue_date=TODAY,
        bank_account_details=bank_accounts_data[client_data["remit_to"]],
        company=my_company,
        client=client,
    )

    invoice = generate_invoice(invoice, template)

    print(f"GENERATED INVOICE FOR {client_name_key}", f"file:///{invoice}")
    os.system(f"open -a 'Google Chrome' file:///{invoice}")


if __name__ == "__main__":
    main()
