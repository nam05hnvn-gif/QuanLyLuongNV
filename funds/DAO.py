from django.db import connection, transaction
from random import randint

def _dict_from_cursor(cursor):
    cols = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    return [dict(zip(cols, row)) for row in rows]


def list_funds():
    try:
        with connection.cursor() as cur:
            cur.execute('''
                SELECT * FROM fund
                ORDER BY fund_id ASC
            ''')
            return _dict_from_cursor(cur)
    except Exception as e:
        return {"error" : str(e)}
    
def get_fund_by_id(fund_id):
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM fund WHERE fund_id = %s", [fund_id])
            row = cur.fetchone()
            if row:
                return dict(zip([col[0] for col in cur.description], row))
            return None
    except Exception as e:
        return {"error": str(e)}


def add_fund(data):
    fund_id = int(data.get('fund_id'))
    fund_amount = float(data.get('fund_amount', 0))

    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) FROM fund WHERE fund_id = %s",
                    [fund_id]
                )
                exists = cur.fetchone()[0]

                if exists > 0:
                    return {"message": "Fund ID already exists."}
                
                cur.execute(
                    "INSERT INTO fund (fund_id, fund_amount) VALUES (%s, %s)",
                    [fund_id, fund_amount]
                )

        return {"message": "Fund added successfully."}

    except Exception as e:
        return {"error": str(e)}



def change_fund(data):
    while True:
        transaction_id = randint(1, 999999)
        with connection.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM fundtransaction WHERE transaction_id = %s",
                [transaction_id]
            )
            exists = cur.fetchone()[0]
            if exists == 0:
                break
    fund_id = int(data.get('fund_id'))
    admin_id = int(data.get('admin_id'))
    with connection.cursor() as cur:
        old_amount = 0
        cur.execute(
            "SELECT fund_amount FROM fund WHERE fund_id = %s",
            [fund_id]
        )
        row = cur.fetchone()
        if row:
            old_amount = row[0]
    transaction_type = data.get('transaction_type')
    if transaction_type == 'rut':
        new_amount = float(old_amount) - data.get('amount')
    else:
        new_amount = float(old_amount) + data.get('amount')
    transaction_date = data.get('transaction_date')
    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute(
                    "UPDATE fund SET fund_amount = %s WHERE fund_id = %s",
                    [new_amount, fund_id]
                )
                if cur.rowcount == 0:
                    return {"message": "Fund not found."}
                cur.execute(
                    "INSERT INTO fundtransaction (transaction_id, fund_id, admin_id, old_amount, new_amount, transaction_date) VALUES (%s, %s, %s, %s, %s, %s)",
                    [transaction_id, fund_id, admin_id, old_amount, new_amount, transaction_date]
                )
        return {"message": "Fund updated successfully."}
    except Exception as e:
        return {"error": str(e)}


def delete_fund(data):
    fund_id = data.get('fund_id')
    try:
        with transaction.atomic():
            with connection.cursor() as cur:
                cur.execute("DELETE FROM fundtransaction WHERE fund_id = %s",[fund_id])
                cur.execute("DELETE FROM fund WHERE fund_id = %s", [fund_id])
                return {"message": "Fund deleted successfully."}
    except Exception as e:
        return {"error": str(e)}


def list_transactions():
    try:
        with connection.cursor() as cur:
            cur.execute('''
                SELECT * FROM fundtransaction
                ORDER BY transaction_date DESC
            ''')
            return _dict_from_cursor(cur)

    except Exception as e:
        return {"error": str(e)}