from app import create_app
from app.shop_methods import seed_items

app = create_app()


with app.app_context():
    seed_items()

if __name__ == "__main__":
    app.run(debug=True)
