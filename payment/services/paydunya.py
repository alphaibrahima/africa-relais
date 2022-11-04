from paydunya import InvoiceItem, Store, Invoice


def get_store():
    infos = {
        "name": "Africarelais",  # Seul le nom est requis
        "tagline": "Africarelais Academy",
        "postal_address": "Sicap Mbao, Extension",
        "phone_number": "763772260",
        "website_url": "https://www.africarelais.com",
        "logo_url": "https://www.africarelais.com/static/img/logo.32b513268679.png",
    }
    store = Store(**infos)
    return store


def get_items(order_items):
    items = [
        InvoiceItem(
            name=item.product.title,
            quantity=item.quantity,
            unit_price=str(item.price),
            total_price=str(item.price * item.quantity),
            description=f"Cours {item.course.title}",
        )
        for item in order_items
    ]
    return items


def get_user_and_product(product_id, user_id):
    user_and_product = [
        ("product_id", product_id),
        ("user_id", user_id),
    ]
    return user_and_product


def get_invoice(items, total_cost, host, custom_data=None):
    store = get_store()
    invoice = Invoice(store)
    invoice.add_items(items)
    invoice.add_custom_data(custom_data)
    invoice.total_amount = int(total_cost)
    invoice.callback_url = f"http://{host}/payment/done/"
    invoice.cancel_url = f"http://{host}/payment/canceled/"
    invoice.return_url = f"http://{host}/payment/done/"
    return invoice.create()


def invoice_confirmation(token):
    store = get_store()
    invoice = Invoice(store)
    return invoice.confirm(token)
