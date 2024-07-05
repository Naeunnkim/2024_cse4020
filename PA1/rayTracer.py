#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)

class Sphere:
    def __init__(self, center, radius, shader):
        self.center = center
        self.radius = radius
        self.shader = shader

class ShaderLamb:
    def __init__(self, diffuse_color):
        self.diffuse_color = diffuse_color

class ShaderPhong:
    def __init__(self, diffuse_color, specular_color, exponent):
        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.exponent = exponent

def raytrace(ray, viewPoint, surfaceList):
    closest = -1
    cnt = 0

    m = sys.maxsize

    for s in surfaceList:
        if(isinstance(s, Sphere)):
            a = np.dot(ray, ray)
            b = np.dot(viewPoint - s.center,  ray)
            c = np.dot(viewPoint - s.center, viewPoint - s.center) - s.radius**2

            if b**2 - a*c >=0 :
                if -b + np.sqrt(b**2 - a*c) >= 0:
                    if m >= (-b + np.sqrt(b**2 - a*c)) / a:
                        m = (-b + np.sqrt(b**2 - a*c)) / a
                        closest = cnt

                if -b - np.sqrt(b**2 - a*c) >= 0:
                    if m >= (-b - np.sqrt(b**2 - a*c)) / a:
                        m = (-b - np.sqrt(b**2 - a*c)) / a
                        closest = cnt

        cnt += 1

    return [m, closest]

def shade(m, ray, viewPoint, surfaceList, idx, lightList):
    if idx == -1:
        return np.array([0,0,0])

    else:
        r = 0
        g = 0
        b = 0
        n = np.array([0,0,0])
        v = -m * ray

        surface = surfaceList[idx]

        if isinstance(surfaceList[idx], Sphere):
            n = viewPoint + m * ray - surfaceList[idx].center
            n = n / np.sqrt(np.sum(n*n))

        for l in lightList:
            light = v + l[0] - viewPoint
            light = light / np.sqrt(np.sum(light * light))

            check = raytrace(-light, l[0], surfaceList)

            if check[1] == idx:
                if isinstance(surface.shader, ShaderLamb):
                    r += surface.shader.diffuse_color[0] * l[1][0] * max(0, np.dot(light, n))
                    g += surface.shader.diffuse_color[1] * l[1][1] * max(0, np.dot(light, n))
                    b += surface.shader.diffuse_color[2] * l[1][2] * max(0, np.dot(light, n))

                elif isinstance(surface.shader, ShaderPhong):
                    v_unit = v / np.sqrt(np.sum(v*v))
                    h = v_unit + light
                    h = h / np.sqrt(np.sum(h*h))

                    r +=  surface.shader.diffuse_color[0] * l[1][0] * max(0, np.dot(light, n)) + surface.shader.specular_color[0] * l[1][0] * pow(max(0, np.dot(n,h)), surface.shader.exponent[0])
                    g += surface.shader.diffuse_color[1] * l[1][1] * max(0, np.dot(light, n)) + surface.shader.specular_color[1] * l[1][1] * pow(max(0, np.dot(n,h)), surface.shader.exponent[0])
                    b += surface.shader.diffuse_color[2] * l[1][2] * max(0, np.dot(light, n)) + surface.shader.specular_color[2] * l[1][2] * pow(max(0, np.dot(n,h)), surface.shader.exponent[0])

            res = Color(r,g,b)
            res.gammaCorrect(2.2)
            return res.toUINT8()

def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir=np.array([0,0,-1]).astype(np.float64)
    viewUp=np.array([0,1,0]).astype(np.float64)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth=1.0
    viewHeight=1.0
    projDistance=1.0
    intensity=np.array([1,1,1]).astype(np.float64)  # how bright the light is.

    #parse image size
    imgSize=np.array(root.findtext('image').split()).astype(np.int32)

    for c in root.findall('camera'):
        viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float64)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float64)
        viewUp = np.array(c.findtext('viewUp').split()).astype(np.float64)
        projNormal = np.array(c.findtext('projNormal').split()).astype(np.float64)

        if(c.findtext('projDistance')):
            projDistance = np.array(c.findtext('projDistance').split()).astype(np.float64)
        viewWidth = np.array(c.findtext('viewWidth').split()).astype(np.float64)
        viewHeight = np.array(c.findtext('viewHeight').split()).astype(np.float64)

    surfaceList = []

    for c in root.findall('surface'):
        if c.get('type') == 'Sphere':
            center = np.array(c.findtext('center').split()).astype(np.float64)
            radius = np.array(c.findtext('radius').split()).astype(np.float64)

            #get shader information
            for tags in c:
                if tags.tag == 'shader':
                    shader_ref = tags.get('ref')

            for d in root.findall('shader'):
                if d.get('name') == shader_ref:
                    diffuseColor_d = np.array(d.findtext('diffuseColor').split()).astype(np.float64)

                    if(d.get('type') == 'Lambertian'):
                        shader = ShaderLamb(diffuseColor_d)
                        surfaceList.append(Sphere(center, radius, shader))

                    elif(d.get('type') == 'Phong'):
                        specularColor_d = np.array(d.findtext('specularColor').split()).astype(np.float64)
                        exponent_d = np.array(d.findtext('exponent').split()).astype(np.float64)
                        shader = ShaderPhong(diffuseColor_d, specularColor_d, exponent_d)
                        surfaceList.append(Sphere(center, radius, shader))

    lightList = []

    for c in root.findall('light'):
        position = np.array(c.findtext('position').split()).astype(np.float64)
        intensity = np.array(c.findtext('intensity').split()).astype(np.float64)
        lightList.append((position, intensity))

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0

    pixelWidth = viewWidth / imgSize[0]
    pixelHeight = viewHeight / imgSize[1]

    x = viewDir
    x = x / np.sqrt(np.sum(x*x))
    y = np.cross(x, viewUp)
    y = y / np.sqrt(np.sum(y*y))
    z = np.cross(x,y)
    z = z / np.sqrt(np.sum(z*z))

    s = x * projDistance - y * pixelWidth * (imgSize[0]/2 + 1/2) - z * pixelHeight * (imgSize[1]/2 + 1/2)

    for i in np.arange(imgSize[0]):
        for j in np.arange(imgSize[1]):
            ray = s + y * i * pixelWidth + z * j * pixelHeight
            traced = raytrace(ray, viewPoint, surfaceList)

            img[j][i] = shade(traced[0], ray, viewPoint, surfaceList, traced[1], lightList)

    rawimg = Image.fromarray(img, 'RGB')
    rawimg.save(sys.argv[1]+'.png')

if __name__=="__main__":
    main()
