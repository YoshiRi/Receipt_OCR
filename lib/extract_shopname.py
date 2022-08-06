#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""店名を抽出するライブラリ
"""

import re
from basic_util import get_sorted_lines, load_json


def get_shop_name_from_response(response):
    """まとめて実行する用
    """
    lines = get_sorted_lines(response)
    return get_shop_name(lines)

def get_shop_name(lines):
    """上から3行抽出してバウンディングボックスが一番縦に大きいものを店名として抽出
    Args:
        lines (_type_): OCR結果を集約したリスト
    Returns:
        string: 店名
    """
    heights_and_texts = []
    for i in range(3):
        line = lines[i]
        texts = [i[2] for i in line]
        texts = ''.join(texts)
        bbx = [i[3] for i in line]
        height = []
        for bb in bbx:
            height.append(calc_bbox_height(bb))
        average_height = sum(height)/len(height)
        heights_and_texts.append([average_height,texts])

    # ソートしてみる
    biggest_bbox = sorted(heights_and_texts, key=lambda x:x[0])[-1]
    return biggest_bbox[1]

def calc_bbox_height(bbx):
    ymax = 0
    ymin = 1e9
    for vt in bbx.vertices:
        ymax = max(ymax,vt.y)
        ymin = min(ymin,vt.y)
    return ymax - ymin    

if __name__=='__main__':
    import sys
    
    try:
        fname = sys.argv[1]
    except:
        fname = "test/test_1.json"

    response = load_json(fname)
    print(get_shop_name_from_response(response))