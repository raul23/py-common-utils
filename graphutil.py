from collections import OrderedDict
# Third-party modules
import ipdb
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.basemap import Basemap
import numpy as np
import plotly
from plotly.graph_objs import Scatter, Layout
from scipy.spatial import ConvexHull
# Own modules
from .genutil import init_variable, load_json_with_codecs


def draw_bar_chart(x,
                   y,
                   xlabel,
                   ylabel,
                   title,
                   grid_which='major',
                   yaxis_major_mutiplelocator=20,
                   yaxis_minor_mutiplelocator=10,
                   fig_width=5,
                   fig_height=5):
    # Sanity check on the input arrays
    assert isinstance(x, type(np.array([]))), \
        "generate_bar_chart(): wrong type on input array 'x'"
    assert isinstance(y, type(np.array([]))), \
        "generate_bar_chart(): wrong type on input array 'y'"
    assert x.shape == y.shape, \
        "generate_bar_chart(): wrong shape with 'x' and 'y'"
    assert grid_which in ["minor", "major", "both"], \
        "generate_bar_chart(): wrong value for grid_which='{}'".format(grid_which)
    plt.figure(figsize=(fig_width, fig_height))
    ax = plt.gca()
    index = np.arange(len(x))
    rects = plt.bar(index, y)
    # Add number-text on top of each bar
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2.,
                1 * height,
                '%d' % int(height),
                ha='center',
                va='bottom')
    plt.xticks(index, x)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=270.)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(yaxis_major_mutiplelocator))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(yaxis_minor_mutiplelocator))
    # plt.minorticks_on()
    plt.grid(which=grid_which)
    plt.tight_layout()
    plt.show()


def draw_histogram(data,
                   bins,
                   xlabel,
                   ylabel,
                   title,
                   grid_which='major',
                   xaxis_major_mutiplelocator=10000,
                   xaxis_minor_mutiplelocator=1000,
                   yaxis_major_mutiplelocator=5,
                   yaxis_minor_mutiplelocator=1):
    # TODO: `bin_width": 10000` not used
    # TODO: `xaxis_minor_mutiplelocator` not used
    # Sanity check on the input array
    assert isinstance(data, type(np.array([]))), \
        "wrong type on input array 'data'"
    assert grid_which in ["minor", "major", "both"], \
        "wrong value for grid_which='{}'".format(grid_which)
    ax = plt.gca()
    ax.hist(data, bins=bins, color="r")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(xaxis_major_mutiplelocator))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(yaxis_major_mutiplelocator))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(yaxis_minor_mutiplelocator))
    plt.xlim(0, data.max())
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=270.)
    plt.grid(True, which="major")
    plt.tight_layout()
    # TODO: add function to save image instead of showing it
    plt.show()


# TODO: check the code and improve it
# ref.: https://stackoverflow.com/a/42685102
def draw_us_states_names_on_map(basemap, us_states_filepath):
    us_states = load_json_with_codecs(us_states_filepath)
    printed_names = []
    mi_index = 0
    wi_index = 0
    for shapedict, state in zip(basemap.states_info, basemap.states):
        draw_state_name = True
        short_name = us_states[(shapedict['NAME'])]
        if short_name == 'PR':
            continue
        if short_name in printed_names and short_name not in ['MI', 'WI']:
            continue
        if short_name == 'MI':
            if mi_index != 3:
                draw_state_name = False
            mi_index += 1
        if short_name == 'WI':
            if wi_index != 2:
                draw_state_name = False
            wi_index += 1
        # center of polygon
        x, y = np.array(state).mean(axis=0)
        hull = ConvexHull(state)
        hull_points = np.array(state)[hull.vertices]
        # center of convex hull over the polygon points
        x, y = hull_points.mean(axis=0)
        if draw_state_name:
            # You have to align x,y manually to avoid overlapping for little states
            plt.text(x + .1, y, short_name, ha="center")
        printed_names += [short_name, ]


# `locations_geo_coords` is a dictionary with keys being the location name and
# the values are their corresponding `geopy.location.Location` objects
def draw_usa_map(locations_geo_coords,
                 shape_filepath,
                 us_states_filepath,
                 title, fig_width,
                 fig_height,
                 annotate_locations=None,
                 annotation_cfg=None,
                 basemap_cfg=None,
                 map_coords_cfg=None,
                 draw_parallels=True,
                 draw_meridians=True):

    def get_markersize(**kwargs):
        count = kwargs['count']
        marker_scale = kwargs['marker_scale']
        return int(np.sqrt(count)) * marker_scale

    # Init variables
    annotate_locations = init_variable(annotate_locations, [])
    annotation_cfg = init_variable(annotation_cfg, {})
    basemap_cfg = init_variable(basemap_cfg, {})
    map_coords_cfg = init_variable(map_coords_cfg, {})

    plt.figure(figsize=(fig_width, fig_height))
    plt.title(title)
    basemap = Basemap(projection=basemap_cfg.get('projection', 'lcc'),
                      llcrnrlon=basemap_cfg.get('llcrnrlon', -119),
                      llcrnrlat=basemap_cfg.get('llcrnrlat', 22),
                      urcrnrlon=basemap_cfg.get('urcrnrlon', -64),
                      urcrnrlat=basemap_cfg.get('urcrnrlat', 49),
                      lat_1=basemap_cfg.get('lat_1', 39),
                      lat_2=basemap_cfg.get('lat_2', 45),
                      lon_0=basemap_cfg.get('lon_0', -95))
    basemap.readshapefile(shapefile=shape_filepath,
                          name="states",
                          drawbounds=True)
    draw_us_states_names_on_map(basemap, us_states_filepath)
    mark_map_coords(basemap, locations_geo_coords, get_markersize,
                    annotate_locations, annotation_cfg, map_coords_cfg)
    if draw_meridians:
        basemap.drawmeridians(np.arange(-120, -40, 20), labels=[0, 0, 0, 1])
    if draw_parallels:
        basemap.drawparallels(np.arange(25, 65, 20), labels=[1, 0, 0, 0])
    plt.show()


