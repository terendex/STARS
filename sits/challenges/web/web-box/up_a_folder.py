import os

from flask import Flask, request

from common import page

app = Flask(__name__)
FLAG = "FLAG{cl1mb3d_0n3_f0ld3r_up}"

# The recipes, and the flag one folder above them. Written at start-up into
# /tmp (the only writable place in the container).
BASE = "/tmp/recipe-box"
RECIPES = os.path.join(BASE, "recipes")
FILES = {
    "pancakes.txt": "Pancakes: 1 cup flour, 1 egg, 1 cup milk, a pinch of sugar. Mix, then fry until golden.",
    "omelette.txt": "Omelette: 3 eggs, a splash of milk, cheese. Whisk, pour into a hot pan, fold in half.",
    "smoothie.txt": "Smoothie: 1 banana, a handful of strawberries, 1 cup of yoghurt. Blend until smooth.",
}
os.makedirs(RECIPES, exist_ok=True)
for name, text in FILES.items():
    with open(os.path.join(RECIPES, name), "w") as f:
        f.write(text + "\n")
with open(os.path.join(BASE, "flag.txt"), "w") as f:
    f.write(f"Grandma's secret ingredient: {FLAG}\n")

BODY = """
<p><a href="?recipe=pancakes.txt">Pancakes</a> &middot; <a href="?recipe=omelette.txt">Omelette</a>
&middot; <a href="?recipe=smoothie.txt">Smoothie</a></p>
{% if error %}<p class="error">{{ error }}</p>{% else %}<p>{{ text }}</p>{% endif %}
"""


@app.route("/")
def home():
    name = request.args.get("recipe", "pancakes.txt")
    # Intentionally vulnerable to path traversal: this is the challenge.
    path = os.path.join(RECIPES, name)
    try:
        with open(path) as f:
            text, error = f.read(), None
    except OSError:
        text, error = None, f"Couldn't open the file {path}"
    return page("Recipe Box", "Breakfast ideas", BODY, text=text, error=error)
