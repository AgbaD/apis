#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

# packages
from flask import *
from flask_login import login_required, current_user
from ..models import Product

# user created
from . import main
from .. import db
from ..models import User, product_categories

# inbuilt
from datetime import datetime


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pass
    products = Product.query.all()
    now = datetime.utcnow()
    prod_time = {}
    for product in products:
        # get time difference between now and when product was created
        pass

    # get the best selling categories
    
    # return render_template('index.html')


@main.route("/get_all_products")
def get_all_products():
    products = Product.query.all()
    return render_template("all_products.html", products=products,
                           categories=product_categories)


@main.route("/all_products/<category>")
def get_category(category):
    products = []
    all_products = Product.query.all()
    for product in all_products:
        if product.category == category:
            products.append(product)
    return render_template("category.html", products=products,
                           category=category)


@main.route("/all_products/<product>/<short_des>")
def get_product(product, short_des):
    products = Product.query.filter_by(name=product).all()
    for product in products:
        if product.short_description == short_des:
            return render_template('product.html', product=product)
        else:   # should not happen
            return redirect(url_for("internal_server_error"))
