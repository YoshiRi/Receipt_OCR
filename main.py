#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""メイン処理
OCRした結果が格納されているjsonのフォルダを用いてcsvを作成する
"""

import pandas as pd
import sys
import os
import glob
import tqdm
# parser
from lib.ocr_by_vision_api import load_from_json
from lib.extract_shopname import get_shop_name_from_response
from lib.extract_date import get_date_from_response
from lib.extract_price import get_totalprice_from_response



class ZaimCSVGenerator():
    def __init__(self):
        self.columns = ["date", "shopname", "price", "category"]
        self.df = pd.DataFrame(columns=self.columns)
    
    def output_csv(self,fname):
        self.df.to_csv(fname, index=False)

    def get_csv_from_json_files(self,folder):

        json_files = glob.glob(folder+"*.json")
        for jf in tqdm.tqdm(json_files):
            response = load_from_json(jf)
            date = get_date_from_response(response)
            shopname = get_shop_name_from_response(response)
            price = get_totalprice_from_response(response)
            self.add_receipt_to_row(date,shopname,price)
            
            
    def add_receipt_to_row(self, date=None, shopname=None, price=None, category=None):
        """append to dataframe
        """        
        pd_part = pd.Series([date, shopname, price, category], index=self.columns)
        self.df = self.df.append(pd_part, ignore_index=True)
        
        
        
def main(folder):
    csv_gen = ZaimCSVGenerator()
    csv_gen.get_csv_from_json_files(folder)
    csv_gen.output_csv(folder+'csvdata.csv')    

    
if __name__=="__main__":
    try:
        folder = sys.argv[1]
    except:
        folder = 'output/'
        
    main(folder)