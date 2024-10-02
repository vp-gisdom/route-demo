import folium
from folium.map import Marker
from jinja2 import Template


def create_map(points, out_fp, map_route=None):
    m = folium.Map(location=[60.96, 24.34])
    click_js = """function onClick(e) {
                    var coord = e.latlng; 
                    sessionStorage.setItem("coords", e.latlng);
                    let data = {
                        lat: e.latlng.lat,
                        lng: e.latlng.lng
                    }

                    fetch("/route", {
                        method: 'POST',
                        mode: 'same-origin',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    }).then(() => {
                        window.location.reload();
                    });

                };
                    """

    click_template = """{% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.marker(
                {{ this.location|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }}).on('click', onClick);
    {% endmacro %}"""

    Marker._template = Template(click_template)

    e = folium.Element(click_js)
    html = m.get_root()
    html.script.get_root().render()
    html.script._children[e.get_name()] = e

    for i in points:
        Marker(location=[i.y, i.x]).add_to(m)

    if map_route:
        folium.PolyLine(
            locations=map_route,
            color="#FF0000",
            weight=5,
        ).add_to(m)

    m.save(out_fp)
