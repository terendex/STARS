from flask import Flask, request

from common import page

app = Flask(__name__)
FLAG = "FLAG{th3_br0ws3r_kn3w_th3_c0d3}"
ACCESS_CODE = "extra-cheese-please"

# The page checks the code with JavaScript, so the code itself is in the page
# for anyone who reads its source.
HOME = """
<p>The Pizza Club members' area. Members get the secret menu.</p>
<form onsubmit="return checkCode()">
  <label for="code">Members' code</label>
  <input id="code" autocomplete="off" autofocus>
  <button type="submit">Let me in</button>
</form>
<p id="result" class="error"></p>
<script>
  // TODO: check the code on the server instead, before we launch!
  const MEMBERS_CODE = "{{ code }}";

  function checkCode() {
    const value = document.getElementById("code").value;
    if (value === MEMBERS_CODE) {
      location.href = "/members?code=" + encodeURIComponent(value);
    } else {
      document.getElementById("result").textContent = "Wrong code.";
    }
    return false;
  }
</script>
"""

MEMBERS = """
<p>Welcome, member! Here's the secret menu.</p>
<p class="key"><code>{{ flag }}</code></p>
"""

DENIED = """
<p class="error">Wrong code.</p>
<p><a href="/">Back</a></p>
"""


@app.route("/")
def home():
    return page("Pizza Club", "Members only", HOME, code=ACCESS_CODE)


@app.route("/members")
def members():
    if request.args.get("code") == ACCESS_CODE:
        return page("Pizza Club", "Members only", MEMBERS, flag=FLAG)
    return page("Pizza Club", "Members only", DENIED), 403
