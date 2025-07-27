from flask import Flask
from flask_cors import CORS
from backend.routes.auth_routes import auth_bp, bcrypt
from backend.routes.product_routes import product_bp
from backend.routes.category_routes import category_bp
from backend.routes.seller_routes import seller_bp
from backend.routes.promo_routes import promo_bp
from backend.routes.user_routes import user_bp 

app = Flask(__name__)
CORS(app)
bcrypt.init_app(app)

# 注册所有 blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(product_bp)
app.register_blueprint(category_bp)
app.register_blueprint(seller_bp)
app.register_blueprint(promo_bp)
app.register_blueprint(user_bp) 

@app.route('/')
def home():
    return "Flask backend is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
