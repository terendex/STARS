from flask import Flask, request

from common import page

app = Flask(__name__)
FLAG = "STARS{m1nt4k4_n3v3r_trust_th3_br0ws3r}"
ACCESS_CODE = "orions-belt-1"

HOME = """
<form onsubmit="return checkCode()">
  <label for="code">Access code</label>
  <input id="code" autocomplete="off" autofocus>
  <button type="submit">Open the vault</button>
</form>
<p id="result" class="error"></p>
<script>
  // TODO: move this check to the server before launch!
  const ACCESS_CODE = "{{ code }}";

  function checkCode() {
    const value = document.getElementById("code").value;
    if (value === ACCESS_CODE) {
      location.href = "/vault?code=" + encodeURIComponent(value);
    } else {
      document.getElementById("result").textContent = "Access denied.";
    }
    return false;
  }
</script>
"""

VAULT = """
<p>The vault is open.</p>
<p class="key"><code>{{ flag }}</code></p>
"""

DENIED = """
<p class="error">Access denied.</p>
<p><a href="/">Back</a></p>
"""


@app.route("/")
def home():
    return page("Mintaka Vault", "Orion's belt, western star", HOME, code=ACCESS_CODE)


@app.route("/vault")
def vault():
    if request.args.get("code") == ACCESS_CODE:
        return page("Mintaka Vault", "Orion's belt, western star", VAULT, flag=FLAG)
    return page("Mintaka Vault", "Orion's belt, western star", DENIED), 403
