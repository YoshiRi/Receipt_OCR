#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""メイン処理
OCRした結果をjsonに格納する

下記の設定を済ませる必要がある
https://cloud.google.com/docs/authentication/getting-started#create-service-account-gcloud

$ export GOOGLE_APPLICATION_CREDENTIALS=<your json file>
"""

import sys
import os
import glob
# parser
from lib.ocr_by_vision_api import ocr_folder_image


def main(folder):
    ocr_folder_image(folder)

    
if __name__=="__main__":
    try:
        folder = sys.argv[1]
    except:
        folder = 'output/'
        
    main(folder)