from app.Model.Model import Model


class Customer(Model):
    def __init__(self, json):
        self.id = None
        self.customer_id = None
        self.customer_code = None
        self.first_name = None
        self.last_name = None
        self.phone = None
        self.email = None
        self.nationality_code = None
        super().__init__(json)

    @staticmethod
    def get_table_name():
        return 'customers'
