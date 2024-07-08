from app import app

@app.route('/product/add')
def add_product():
    return 'add_product'