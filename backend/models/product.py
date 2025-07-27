import uuid

class Product:
    def __init__(self, name, category, price, stock, image_url, seller_id, description=""):
        self.id = str(uuid.uuid4())  # 自动生成唯一 ID
        self.name = name
        self.category = category  # 分类，比如 'food', 'toy', 'accessory' 等
        self.price = price
        self.stock = stock
        self.image_url = image_url
        self.seller_id = seller_id
        self.description = description  # 可选：商品描述

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "image_url": self.image_url,
            "seller_id": self.seller_id,
            "description": self.description,
        }
