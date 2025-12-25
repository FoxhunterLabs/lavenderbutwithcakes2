from flask import Blueprint, render_template_string, request, redirect, url_for

from models.people import list_people, upsert_person, get_person
from inference.bayes import compute_posteriors
from db import db

ui = Blueprint("ui", __name__)

DASH = """
<h2>LavenderButWithCakes2</h2>
<form method="post" action="/ui/person">
  <input name="person_key" placeholder="person_key" required>
  <input name="display_name" placeholder="display_name">
  <button type="submit">Upsert person</button>
</form>

<h3>People</h3>
<ul>
{% for p in people %}
  <li>
    <b>{{p.person_key}}</b>
    <a href="/ui/person/{{p.person_key}}">view</a>
  </li>
{% endfor %}
</ul>
"""

PERSON = """
<h2>{{person.person_key}}</h2>
<pre>{{person}}</pre>

<h3>Posteriors</h3>
<pre>{{post}}</pre>

<p><a href="/">Back</a></p>
"""


@ui.route("/", methods=["GET"])
def home():
    return render_template_string(DASH, people=list_people())


@ui.route("/person", methods=["POST"])
def person_upsert():
    upsert_person(
        request.form["person_key"],
        request.form.get("display_name"),
    )
    return redirect(url_for("ui.home"))


@ui.route("/person/<person_key>", methods=["GET"])
def person_view(person_key: str):
    person = get_person(person_key)
    if not person:
        return "not found", 404
    return render_template_string(
        PERSON,
        person=person,
        post=compute_posteriors(person_key),
    )
