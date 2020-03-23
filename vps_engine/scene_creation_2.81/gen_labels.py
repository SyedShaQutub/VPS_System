# reload every import 
import bpy
import sys, os
import importlib

import metaData
importlib.reload(metaData)
import ComponentbasedAlpha
importlib.reload(ComponentbasedAlpha)
from ComponentbasedAlpha import ComponentbasedAlpha

# TODO: change this to relative path using os/pathlib
# NOTE: If you load Blender first then open a project then the CWD is where Blender is. If you script from the blender the CWD is the location of the blender program.

# TODO: When excecuted in blender the os.path gives out C:/ instead of abs path of scene_launch; for now hard code the abs path of this file.
# office WS C:/Users/Qutub/Documents/VPS/scene_content/VPS_project/scene_creation
# HP laptop C:/Users/squtub/Documents/Master_Thesis/Git/vps_engine/scene_creation

# filepath = bpy.context.space_data.text.filepath
# print(filepath)
# labels_path = os.path.dirname(filepath)
# labels_path = labels_path.replace('\\','/')
# sys.path.append(labels_path)

def edit_ShaderEditorNodes():
    # adapts FBX model for cycle renderer
    mat = [mat.name for mat in bpy.data.materials]
    character = 'male'
    for _mat in mat:
        if character not in _mat:
            #delete the node Image Texture.001
            purge_nodeName = 'Image Texture.001'
            principled_bsdf = 'Principled BSDF'
            nodes = bpy.data.materials[_mat].node_tree.nodes
            links = bpy.data.materials[_mat].node_tree.links
            node_names = [node.name for node in nodes]
            if purge_nodeName in node_names and principled_bsdf in node_names:
                print(_mat)
                purge_node = nodes[purge_nodeName]
                nodes.remove(purge_node)
                links.new(nodes['Image Texture'].outputs['Alpha'], nodes['Principled BSDF'].inputs['Alpha'])
            
def gen_CompositorNodes_objbased():
    obj_names = [obj.name for obj in bpy.data.objects]
    labels = metaData.cityscape_labels
    obj_pass_idx = [0] * len(obj_names)
    obj_labels_name = ['unlabeled'] * len(obj_names)
    obj_labels_color = [(0,0,0)] * len(obj_names)

    bpy.context.scene.view_layers["View Layer"].use_pass_object_index = True
    bpy.context.scene.view_layers["View Layer"].use_pass_environment = True

    #attribute labels data corresponsing to the object
    for obj_ind, obj in enumerate(obj_names):
        label_found = False
        for label in labels:
            for idx in range(len(label[-1])):
                if label[-1][idx].lower() in obj.lower(): 
                    bpy.data.objects[obj].pass_index = label[2]  #  label[1] 
                    obj_pass_idx[obj_ind] = label[2] #  label[1] 
                    obj_labels_color[obj_ind] = list(label[7])
                    obj_labels_name[obj_ind] = label[0]
                    label_found = True
                    break
            if label_found == True:
                break
    
    #DEBUG
    # print(obj_labels_name)
    # print(obj_pass_idx)

    labels_list = list(zip(obj_labels_name, obj_pass_idx, obj_labels_color))
    del obj_pass_idx, obj_labels_name, obj_labels_color

    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    tree.use_opencl = True

    links = tree.links
    # remove all nodes
    for currentNode in tree.nodes:
        tree.nodes.remove(currentNode)

    alphablocks = []
    renderer = tree.nodes.new('CompositorNodeRLayers') # add render node
    global_composite = tree.nodes.new('CompositorNodeComposite')
    global_composite.use_alpha = True
    inputLink_image = renderer.outputs[0]
    inputLink_obj_id = renderer.outputs[14]

    ## TEST to check the class
    # alphablocks.append(objectbasedAlpha(labels_list[0], inputLink_image, inputLink_obj_id, 0, tree))
    # inputLink_image = alphablocks[0].get_outputLink()

    for idx, label_list in enumerate(labels_list):
        alphablocks.append(ComponentbasedAlpha(label_list, inputLink_image, inputLink_obj_id, idx, tree, color = 'grey'))
        inputLink_image = alphablocks[idx].get_outputLink()

    #environment based Alpha
    Sky_label = (70,130,180)
    sky_label = [x / 255 for x in Sky_label]
    sky_label.extend([1])
    envAlphaNode = tree.nodes.new('CompositorNodeAlphaOver') # add alpha over node
    envAlphaNode.inputs[2].default_value = sky_label
    links.new(inputLink_image, envAlphaNode.inputs[1])
    links.new(renderer.outputs['Env'], envAlphaNode.inputs[0])

    #Global LinkS
    links.new(envAlphaNode.outputs[0], global_composite.inputs[0] )

