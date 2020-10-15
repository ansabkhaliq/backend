from app.Model.Address import Address
from app.Model.Customer import Customer
from app.Service import CustomerService as cs
from app.Service.ProductService import retrieve_products as sync_products
from .exceptions import LackRequiredData
from app.Util.validation import lack_keys
from app.Util import AuthUtil as authUtil
from flask import (
    Blueprint,
    redirect,
    request,
    jsonify,
    url_for
)

cust = Blueprint('customer', __name__)


# TODO auth decorator (make session validation a decorator)
@cust.route('/api/switch_customer', methods=['POST'])
def switch_customer():
    data = request.get_json()
    # Check necessary keys
    required = ['customer_code']
    lacked = lack_keys(data, required)

    if lacked:
        raise LackRequiredData(lacked)

    cust_code = data.get('customer_code')
    if cust_code is None:
        raise LackRequiredData('customer_code')

    if cust_code not in cs.customer_codes:
        return {'message': f'Provided customer code {cust_code} does not exist'}, 404

    if cust_code not in cs.get_used_customer_codes():
        return {'message': f'Provided customer code {cust_code} does not match any customer'}, 404

    # TODO this is a problematic function, to be fixed
    sync_products(customer_code=cust_code)
    return {'message': 'Switch customer successfully'}, 200


@cust.route('/api/customers', methods=['GET', 'POST'])
def customers():
    # Create a customer
    if request.method == 'POST':
        data = request.get_json()
        cust_data = data.get('customer')
        addr_data = data.get('address')

        # Check customer necessary keys
        cust_required = ['customer_code', 'title', 'first_name', 'last_name']
        cust_lacked = lack_keys(cust_data, cust_required)

        if cust_lacked:
            raise LackRequiredData(cust_lacked)
        # Check customer_code
        cust_code = cust_data['customer_code']
        if cust_code not in cs.customer_codes:
            return jsonify({'message': f'Provided customer code {cust_code} does not exist'}), 404

        if cust_code not in cs.get_unused_customer_codes():
            return jsonify({'message': f'Provided customer code {cust_code} is already used'}), 409

        new_customer = Customer(cust_data)

        # Create customer only
        if addr_data is None:
            cs.create_customer(new_customer)
            return {"customer": new_customer.__dict__}, 201

        # Create customer with address
        addr_data = data['address']
        addr_required = ['contact', 'address_line1', 'address_line2', 'postcode', 'country']
        addr_lacked = lack_keys(addr_data, addr_required)
        if addr_lacked:
            raise LackRequiredData(addr_lacked)

        new_address = Address(addr_data)
        cs.create_customer(new_customer, new_address)
        return {'customer': new_customer.__dict__, 'address': new_address.__dict__}, 201

    # Get customers list
    elif request.method == 'GET':
        all_customers = cs.list_all_customers()
        return jsonify([c.__dict__ for c in all_customers]), 200


@cust.route('/api/customer/<customer_id>', methods=['GET', 'DELETE'])
def customer(customer_id):
    # Get specific customer
    if request.method == 'GET':
        return cs.get_one_customer(customer_id).__dict__, 200

    # Delete specific customer
    if request.method == 'DELETE':
        cs.delete_customer(customer_id)
        return {'message': f'Customer {customer_id} deleted'}, 200


@cust.route('/api/customer_codes', methods=['GET'])
def customers_codes():
    return cs.get_unused_customer_codes(), 200


@cust.route('/api/customer/<customer_id>/addresses', methods=['GET', 'POST'])
def customers_addresses(customer_id):
    return {}, 200
