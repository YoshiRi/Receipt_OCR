#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""合計金額を抽出するライブラリ
"""

import re
from basic_util import get_line_texts, load_json

def match_price_string(text):
    pattern = r'[¥\*][ \d,.]+'
    match = re.search(pattern, text)
    if match:
        match_text = match.group()
        for sp_char in [" ",",","."]:
            match_text = match_text.replace(sp_char,"")
        price = match_text[1:]
        return price
    else:
        return ''


def search_gokei_pattern(texts,pattern):
    """
    パターンに合致する行番号のリストを返す
    Args:
         texts: list of string
         pattern: 正規表現のパターン
    """
    
    pattern_matched = []
    for i in range(len(texts)):
        text = texts[i]
        if re.search(pattern,text):
            pattern_matched.append(i)
    return pattern_matched

def search_price_string(texts):
    """
    テキストのリストを{行番号: 金額} のdictにして返す
    """
    price_matched = {}
    for i in range(len(texts)):
        text = texts[i]
        if match_price_string(text):
            price_matched[i] = match_price_string(text)
    return price_matched
    
def match_gokei_price(texts,pattern):
    """
    特定のパターンに合致する金額のstirngを返す。なければ空の文字列を返す。
    """
    pattern_matched = search_gokei_pattern(texts,pattern)
    price_matched = search_price_string(texts)
    
    for idx in pattern_matched:
        try:
            return price_matched[idx]
        except:
            try:
                return price_matched[idx+1]
            except:
                try:
                    return price_matched[idx-1]
                except:
                    continue
        return ''


def extract_gokei_prices_dict(response):
    texts = get_line_texts(response)
    
    gokei_patterns = [r'^[合] ?計', r'買上げ?計', r'対象計']
    shokei_patterns = [r'[小] ?計']
    other_patterns = [r'[現] ?計', r'信用',r'決済',r'金額',r'支払']

    gokei , shokei , other_kei = '','',''

    for gp in gokei_patterns:
        temp = match_gokei_price(texts,gp)
        if temp:
            gokei = temp
            break

    for sp in shokei_patterns:
        temp = match_gokei_price(texts,sp)
        if temp:
            shokei = temp
            break

    for op in other_patterns:
        temp =  match_gokei_price(texts,op)
        if temp:
            other_kei = temp
            break

    gokei_dict = {}
    gokei_dict["合計"] = gokei
    gokei_dict["小計"] = shokei
    gokei_dict["現計等"] = other_kei

    return gokei_dict

def check_valid_prices(gokei_dict, min_price = 21):
    """
    一定の金額以下を排除
    """
    for key in gokei_dict.keys():
        if gokei_dict[key] == '':
            continue
        elif int(gokei_dict[key]) < min_price:
            gokei_dict[key] = ''
        else:
            continue
    return gokei_dict

def get_totalprice_from_response(response):
    """
    合計・小計・現計等から有効そうな金額を選ぶ
    """
    gokei_dict = check_valid_prices(extract_gokei_prices_dict(response))
    
    nonzero = sum([1 if gokei_dict[i] else 0 for i in gokei_dict.keys() ])
    
    if nonzero == 0:
        return ''
    elif nonzero == 1:
        price = ''.join([gokei_dict[i] for i in gokei_dict.keys()])
    else:
        price = decide_valid_gokei_prices(gokei_dict)
    
    return price

def decide_valid_gokei_prices(gokei_dict):
    """有効な金額を選択する

    Args:
        gokei_dict (_type_): 合計、小計、現計等のキーワードに対応する金額の辞書

    Returns:
        String: 有効そうな金額
    """
    gokei  = gokei_dict["合計"]
    shokei = gokei_dict["小計"]
    other_kei = gokei_dict["現計等"]
    
    if shokei == '':
        return gokei
    else:
        taxed_shokei = int(int(shokei) * 1.08)
        taxed_shokei_strs = [str(taxed_shokei), str(taxed_shokei+1)]
        
        if shokei == gokei or shokei == other_kei:
            return shokei
        elif gokei in taxed_shokei_strs:
            return gokei
        elif other_kei in taxed_shokei_strs:
            return other_kei
        elif gokei:
            return gokei
        else:
            return other_kei


if __name__=='__main__':
    import sys
    
    try:
        fname = sys.argv[1]
    except:
        fname = "test/test_1.json"

    response = load_json(fname)
    print(get_totalprice_from_response(response))