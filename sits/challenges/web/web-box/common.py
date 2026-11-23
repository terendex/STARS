"""The page every SITS web challenge is drawn in: a plain, ordinary-looking
small-business site, so nothing on screen hints at where the flag is."""
from flask import render_template_string

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
  <style>
    body { margin: 0; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; color: #1f2328; background: #f3f3f1; }
    header { padding: 14px 20px; background: #ffffff; border-bottom: 1px solid #d8d8d4; }
    header strong { font-size: 18px; }
    header span { margin-left: 10px; color: #6b6f76; font-size: 14px; }
    main { max-width: 640px; margin: 24px auto; padding: 0 16px; }
    .card { padding: 20px; background: #ffffff; border: 1px solid #d8d8d4; border-radius: 6px; }
    p { line-height: 1.5; }
    label { display: block; margin: 12px 0 4px; font-size: 14px; }
    input { width: 100%; padding: 8px; box-sizing: border-box; font: inherit; border: 1px solid #b9bcc2; border-radius: 4px; }
    button { margin-top: 14px; padding: 8px 16px; font: inherit; color: #ffffff; background: #1f5fa8; border: 0; border-radius: 4px; cursor: pointer; }
    button:disabled { color: #6b6f76; background: #d8d8d4; cursor: not-allowed; }
    a { color: #1f5fa8; }
    code { overflow-wrap: anywhere; }
    .error { color: #b42318; overflow-wrap: anywhere; }
    .key { padding: 10px; background: #f3f3f1; border: 1px solid #1f5fa8; border-radius: 4px; }
    .results { overflow-x: auto; margin-top: 16px; }
    table { width: 100%; border-collapse: collapse; font-size: 14px; }
    th, td { padding: 6px 8px; text-align: left; border-bottom: 1px solid #d8d8d4; }
  </style>
</head>
<body>
  <header><strong>{{ title }}</strong>{% if subtitle %}<span>{{ subtitle }}</span>{% endif %}</header>
  <main>
    <div class="card">
{{ body | safe }}
    </div>
  </main>
</body>
</html>
"""


def page(title, subtitle, body, **values):
    return render_template_string(
        PAGE,
        title=title,
        subtitle=subtitle,
        body=render_template_string(body, **values),
    )
