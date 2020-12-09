#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

from flask import *
from flask_login import login_required, current_user
from ..models import Product

# user created
from . import main
from .. import db
from ..models import User


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pass
    products = Product.query.all()
    prd_qty = {}
    qty = []
    for product in products:
        prd_qty[product] = product.quantity
        qty.append(product.quantity)
    
    return render_template('index.html')

