import geopandas as gpd
import networkx as nx
import osmnx as ox
from pyproj import Transformer


def calculate_route(graph: ox.graph, start_lat, start_lon, end_lat, end_lon):
    graph_proj = ox.project_graph(graph)
    dest_epsg = ox.graph_to_gdfs(graph_proj, nodes=True, edges=False).crs.to_epsg()
    transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{dest_epsg}")
    start_x, start_y = transformer.transform(start_lat, start_lon)
    end_x, end_y = transformer.transform(end_lat, end_lon)
    orig_node = ox.nearest_nodes(graph_proj, start_x, start_y)
    target_node = ox.nearest_nodes(graph_proj, end_x, end_y)
    return nx.shortest_path(G=graph_proj, source=orig_node, target=target_node, weight="length")
    # fig, ax = ox.plot_graph_route(graph, rt)


def route_to_map_coords(graph, route):
    graph_proj = ox.project_graph(graph)
    nodes_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=False)
    route_nodes = nodes_proj.loc[route]
    route_nodes.to_crs(crs=4326, inplace=True)
    node_list = list(route_nodes.geometry.values)
    return [[i.y, i.x] for i in node_list]


def get_graph(bbox: tuple, nw_type: str = "drive"):
    return ox.graph.graph_from_bbox(bbox=bbox, network_type=nw_type)


def get_points(fp="/mnt/c/Users/Viljami/Documents/route_test/random_points_subset.shp"):
    gdf = gpd.read_file(fp)
    return gdf["geometry"].to_list()
