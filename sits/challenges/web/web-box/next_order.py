from flask import Flask

from common import page

app = Flask(__name__)
FLAG = "FLAG{0rd3r_numb3rs_4r3_gu3ss4bl3}"
MINE = [1004, 1007, 1009]

# Every order. The site never checks whose order you're looking at, so changing
# the number in the address shows anyone's. Order 1001, the very first one, was
# placed by the owner.
ORDERS = {
    1001: ("The owner", f"1 x Owner's Special. Note to the kitchen: the safe code is {FLAG}"),
    1002: ("Mia", "2 x Margherita, 1 x garlic bread"),
    1003: ("Leo", "1 x Hawaiian (yes, with pineapple)"),
    1004: ("You", "1 x Pepperoni, 1 x cola"),
    1005: ("Sam", "3 x Four Cheese, for a movie night"),
    1006: ("Ana", "1 x Veggie Supreme, no olives"),
    1007: ("You", "1 x BBQ Chicken"),
    1008: ("Ben", "2 x Pepperoni, extra hot"),
    1009: ("You", "1 x Margherita, 1 x ice cream"),
}

HOME = """
<p>Your recent orders:</p>
<ul>
{% for number in mine %}
  <li><a href="/order/{{ number }}">Order {{ number }}</a></li>
{% endfor %}
</ul>
"""

ORDER = """
<p><strong>Ordered by:</strong> {{ who }}</p>
<p>{{ text }}</p>
<p><a href="/">Back to your orders</a></p>
"""


@app.route("/")
def home():
    return page("Pizza Tracker", "Your orders", HOME, mine=MINE)


@app.route("/order/<int:number>")
def order(number):
    if number not in ORDERS:
        return page("Pizza Tracker", "No such order",
                    '<p>There\'s no order with that number.</p><p><a href="/">Back to your orders</a></p>'), 404
    who, text = ORDERS[number]
    return page("Pizza Tracker", f"Order {number}", ORDER, who=who, text=text)
