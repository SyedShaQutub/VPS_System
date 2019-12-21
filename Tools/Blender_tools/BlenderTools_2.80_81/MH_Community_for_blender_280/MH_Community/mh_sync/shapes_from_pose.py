
import bpy
#===============================================================================
def shapesFromPose(operator, skeleton, shapeName):
    scene = bpy.context.scene
    meshes = getMeshesForRig(scene, skeleton)
    allBones = getAllBones(skeleton)
    operator.report({'INFO'}, shapeName + ' stats:')

    for mesh in meshes:
        tVerts = len(mesh.data.vertices)

        # delete if key already exists
        deleteShape(mesh, shapeName)

        # add an empty key (create a basis when none)
        key = mesh.shape_key_add(shapeName, False)
        key.value = 0 # keep un-applied

        # get basis, so can write only verts different than
        basis = mesh.data.shape_keys.key_blocks['Basis']

        # get temporary version with modifiers applied
        tmp = mesh.to_mesh(scene, True, 'PREVIEW')

        # assign the key the vert values of the current pose, when different than Basis
        nDiff = 0
        for v in tmp.vertices:
            # first pass; exclude verts not influenced by the Bones selected
            if not isVertexInfluenced(mesh.vertex_groups, v, allBones) : continue

            value   = v.co
            baseval = basis.data[v.index].co
            if not similar_vertex(value, baseval):
                key.data[v.index].co = value
                nDiff += 1

        if nDiff > 0:
            operator.report({'INFO'}, '     ' + mesh.name + ':  ' + str(nDiff) + ' of ' + str(tVerts))
        else:
            # when no verts different, delete key for this mesh
            mesh.shape_key_remove(key)

        # remove temp mesh
        bpy.data.meshes.remove(tmp)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# determine all the meshes which are controlled by skeleton
def getMeshesForRig(scene, skeleton):
    meshes = []
    for object in [object for object in scene.objects]:
        if object.type == 'MESH' and len(object.vertex_groups) > 0 and skeleton == object.find_armature():
            meshes.append(object)
            # ensure that there is a Basis key
            if not object.data.shape_keys:
                object.shape_key_add('Basis')

    return meshes
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# This also returns hidden bones, critical for finger shape keys
def getAllBones(skeleton):
    vGroupNames = []
    for bone in skeleton.data.bones:
        vGroupNames.append(bone.name)

    return vGroupNames
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def deleteShape(mesh, shapeName):
    if not mesh.data.shape_keys:
        return

    for key_block in mesh.data.shape_keys.key_blocks:
        if key_block.name == shapeName:
            mesh.shape_key_remove(key_block)
            return
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def isVertexInfluenced(mesh_vertex_groups, vertex, allBones):
    for group in vertex.groups:
        for bone in allBones:
            if mesh_vertex_groups[group.group].name == bone:
                return True
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def similar_vertex(vertA, vertB, tolerance = 0.00015):
    if vertA is None or vertB is None: return False
    if (abs(vertA.x - vertB.x) > tolerance or
        abs(vertA.y - vertB.y) > tolerance or
        abs(vertA.z - vertB.z) > tolerance ):
        return False
    return True