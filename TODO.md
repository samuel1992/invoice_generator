# INVOICE GENERATOR

A simple system to create invoices to charge your clients.

## REQUIREMENTS

- the system should be able to configure bank account data
- the system should be able to configure invoice data like: document, address, bank account data, due date
- the system should be able to configure clients with: document, address, payment date
- the system should be able to gerenate invoices in pdf format
- the system should provide an report with invoices sent
- the system should provide a button on each invoice to mark it as paid
- the system should send via email the invoice for the configured clients 10 days before the invoice due

## ENTITIES

- invoice
- client
- bank_account

## SERVICES

- invoice_pdf_generator
- invoice_sender
