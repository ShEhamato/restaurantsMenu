from flask import Flask, render_template, url_for, request, redirect
from database_setup import Restaurant
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.route('/')
@app.route('/restaurants')
def listRestaurants():
    session = DBSession()
    restaurants= session.query(Restaurant)
    return render_template('restaurants.html', restaurants= restaurants)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def createNewRestaurant(): 
    if request.method=='POST':
        session = DBSession()
        newRestaurant= Restaurant(name= request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('listRestaurants'))
    else :
        return render_template('createNewRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'] )
def editRestaurant(restaurant_id):
    session = DBSession()
    restaurantToedit=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        if request.form['name']:
            restaurantToedit.name=request.form['name']
        session.add(restaurantToedit)
        session.commit()
        return redirect(url_for('listRestaurants'))
    else :
        return render_template('editRestaurant.html', restaurant = restaurantToedit)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    session = DBSession()
    restaurantTodelete= session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        session.delete(restaurantTodelete)
        session.commit()
        return redirect(url_for('listRestaurants'))
    else :
        return render_template('deleteRestaurant.html', restaurant= restaurantTodelete)


@app.route('/restaurants/<int:restaurant_id>/menu')
def showRestaurantMenu(restaurant_id):
    session = DBSession()
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items= session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('restaurantMenu.html', restaurant = restaurant, items=items )

@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def createNewMenuItem(restaurant_id):
    if request.method=='POST':
        session = DBSession()
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showRestaurantMenu', restaurant_id=restaurant_id ))
    else:
        return render_template('createNewMenuItem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    session = DBSession()
    itemToedit=session.query(MenuItem).filter_by(id=item_id).one()
    if request.method=='POST':
        if request.method=='POST':
            if request.form['name']:
                itemToedit.name=request.form['name']
            session.add(itemToedit)
            session.commit()
            return redirect(url_for('showRestaurantMenu', restaurant_id=restaurant_id ))
    else:
        return render_template('editOneMenuItem.html', restaurant_id=restaurant_id, item= itemToedit)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
    session = DBSession()
    itemToDelete=session.query(MenuItem).filter_by(id=item_id).one()
    if request.method=='POST':
        session.delete(itemToDelete)
        return redirect(url_for('showRestaurantMenu', restaurant_id=restaurant_id ))
    else:
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, item= itemToDelete)




if __name__== '__main__' :
    app.debug= True
    app.run(host = '0.0.0.0', port= 5000)