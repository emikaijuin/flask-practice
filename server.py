import peeweedbevolve
from flask import Flask, render_template, request, redirect, url_for
from models import *
app = Flask(__name__)

@app.before_request 
def before_request():
  db.connect()

@app.after_request
def after_request(response):
  db.close()
  return response

@app.cli.command()
def migrate():
  db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/stores", methods=["GET","POST"])
def stores():
  if request.method == "POST":
    store = Store.create(name=request.form['name'])
    return redirect(url_for('store', id=store.id))
  else:
    return render_template("store/index.html", stores=Store.select())

@app.route("/stores/new")
def store_new():
  return render_template("store/new.html")

@app.route("/stores/<id>", methods=["GET","POST", "DELETE"])
def store(id):
  store = Store.get(id=id)
  if request.method == "POST":
    store.name = request.form['name']
    store.save()
    return redirect(url_for('store', id = store.id))
  else:
    return render_template('store/show.html', store = store)

@app.route("/stores/<id>/delete", methods=["POST"])
def store_delete(id):
  store = Store.get(id=id)
  store.delete()
  store.save()
  return redirect(url_for('stores'))

# WAREHOUSES

@app.route("/warehouses/new")
def warehouses_new():
  return render_template('warehouse/new.html',stores=Store.select())

@app.route("/warehouses", methods=["GET","POST"])
def warehouses():
  if request.method == "POST":
    warehouse = Warehouse.create(
      location=request.form['location'],
      store=request.form['store']
    )
    return redirect(url_for('warehouse', id=warehouse.id))
  else:
    return render_template('warehouse/index.html',warehouses=Warehouse.select())

@app.route("/warehouses/<id>", methods=["GET","POST"])
def warehouse(id):
  if request.method=="POST":
    return "not done yet"
  else:
    return render_template('warehouse/show.html', warehouse=Warehouse.get(id=id))



if __name__ == 'main':
  app.run()