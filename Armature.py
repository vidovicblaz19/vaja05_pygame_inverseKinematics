import math
import pygame
import manager
import copy

class Armature:
    def __init__(self, _bones, _target):
        self.bones = _bones
        self.target = _target
        self.anchor = manager.anchor
        self.armature_length = self.armature_length_function()

    def armature_length_function(self):
        dist = 0
        for bone in self.bones:
            dist = dist + bone.bone_length
        return dist

    def distance(self,p1,p2):
        return math.sqrt(math.pow(p2[0]-p1[0],2) + math.pow(p2[1]-p1[1],2))

    def err(self,_bones):
        eff = self.updateBonesAndGetEffector(_bones)
        return self.distance(eff,self.target)

    def modifyAngles(self, relative_angles):
        for i in range(len(self.bones)):
            self.bones[i].relative_angle = relative_angles[i]

    def GradientOptimizationMethod(self):
        current_relative_angles = []
        for bone in self.bones:
            current_relative_angles.append(bone.relative_angle)

        gradients = [None] * len(current_relative_angles)
        
        iter = 0
        while(self.err(self.bones) > manager.d and iter < manager.max_iter):
            for i in range(len(self.bones)):
                bonesA_relative_angles = list(current_relative_angles)
                bonesB_relative_angles = list(current_relative_angles)

                bonesA_relative_angles[i] = bonesA_relative_angles[i] + manager.g
                bonesB_relative_angles[i] = bonesA_relative_angles[i] - manager.g

                self.modifyAngles(bonesA_relative_angles)
                errA = self.err(self.bones)
                self.modifyAngles(bonesB_relative_angles)
                errB = self.err(self.bones)

                gradients[i] = errA - errB
                current_relative_angles[i] = current_relative_angles[i] - gradients[i]

            iter = iter + 1

        self.modifyAngles(current_relative_angles)


    def angleBetweenPoints(self,p1,p2):
        return math.atan2(p2[1]-p1[1],p2[0]-p1[0]) * 180 / math.pi

    def update(self, target_location):
        #compute Gradient optimization
        self.target = target_location
        #if(self.distance(self.target,self.anchor) > self.armature_length):
        #    self.bones[0].relative_angle = self.angleBetweenPoints(self.anchor,self.target)
        #    for i in range(1,len(self.bones)):
        #        self.bones[i].relative_angle = 0
        #else:
        self.GradientOptimizationMethod()
        self.updateBonesAndGetEffector(self.bones)

    def updateBonesAndGetEffector(self, _bones):
        #===updates the positions of bones (joints, angles, and effectors)===
        _total_angle = 0;
        # set joint of child bone to effector of previous bone, and update the current bone position
        for i in range(len(_bones)):
            if(i == 0):
                _bones[i].update(self.anchor,_total_angle)
            else:
                _bones[i].update(_bones[i-1].effector,_total_angle)
            
            _total_angle = _total_angle + _bones[i].relative_angle
        
        return _bones[len(_bones)-1].effector