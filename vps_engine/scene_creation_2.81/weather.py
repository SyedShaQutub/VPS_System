import os
import bpy

import importlib
import blender_utils
importlib.reload(blender_utils)
from blender_utils import *


def dynamicWeather():
    bpy.ops.sky.dyn()
    dyn_sky = bpy.data.worlds['Dynamic_1']
    dyn_sky.use_nodes = True
    bpy.context.scene.world = dyn_sky
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
    #dyn_sky.node_tree.nodes["sun_value"].inputs[1].default_value = (0,0,0,1)
    #Sun_Color
    #dyn_sky.node_tree.nodes["sun_color"].inputs[1].default_value = (0,0,0,1)
    #Soft_Hard - Controls softness of shadows
    #dyn_sky.node_tree.nodes["Soft_hard"].inputs[0].default_value = 0

    ##sky day and night
    dyn_sky.node_tree.nodes["Scene_Brightness"].inputs[1].default_value = 0.2

    #Sun position
    dyn_sky.node_tree.nodes["Sky_normal"].outputs[0].default_value = (-0.0956522, 0.169565, 0.980866)
