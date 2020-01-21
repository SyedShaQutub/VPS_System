import os
import bpy

import importlib
import blender_utils
importlib.reload(blender_utils)
from blender_utils import *

from pysolar.solar import *
import datetime
import pytz

CITY_LAT_LONG = [['munich', [48.1351, 11.5820]], ['berlin',[52.5200, 13.4050]], ['london',[51.507351, -0.127758]]]

def dynamicWeather():
    bpy.ops.sky.dyn()
    dyn_sky = bpy.data.worlds['Dynamic_1']
    dyn_sky.use_nodes = True
    bpy.context.scene.world = dyn_sky

    date = datetime.datetime.now()
    
    city_name = 'munich'
    ind_city_lat_long = [(i, colour.index(c)) for i, colour in enumerate(CITY_LAT_LONG) if c in colour]
    city_lat_long = CITY_LAT_LONG[ind_city_lat_long[0][0]]
    date = datetime.datetime.now(pytz.UTC)
    #https://pysolar.readthedocs.io/en/latest/
    altitude_deg = get_altitude(lat_long[1][0], lat_long[1][1], date)

    #radiation  - watts/sq.m
    rad_direct = radiation.get_radiation_direct(date, altitude_deg)
    ##Sky Control
    #sky color 
    #dyn_sky.node_tree.nodes['Sky_and_Horizon_colors'].inputs[1].default_value 
    #Horizon color
    #dyn_sky.node_tree.nodes['Sky_and_Horizon_colors'].inputs[2].default_value

    ##Cloud Control
    #Cloud Color
    #dyn_sky.node_tree.nodes["Cloud_color"].inputs[1].default_value = (0.0618412, 1, 0.256814, 1)
    #Cloud Opacity
    #dyn_sky.node_tree.nodes["Cloud_opacity"].inputs[0].default_value = 0.5
    #Cloud Density
    #dyn_sky.node_tree.nodes["Cloud_density"].inputs[0].default_value = 1

    ##Sun Control
    #Sun_value - sunlight opacity
    #dyn_sky.node_tree.nodes["Sun_value"].inputs[1].default_value = 0.5

    #Sun_Color
    #dyn_sky.node_tree.nodes["Sun_color"].inputs[1].default_value = (0,0,0,1)
    #Soft_Hard - Controls softness of shadows
    #dyn_sky.node_tree.nodes["Soft_hard"].inputs[0].default_value = 0

    ##sky day and night
    #dyn_sky.node_tree.nodes["Scene_Brightness"].inputs[1].default_value = 0.2

    #Sun position
    #dyn_sky.node_tree.nodes["Sky_normal"].outputs[0].default_value = (-0.0956522, 0.169565, 0.980866)

    #Shadow Color Saturation
    #dyn_sky.node_tree.nodes["Shadow_color_saturation"].inputs[1].default_value = 0.02
