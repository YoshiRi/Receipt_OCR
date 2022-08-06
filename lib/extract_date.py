#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""日付を抽出するライブラリ
"""

import re
from basic_util import get_sorted_lines, load_json


def matching_date_pattern(texts, pattern=None):
    pattern = pattern if pattern else r'[12]\d{3}[/\-年 ](0?[1-9]|1[0-2])[/\-月 ]([12][0-9]|3[01]|0?[0-9])(日?)'
    if re.search(pattern,texts):
        return re.search(pattern,texts).group(0).replace(' ','/')
    else:
        return ''

def extract_date(lines):
    for line in lines:
        texts = [i[2] for i in line]
        texts = ''.join(texts)
        date = matching_date_pattern(texts)
        if date:
            return date
    return ''


def symbol_width(symbol):
    return symbol.bounding_box.vertices[1].x - symbol.bounding_box.vertices[0].x

def symbol_height(symbol):
    return symbol.bounding_box.vertices[3].y - symbol.bounding_box.vertices[0].y


def extract_words(response):
    """
    words単位でテキストをリスト化。スペースが空いている場合は半角スペースを挿入
    """
    document = response.full_text_annotation
    words = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:    
                for word in paragraph.words:
                    # word 単位で処理
                    texts = ''
                    last_left_x = - 1e6
                    # word内の文字を結合
                    for symbol in word.symbols: 
                        left_x = symbol.bounding_box.vertices[0].x
                        # 行間が文字の横幅と縦幅の和より大きいならば、半角スペースを挿入
                        if left_x - last_left_x > symbol_width(symbol)+symbol_height(symbol):
                            texts += ' ' + symbol.text
                        else:
                            texts += symbol.text
                        last_left_x = left_x
                    words.append(texts[1:]) # 先頭の半角スペースを排除して抽出
    return words


def search_monthdate_string(wordlist):
    """
    stringのリストから正規表現でXX/YYとなりうる最初の月日を検索。ない場合は空の文字列を返す。
    """
    newlist = []
    for word in wordlist:
        word_ = ' '.join(re.findall(r"\d+", word))
        if word_:
            newlist.append(word_)
    
    monthdate_candidate = '/'.join(newlist).replace(' ','/')
    #print(monthdate_candidate)
    monthdate_match = re.search(r'(0?[1-9]|1[0-2])[/]([12][0-9]|3[01]|0?[0-9])($|/)?', monthdate_candidate)
    if monthdate_match:
        #print(monthdate_match)
        return '/'.join(re.findall(r"\d+", monthdate_match.group()))
    else:
        return ''    

    
def find_date_from_year(response, yearlist=['2021','2022']):
    """
    特定の年のパターンに合致する日付を返す。なければからの文字列を返す。
    """
    words = extract_words(response)
    year_matched = ''
    for i in range(len(words)):
        word = words[i]
        # そのまま日付にマッチングする場合
        if matching_date_pattern(word):
            return matching_date_pattern(word).replace(' ','/')
        # 年だけにマッチングする場合
        if word in yearlist:
            searched_date = search_monthdate_string(words[i+1:i+6]) # 月日なども考慮
            if searched_date:
                return word+'/'+searched_date
            else:
                return searched_date
            # 何もなければ空の文字列を返す
    return ''


def get_date_from_response(response):
    """responseを受け取ってDateを返す
    """
    lines = get_sorted_lines(response)
    date = extract_date(lines)
    if date:
        return date
    else:
        date = find_date_from_year(response)
        if date:
            return date
        else:
            print("No Date Pattern Extracted!")
            return ""


if __name__=='__main__':
    import sys
    
    try:
        fname = sys.argv[1]
    except:
        fname = "test/test_1.json"

    response = load_json(fname)
    print(get_date_from_response(response))