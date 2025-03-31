from recommendation_app.models import Customer

class CustomerAgent:
    def __init__(self, customer_id):
        self.customer = Customer.objects.get(customer_id=customer_id)

    def get_customer(self):
        return self.customer

def run_customer_analysis(customer_id):
    agent = CustomerAgent(customer_id)
    return agent.get_customer()
