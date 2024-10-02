import json

SESSION_FILE = "session/session.json"
TEMPLATE_FILE = "session/template.json"


def load_session():
    with open(SESSION_FILE, "r") as file:
        return json.load(file)


def save_session(session: dict):
    with open(SESSION_FILE, "w") as file:
        json.dump(session, file, indent=4)


def clear_session():
    with open(TEMPLATE_FILE, "r") as file:
        template = json.load(file)
    with open(SESSION_FILE, "w") as file:
        json.dump(template, file)


def add_route(route):
    session = load_session()
    session["session"]["route"] = route
    save_session(session)


def add_latlon(lat, lon):
    session = load_session()
    session["session"]["lat"] = lat
    session["session"]["lon"] = lon
    save_session(session)