def gen_CompositorNodes_matbased():
    mat_names = [material.name for material in bpy.data.materials]
    labels = metaData.labels
    mat_pass_idx = [0] * len(mat_names)
    mat_labels_name = ['unlabeled'] * len(mat_names)
    mat_labels_color = [(0,0,0)] * len(mat_names)

    bpy.context.scene.view_layers["View Layer"].use_pass_material_index = True
    bpy.context.scene.view_layers["View Layer"].use_pass_environment = True

    #attribute labels data corresponsing to the object
    for mat_ind, mat in enumerate(mat_names):
        label_found = False
        for label in labels:
            for idx in range(len(label[-1])):
            
                if label[-1][idx].lower() in mat.lower(): 
                    bpy.data.materials[mat].pass_index = label[2]
                    mat_pass_idx[mat_ind] = label[2]
                    mat_labels_name[mat_ind] = label[0]
                    mat_labels_color[mat_ind] = list(label[7])
                    label_found = True
                    break
            if label_found == True:
                break
    
    # #DEBUG
    # print(mat_labels_name)
    # print(mat_pass_idx)

    labels_list = list(zip(mat_labels_name, mat_pass_idx, mat_labels_color))
    del mat_pass_idx, mat_labels_name, mat_labels_color

    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    tree.use_opencl = True

    links = tree.links
    # remove all nodes
    for currentNode in tree.nodes:
        tree.nodes.remove(currentNode)

    alphablocks = []
    renderer = tree.nodes.new('CompositorNodeRLayers') # add render node
    global_composite = tree.nodes.new('CompositorNodeComposite')
    global_composite.use_alpha = True
    inputLink_image = renderer.outputs[0]
    inputLink_mat_id = renderer.outputs[15] #15 IndexedMA

    ## TEST to check the class
    # alphablocks.append(objectbasedAlpha(labels_list[0], inputLink_image, inputLink_obj_id, 0, tree))
    # inputLink_image = alphablocks[0].get_outputLink()

    for idx, label_list in enumerate(labels_list):
        alphablocks.append(ComponentbasedAlpha(label_list, inputLink_image, inputLink_mat_id, idx, tree,  label = 'grey'))
        inputLink_image = alphablocks[idx].get_outputLink()

    #environment based Alpha
    #Sky_label = (70,130,180)
    Sky_label = [10,10,10]
    sky_label = [x / 255 for x in Sky_label]
    sky_label.extend([0])
    envAlphaNode = tree.nodes.new('CompositorNodeAlphaOver') # add alpha over node
    envAlphaNode.inputs[2].default_value = sky_label
    links.new(inputLink_image, envAlphaNode.inputs[1])
    links.new(renderer.outputs['Env'], envAlphaNode.inputs[0])

    #Global LinkS
    links.new(envAlphaNode.outputs[0], global_composite.inputs[0] )


def gen_labels():

    gen_CompositorNodes_objbased()
    FILEPATH = launch_path + '/test.png'
    bpy.data.scenes['Scene'].render.filepath = FILEPATH
    bpy.ops.render.render(layer='RenderLayers', write_still=True)

def gen_labels_env(mode='obj', labels_path=None,):

    if mode == 'obj':
        gen_CompositorNodes_objbased()
    elif mode == 'mat':
        gen_CompositorNodes_matbased()
    #FILEPATH = labels_path + '/test.png'
    # bpy.data.scenes['Scene'].render.filepath = FILEPATH
    # bpy.ops.render.render(layer='RenderLayers', write_still=True)

if __name__ == "__main__":
    gen_labels_env(mode ='mat')