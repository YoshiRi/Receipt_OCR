#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
結果の可視化用クラス
"""

from enum import Enum

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def draw_boxes(input_file, bounds):
    img = cv2.imread(input_file, cv2.IMREAD_COLOR)
    for bound in bounds:
      p1 = (bound.vertices[0].x, bound.vertices[0].y) # top left
      p2 = (bound.vertices[1].x, bound.vertices[1].y) # top right
      p3 = (bound.vertices[2].x, bound.vertices[2].y) # bottom right
      p4 = (bound.vertices[3].x, bound.vertices[3].y) # bottom left
      cv2.line(img, p1, p2, (0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
      cv2.line(img, p2, p3, (0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
      cv2.line(img, p3, p4, (0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
      cv2.line(img, p4, p1, (0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    return img

def get_document_bounds(response, feature):
    document = response.full_text_annotation
    bounds = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                          bounds.append(symbol.bounding_box)
                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)
                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)
            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)
    return bounds

import cv2
import matplotlib.pyplot as plt
import matplotlib

def draw_API_results(response,input_file):
    bounds = get_document_bounds(response, FeatureType.BLOCK)
    img_block = draw_boxes(input_file, bounds)

    bounds = get_document_bounds(response, FeatureType.PARA)
    img_para = draw_boxes(input_file, bounds)

    bounds = get_document_bounds(response, FeatureType.WORD)
    img_word = draw_boxes(input_file, bounds)

    bounds = get_document_bounds(response, FeatureType.SYMBOL)
    img_symbol = draw_boxes(input_file, bounds)

    plt.figure(figsize=[20,20])
    plt.subplot(141);plt.imshow(img_block[:,:,::-1]);plt.title("img_block")
    plt.subplot(142);plt.imshow(img_para[:,:,::-1]);plt.title("img_para")
    plt.subplot(143);plt.imshow(img_word[:,:,::-1]);plt.title("img_word")
    plt.subplot(144);plt.imshow(img_symbol[:,:,::-1]);plt.title("img_symbol")
