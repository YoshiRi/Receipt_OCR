#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
全てにおいて使われる基本クラス
""" 

from google.cloud import vision
from google.cloud.vision import AnnotateImageResponse
import json


def load_json(fname):
    """jsonのファイルを読む関数

    Args:
        fname (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        with open(fname, mode='r', encoding='utf-8') as file:
            temp = json.load(file)
        response = AnnotateImageResponse.from_json(temp)
        return response
    except Exception as e:
        print('Loading json is terminated due to following reasons.')
        print(e)
        return None


def get_sorted_lines(response,threshold = 5):
    """Boundingboxの左上の位置を参考に行ごとの文章にParseする

    Args:
        response (_type_): VisionのOCR結果のObject
        threshold (int, optional): 同じ列だと判定するしきい値

    Returns:
        line: list of [x,y,text,symbol.boundingbox]
    """
    # 1. テキスト抽出とソート
    document = response.full_text_annotation
    bounds = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols: #左上のBBOXの情報をx,yに集約
                        x = symbol.bounding_box.vertices[0].x
                        y = symbol.bounding_box.vertices[0].y
                        text = symbol.text
                        bounds.append([x, y, text, symbol.bounding_box])
    bounds.sort(key=lambda x: x[1])
    # 2. 同じ高さのものをまとめる
    old_y = -1
    line = []
    lines = []
    for bound in bounds:
        x = bound[0]
        y = bound[1]
        if old_y == -1:
            old_y = y
        elif old_y-threshold <= y <= old_y+threshold:
            old_y = y
        else:
            old_y = -1
            line.sort(key=lambda x: x[0])
            lines.append(line)
            line = []
        line.append(bound)
    line.sort(key=lambda x: x[0])
    lines.append(line)
    return lines

def get_line_texts(response):
    """OCR 構造物から各行ごとのテキストを抽出

    Args:
        response (_type_): _description_

    Returns:
        _type_: _description_
    """
    lines = get_sorted_lines(response)
    texts = []
    for line in lines:
        texts.append(''.join([i[2] for i in line]))
    return texts
