from unittest import TestCase

from models import Company, Product, Invoice


class TestProduct(TestCase):
    def test_create_product(self):
        product = Product(
            name="Product 1",
            description="Description 1",
            quantity=2,
            price=100.00,
        )
        self.assertEqual(product.name, "Product 1")
        self.assertEqual(product.description, "Description 1")
        self.assertEqual(product.quantity, 2)
        self.assertEqual(product.price, 100.00)


class TestCompany(TestCase):
    def setUp(self) -> None:
        self.company = Company(
            id="companykey",
            name="Company 1",
            document="123456789",
            address="Address 1",
            products=["product1", "product2"],
        )

    def test_create_company(self):
        self.assertIsNotNone(self.company)

    def test_company_parses_products(self):
        products_data = {
            "product1": {
                "name": "Product 1",
                "description": "Description 1",
                "quantity": 2,
                "price": 100.00,
            },
            "product2": {
                "name": "Product 2",
                "description": "Description 2",
                "quantity": 3,
                "price": 150.00,
            },
        }
        self.company.parse_products(products_data)
        self.assertEqual(self.company.products[0].name, "Product 1")
        self.assertEqual(self.company.products[0].description, "Description 1")
        self.assertEqual(self.company.products[0].quantity, 2)
        self.assertEqual(self.company.products[0].price, 100.00)
        self.assertEqual(self.company.products[1].name, "Product 2")
        self.assertEqual(self.company.products[1].description, "Description 2")
        self.assertEqual(self.company.products[1].quantity, 3)
        self.assertEqual(self.company.products[1].price, 150.00)


class TestInvoice(TestCase):
    def test_create_invoice(self):
        invoice = Invoice(
            id="123456789",
            discount=0.00,
            penalty=0.00,
            due_date="2021-09-30",
            issue_date="2021-09-01",
            bank_account_details={},
            client=Company(),
            company=Company(),
        )
        self.assertIsNotNone(invoice)
