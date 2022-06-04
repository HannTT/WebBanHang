from decimal import Decimal

from django.conf import settings

from store.models import Product


class Basket():
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    # Thêm và cập nhật dữ liệu giỏ hàng của người dùng
    def add(self, product, qty):
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}
        self.save()

    # Thu thập product_id trong dữ liệu phiên để truy vấn cơ sở dữ liệu và trả lại sản phẩm
    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    # Lấy dữ liệu giỏ hàng và đếm số lượng mặt hàng
    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())

    # Cập nhật số lượng món đồ
    def update(self, product, qty):
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def get_total_price(self):
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

        if subtotal == 0:
            shipping = Decimal(0.000)
        else:
            shipping = Decimal(30.000)

        total = subtotal + Decimal(shipping)
        return total

    # Xóa món đồ
    def delete(self, product):
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    # Xoá toàn bộ món đồ
    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True