def draw_world_map(locations_geo_coords,
                   title,
                   fig_width,
                   fig_height,
                   annotate_locations=None,
                   annotation_cfg=None,
                   basemap_cfg=None,
                   map_coords_cfg=None,
                   draw_coastlines=True,
                   draw_countries=True,
                   draw_map_boundary=True,
                   draw_meridians=True,
                   draw_parallels=True,
                   draw_states=True,
                   fill_continents=True):

    def get_markersize(**kwargs):
        return kwargs['marker_scale']

    # Init variables
    annotate_locations = init_variable(annotate_locations, [])
    annotation_cfg = init_variable(annotation_cfg, {})
    basemap_cfg = init_variable(basemap_cfg, {})
    map_coords_cfg = init_variable(map_coords_cfg, {})

    ipdb.set_trace()
    plt.figure(figsize=(fig_width, fig_height))
    plt.title(title)
    basemap = Basemap(projection=basemap_cfg['projection'],
                      llcrnrlon=basemap_cfg['llcrnrlon'],
                      llcrnrlat=basemap_cfg['llcrnrlat'],
                      urcrnrlon=basemap_cfg['urcrnrlon'],
                      urcrnrlat=basemap_cfg['urcrnrlat'])
    mark_map_coords(basemap, locations_geo_coords, get_markersize,
                    annotate_locations, annotation_cfg, map_coords_cfg)
    if draw_coastlines:
        basemap.drawcoastlines()
    if draw_countries:
        basemap.drawcountries()
    if draw_map_boundary:
        basemap.drawmapboundary()
    if draw_meridians:
        # basemap.drawmeridians(np.arange(-120, -40, 20), labels=[0, 0, 0, 1])
        pass
    if draw_parallels:
        # basemap.drawparallels(np.arange(25, 65, 20), labels=[1, 0, 0, 0])
        pass
    if draw_states:
        basemap.drawstates()
    if fill_continents:
        basemap.fillcontinents()
    plt.show()


def draw_pie_chart(values, labels, title):
    # Sanity check on the input arrays
    assert isinstance(values, type(np.array([]))), \
        "Wrong type on input array 'values'"
    assert isinstance(labels, type(np.array([]))), \
        "Wrong type on input array 'labels'"
    assert values.shape == labels.shape, \
        "Wrong shape with 'labels' and 'values'"
    ax = plt.gca()
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    ax.set_title(title)
    plt.axis("equal")
    plt.show()


def draw_scatter_plot(x, y, text, title, mode='markers', hovermode='closest',
                      yaxis_tickformat='$0.0f'):
    # TODO: add labels to axes
    assert isinstance(x, type(np.array([]))), "wrong type on input array 'x'"
    assert isinstance(y, type(np.array([]))), "wrong type on input array 'y'"
    assert isinstance(text, type(np.array([]))), "wrong type on input array 'text'"
    plotly.offline.plot({
        "data": [Scatter(x=list(x.flatten()),
                         y=list(y.flatten()),
                         mode=mode,
                         text=list(text.flatten()))],
        "layout": Layout(title=title,
                         hovermode=hovermode,
                         yaxis={'tickformat': yaxis_tickformat})
    })


# `get_markersize` is a function to compute the markersize
def mark_map_coords(basemap, locations_geo_coords, get_markersize,
                    annotate_locations=None, annotation_cfg=None,
                    map_coords_cfg=None):
    # Init variables
    annotate_locations = init_variable(annotate_locations, [])
    annotation_cfg = init_variable(annotation_cfg, {})
    map_coords_cfg = init_variable(map_coords_cfg, {})
    for address, data in locations_geo_coords.items():
        location = data['location']
        # Transform the location's longitude and latitude to the projection map
        # coordinates
        geo_coords = data['geo_coords']
        x, y = basemap(geo_coords.longitude, geo_coords.latitude)
        # Plot the map coordinates on the map; the size of the marker is
        # proportional to the number of occurrences of the location in job posts
        basemap.plot(
            x, y,
            color=map_coords_cfg.get('color', 'Red'),
            marker=map_coords_cfg.get('marker', 'o'),
            markersize=get_markersize(
                count=data['count'],
                marker_scale=map_coords_cfg.get('marker_scale', 1.5)))
        # Annotate some locations, e.g. the topk locations with the most job posts
        if location in annotate_locations:
            plt.text(x, y, location,
                     fontsize=annotation_cfg.get('fontsize', 5),
                     fontweight=annotation_cfg.get('fontweight', 'bold'),
                     ha=annotation_cfg.get('ha', 'left'),
                     va=annotation_cfg.get('va', 'bottom'),
                     color=annotation_cfg.get('color', 'k'))
