# utils.py
import csv
from models import db, Product
from datetime import datetime

def load_initial_data():
    if Product.query.count() == 0:
        try:
            with open('data/products.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    product = Product(
                        name=row['name'],
                        strength=row['strength'],
                        company=row['company'],
                        salt=row['salt'],
                        uses=row['uses'],
                        type=row['type'],
                        batch_id=row['batch_id'],
                        pack_price=float(row['pack_price']),
                        packs_quantity=int(row['packs_quantity']),
                        units_per_pack=int(row['units_per_pack']),
                        expiry_date=datetime.strptime(row['expiry_date'], '%Y-%m-%d').date()
                    )
                    db.session.add(product)
                db.session.commit()
                print("Successfully loaded initial products")
        except Exception as e:
            print(f"Error loading products: {str(e)}")
