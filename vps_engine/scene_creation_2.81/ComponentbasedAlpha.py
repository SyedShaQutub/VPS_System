import bpy

class ComponentbasedAlpha():
    def __init__(self, labelList, inputLink_image, inputLink_comp_id, idx, tree):

        self.label_name = labelList[0]
        self.pass_idx   = labelList[1]
        color = labelList[2]
        color =  [x / 255 for x in color]
        color.extend([1])
        self.id = idx
        self.color = color
        ##DEBUG
        # print("label name: {}".format(self.label_name))
        # print("label name: {}".format(self.label_name))
        # print("label pass idx: {}:".format(self.pass_idx))
        # print("label original color: {}".format(labelList[2]))
        # print("label color: {}".format(self.color))
    


        self.idMask = tree.nodes.new('CompositorNodeIDMask') # add ID mask node
        self.alpha = tree.nodes.new('CompositorNodeAlphaOver') # add alpha over node
        
        self.alpha.inputs[2].default_value = self.color
        #self.idMask.index
        self.idMask.use_antialiasing = True
        #self.idMask.inputs[0].default_value = self.label_id
        self.idMask.index = self.pass_idx

        self.link01 = tree.links.new(inputLink_comp_id,self.idMask.inputs[0]) # 14 - 'IndexOB', 15 - 'IndexMAT'
        self.link02 = tree.links.new(inputLink_image,self.alpha.inputs[1])
        self.link03 = tree.links.new(self.idMask.outputs[0], self.alpha.inputs[0])

    def get_outputLink(self):
        return self.alpha.outputs[0] # output from alpha over node
         