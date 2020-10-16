from app.Resource.SimpleModelResource import SimpleModelResource as SR
from app.Model.Customer import Customer
from app.Util import AuthUtil as authUtil
from app.Model.Product import Product


# Hardcoded for now
customer_codes = {
    'ALLUNEED',
    'THETASMANIANGIFTWR',
    'ABEERGIFTSHOP',
    'ACEFROZENWOODPARK',
    'METCASHLIMITED',
    'TESTDEBTOR',
}


def get_unused_customer_codes():
    customers = SR().get_all(Customer)
    used_codes = set([c.customer_code for c in customers])
    return customer_codes - used_codes


def get_used_customer_codes():
    customers = SR().get_all(Customer)
    used_codes = set([c.customer_code for c in customers])
    return used_codes


def list_all_customers():
    customers = SR().get_all(Customer)
    return customers


def get_one_customer(customer_id):
    customer = SR().get_one_by_id(Customer(pk=customer_id))
    return customer


def create_customer(customer, address=None):
    if address is None:
        SR().create(customer)
    else:
        create_customer_with_address(customer, address)


def delete_customer(customer_id):
    SR().delete(Customer(pk=customer_id))


# TODO elegant transaction
def create_customer_with_address(customer, address):
    sr = SR()
    try:
        created_customer = sr.create(customer, commit=False)
        address.customer_id = created_customer.id
        sr.create(address, commit=False)
    except Exception as e:
        sr.connection.rollback()
        raise e
    else:
        sr.connection.commit()


def get_customer_addresses(customer_id):
    pass


def create_customer_address(customer_id, address):
    address.customer_id = customer_id
    SR().create(address)
