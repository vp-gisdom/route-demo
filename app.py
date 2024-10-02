from flask import Flask, redirect, render_template, request, url_for

from flask_session import Session
from src.map import create_map
from src.route import calculate_route, get_graph, get_points, route_to_map_coords
from src.session import add_latlon, add_route, clear_session, load_session

app = Flask(__name__)
sess = Session()


@app.route("/", methods=["GET", "POST"])
def base():
    global graph
    session = load_session()
    if not session["session"]["lat"]:
        graph = get_graph((61.1223, 60.8164, 24.6231, 24.0063))
        return render_template("map.html")
    else:
        route = calculate_route(graph, 60.9814, 24.0728, session["session"]["lat"], session["session"]["lon"])
        map_route = route_to_map_coords(graph, route)
        create_map(get_points(), "templates/route.html", map_route)
        add_route(map_route)
        return render_template("route.html")


@app.route("/route", methods=["GET", "POST"])
def route_to_map():
    if request.method == "POST":
        data = request.get_json()
        lat = float(data["lat"])
        lon = float(data["lng"])
        add_latlon(lat, lon)

        return redirect("/")


@app.route("/render", methods=["GET", "POST"])
def render():
    return render_template("route.html")


if __name__ == "__main__":
    clear_session()
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SESSION_TYPE"] = "filesystem"
    sess.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
