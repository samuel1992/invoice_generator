# Invoice Generator

This script automates the creation of invoices from JSON data using a specified Jinja2 template. It is designed to handle different due date calculations and render the invoice to an HTML file.

## Features

- Generate invoices as HTML files.
- Use Jinja2 templates for invoice layout.
- Calculate due dates based on various criteria (last day of the month, specific date, etc.).
- Load client and company data from a JSON file.

## Prerequisites

Before running the script, ensure you have the following prerequisites installed:

- Python 3.x
- Jinja2
- python-dateutil

You can install the required Python packages using pip:

```sh
pip install Jinja2 python-dateutil
```

## Usage

1. **Prepare Your Data**: Ensure your `data.json` contains the necessary information about clients, your company, bank accounts, and products.

2. **Choose or Create a Template**: Prepare a Jinja2 template for your invoice layout. Place this template in the `templates` directory. (templates are locate in templates/ folder)

3. **Generate an Invoice**: Run the script with the required arguments:

```sh
python generate_invoice.py generate-invoice --client CLIENT_KEY --invoice-number INVOICE_NUMBER --template TEMPLATE_NAME.html --products 'PRODUCT1 QUANTITY,PRODUCT2 QUANTITY,PRODUCT3 QUANTITY'
# if you dont use invoice-number it will generate a uuid as the invoice identifier
```

- `CLIENT_KEY`: The key for the client's data in `data.json`.
- `INVOICE_NUMBER`: Unique identifier for the invoice. If omitted, a UUID will be generated.
- `TEMPLATE_NAME.html`: Name of the Jinja2 template file to use.
- `PRODUCT1 QUANTITY...`.: List of products and their quantities to include in the invoice.

The script will generate an HTML file for the invoice and open it in Google Chrome.

## Arguments

- `--client`: Specifies the client for which to generate an invoice. This should match a key in `data.json`.
- `--invoice-number`: (Optional) Specifies the invoice number. If not provided, a UUID will be generated.
- `--template`: The Jinja2 template file to use for generating the invoice.

## Other Commands
You can also use the following commands:
- `list-clients`: List all clients available in the `data.json` file.
- `list-products`: List all products available in the `data.json` file.
- `list-invoices`: List all invoices available in the `invoices` directory.
- `open-invoice`: Open an invoice in chrome. You need to provide the invoice file name as an argument `--invoice`. Ex: `python generate_invoice.py open-invoice --invoice INVOICE_FILE_NAME.html`

```sh

## Data Format

Your `data.json` should follow this structure:

```json
{
  "mycompany": {
    "name": "Your Company Name",
    "document": "Your Company Document",
    "address": "Your Company Address"
  },
  "bank_accounts": {
    "account_details": "Your Bank Account Details"
  },
  "products": {
    "product1": {
      "name": "Product Name",
      "price": 100
    }
  },
  "client_key": {
    "name": "Client Name",
    "document": "Client Document",
    "address": "Client Address",
    "products": ["product1"],
    "discount": 10,
    "penalty": 5,
    "due_date": "specific_date-YYYY-MM-DD",
    "remit_to": "account_details"
  }
}
```

Replace placeholders with actual data for your company, bank accounts, products, and clients.

## Customizing the Template

The Jinja2 template should be designed to accept the invoice, client, and company objects passed to it. Customize your template to fit the layout you desire for your invoices.
