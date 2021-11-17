from api import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    fullname = db.Column(db.String)
    wallet_id = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'fullname': self.fullname,
            'wallet-id': self.wallet_id
        }


class Wallet(db.Model):
    __tablename__ = "wallet"
    BASE = 10000
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    user_id = db.Column(db.Integer)
    amount = db.Column(db.Integer, default=10000)

    def to_dict(self):
        return {
            'public-id': self.public_id,
            'user-id': self.user_id,
            'amount': self.amount
        }

    def add_amount(self, amount):
        self.amount = amount * self.BASE

