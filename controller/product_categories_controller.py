from app import app

@app.route('/category/addnew')
def CategoryAddNew():
    return 'new category'