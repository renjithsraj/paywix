from paywix.models import PaywixData


def save_db(data, transaction):
    if transaction == 'init':
        transaction = PaywixData.objects.create(
            transaction_id=data['txnid'],
            pg_type=data['pg_type'],
            txn_amount=data['amount'],
            txn_status="IN",
            request_data=data
        )
    else:
        print(data, transaction)
