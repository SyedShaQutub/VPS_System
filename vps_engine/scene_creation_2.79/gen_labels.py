# reload every import 
import sys, os
import importlib
import bpy
import metaData
# TODO: change this to relative path using os/pathlib
# NOTE: If you load Blender first then open a project then the CWD is where Blender is. If you script from the blender the CWD is the location of the blender program.

# TODO: When excecuted in blender the os.path gives out C:/ instead of abs path of scene_launch; for now hard code the abs path of this file.
# office WS C:/Users/Qutub/Documents/VPS/scene_content/VPS_project/scene_creation
# HP laptop C:/Users/squtub/Documents/Master_Thesis/Git/vps_engine/scene_creation
filepath = bpy.context.space_data.text.filepath
print(filepath)
launch_path = os.path.dirname(filepath)
launch_path = launch_path.replace('\\','/')
sys.path.append(launch_path)

def main():
    obj_names = [obj.name for obj in bpy.data.objects]
    labels = metaData.labels
    _len = len(obj_names)
    obj_labels_id = [0] * _len
    obj_labels_name = ['unlabeled'] * _len
    bpy.context.scene.render.layers["RenderLayer"].use_pass_object_index = True

    for obj_ind, obj in enumerate(obj_names):
        for label in labels:
            if label[-1] in obj: 
                bpy.data.objects[obj].pass_index = label[1]
                obj_labels_id[obj_ind] = label[1]
                obj_labels_name[obj_ind] = label[-1]

    print(obj_labels_name)
    print(obj_labels_id)

    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links
    # remove all nodes
    for currentNode in tree.nodes:
        tree.nodes.remove(currentNode)

    idMask = tree.nodes.new('CompositorNodeIDMask') # add ID mask node
    renderer = tree.nodes.new('CompositorNodeRLayers') # add render node
    alpha = tree.nodes.new('CompositorNodeAlphaOver') # add alpha over node
    composite = tree.nodes.new('CompositorNodeComposite')

    alpha.inputs[2].default_value = (0, 1, 0.000530278, 1)


    idMask.inputs[0].default_value = 11
    link0 = links.new(renderer.outputs[14],idMask.inputs[0]) # 14 - 'IndexOB'
    link1 = links.new(renderer.outputs[0],alpha.inputs[1])

    link2 = links.new(idMask.outputs[0], alpha.inputs['Fac'])
    link3 = links.new(alpha.outputs[0], composite.inputs[0] )

    FILEPATH = launch_path + '/test.png'
    bpy.data.scenes['Scene'].render.filepath = FILEPATH
    bpy.ops.render.render(layer='RenderLayers', write_still=True)
    #bpy.ops.image.save_as(save_as_render=True, copy=True, filepath=FILEPATH, relative_path=True, show_multiview=False, use_multiview=False)



if __name__ == "__main__":
     main()