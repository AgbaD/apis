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
        query = request.form.get("query")
        products = Product.query.all()
        searched_products = []
        for product in products:
            if product.name == query:
                searched_products.append(product)
            for tag in product.tags:
                if tag == query:
                    if product not in searched_products:
                        searched_products.append(product)
                    break
        return render_template(url_for("search.html", products=searched_products))
    products = Product.query.all()

    # new arrivals
    now = datetime.utcnow()
    prod_time = {}
    times = []
    new_products = []
    for product in products:
        # get time difference between now and when product was created
        pass_time = now - product.created_on
        prod_time[pass_time] = product
        times.append(pass_time)
    while len(new_products) < 4:
        v = min(times)
        if prod_time[v] not in new_products:
            new_products.append(prod_time[v])
        times.remove(v)

    # get the top categories based on quantity
    top_categories = []
    qty = [v for v in product_categories.values()]
    qty_sorted = sorted(qty)
    i = 1
    while len(top_categories) < 4:
        for k, v in product_categories.items():
            if v == qty_sorted[-i]:
                top_categories.append(k)
                if len(top_categories) >= 4:
                    break
        while qty_sorted[-i] == qty_sorted[-(i+1)]:
            del(qty_sorted[-i])
        i += 1

    # best sellers
    best_sellers = []
    best_products = {product.purchases: product for product in products}
    while len(best_sellers) < 4:
        prod = max(best_products)
        best_sellers.append(best_products[prod])
        del[best_products[prod]]

    return render_template('index.html', top_categories=top_categories,
                           new_products=new_products, best_sellers=best_sellers)


@main.route("/get_all_products")
def get_all_products():
    products = Product.query.all()
    return render_template("all_products.html", products=products,
                           categories=product_categories)


@main.route("/all_products/<category>")
def get_category(category):
    all_products = Product.query.all()
    products = [product for product in all_products if product.category == category]
    """for product in all_products:
        if product.category == category:
            products.append(product)"""
    return render_template("category.html", products=products,
                           category=category)


@main.route("/all_products/<product>/<short_des>")
def get_product(product, short_des):
    products = Product.query.filter_by(name=product).all()
    try:
        for product in products:
            if product.short_description == short_des:
                return render_template('product.html', product=product)
        return redirect(url_for("main.internal_server_error"))  # should never happen
    except:
        return render_template('product.html', product=products)
