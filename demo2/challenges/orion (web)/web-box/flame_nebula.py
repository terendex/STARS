"""Flame Nebula (Medium): server-side template injection.

The register writes the visitor's star name into the source of a small
template and then renders it, so anything between {{ and }} is worked out as a
template expression. Naming a star {{7*7}} shows 49, and {{ config }} shows the
site's settings, flag included.

It's kept safe. The card is rendered in Jinja's sandbox, which blocks the usual
ways out to Python itself (anything starting with _), with no global functions,
a short list of filters, no **, and no huge numbers or repeats. The name is
short, < and > are escaped before it goes in, and "config" is a plain dict, not
Flask's real config. The rest of the page is a normal template that only ever
receives the finished card.
"""
import html

from flask import Flask, request
from jinja2 import TemplateError
from jinja2.sandbox import ImmutableSandboxedEnvironment, SecurityError
from markupsafe import Markup, escape

from common import page

app = Flask(__name__)
FLAG = "STARS{fl4m3_t3mpl4t3s_sp1ll_s3cr3ts}"
LONGEST_NAME = 60
BIGGEST_NUMBER = 1000

# What {{ config }} shows. It looks like a real site's settings.
SETTINGS = {
    "SITE_NAME": "Flame Nebula Star Register",
    "REGISTER_OPEN": True,
    "STARS_PER_VISITOR": 1,
    "SECRET_KEY": FLAG,
}

SAFE_FILTERS = {
    "capitalize", "count", "default", "d", "dictsort", "e", "escape", "first", "items", "join",
    "last", "length", "list", "lower", "pprint", "replace", "reverse", "sort", "string", "title",
    "tojson", "trim", "upper",
}


class CardSandbox(ImmutableSandboxedEnvironment):
    # call_binop only sees these operators. ** can run for ever, and * can
    # build a string too big for the server.
    intercepted_binops = frozenset(["**", "*"])

    def call_binop(self, context, operator, left, right):
        if operator == "**":
            raise SecurityError("Powers (**) are switched off on this site.")
        if isinstance(left, (str, list, tuple)) or isinstance(right, (str, list, tuple)):
            count = right if isinstance(right, int) else left
            if not isinstance(count, int) or abs(count) > BIGGEST_NUMBER:
                raise SecurityError("That would make the card too big.")
        return left * right

    def call(self, context, obj, /, *args, **kwargs):
        # Methods like "a".ljust(99999999) would also make huge strings.
        for value in (*args, *kwargs.values()):
            if isinstance(value, int) and abs(value) > BIGGEST_NUMBER:
                raise SecurityError("That number is too big for a star card.")
        return super().call(context, obj, *args, **kwargs)


cards = CardSandbox(autoescape=True)
cards.globals.clear()
cards.filters = {name: f for name, f in cards.filters.items() if name in SAFE_FILTERS}

BODY = """
<p>Anyone can name a star in the Flame Nebula, the glowing cloud beside Orion's
belt. Type a name, and the register makes you a welcome card for it.</p>
<form method="get" action="/">
  <label for="name">Your star's name</label>
  <input id="name" name="name" maxlength="60" value="{{ name }}" autocomplete="off">
  <button type="submit">Name my star</button>
</form>
{% if card %}<div class="results">{{ card }}</div>{% endif %}
"""


def welcome_card(name):
    if len(name) > LONGEST_NAME:
        return Markup('<p class="error">Star names can be 60 characters at most.</p>')
    # The bug: the name becomes part of the template's own source.
    source = (
        '<div class="key"><p>Welcome to the register, <strong>'
        + html.escape(name, quote=False)
        + "</strong>!</p><p>Your star now shines in the Flame Nebula.</p></div>"
    )
    try:
        return Markup(cards.from_string(source).render(config=SETTINGS))
    except TemplateError as problem:
        return Markup('<p class="error">The register couldn\'t make that card: {}</p>').format(escape(str(problem)))


@app.route("/")
def home():
    name = request.args.get("name", "")
    card = welcome_card(name) if name else ""
    return page("Flame Nebula Star Register", "Name a star of your own", BODY, name=name, card=card)
