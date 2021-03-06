from app.Resource.SimpleModelResource import SimpleModelResource as SR
from app.Model.Customer import Customer
from app.Model.Address import Address
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


def list_used_customer_codes():
    customers = SR().list_all(Customer)
    used_codes = set([c.customer_code for c in customers])
    return used_codes


def list_unused_customer_codes():
    return customer_codes - list_used_customer_codes()


def list_all_customers():
    customers = SR().list_all(Customer)
    return customers


def get_one_customer(customer_id):
    customer = SR().get_one_by_id(Customer(pk=customer_id))
    return customer


def create_customer(customer, address=None):
    if address is None:
        SR().insert(customer)
    else:
        create_customer_with_address(customer, address)


def update_customer(customer):
    SR().update(customer)


def delete_customer(customer_id):
    SR().delete(Customer(pk=customer_id))


# TODO elegant transaction
def create_customer_with_address(customer, address):
    sr = SR()
    try:
        created_customer = sr.insert(customer, commit=False)
        address.customer_id = created_customer.id
        sr.insert(address, commit=False)
    except Exception as e:
        sr.connection.rollback()
        sr.cursor.close()
        raise e
    else:
        sr.connection.commit()
        sr.cursor.close()


def list_customer_addresses(customer_id):
    SR().get_one_by_id(Customer(pk=customer_id))
    cust_addr = Address()
    cust_addr.customer_id = customer_id
    return SR().find_all(cust_addr)


def create_customer_address(customer_id, address):
    address.customer_id = customer_id
    SR().insert(address)


def delete_address(customer_id, address_id):
    address = SR().find_one(Address({'id': address_id, 'customer_id': customer_id}))
    SR().delete(address)


def get_one_address(customer_id, address_id):
    addr = SR().find_one(Address({'id': address_id, 'customer_id': customer_id}))
    return addr


def update_address(address):
    SR().update(address)
