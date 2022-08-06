#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Google Vision APIを用いて画像のOCRをするクラス


下記の設定を済ませる必要がある
https://cloud.google.com/docs/authentication/getting-started#create-service-account-gcloud

$ export GOOGLE_APPLICATION_CREDENTIALS=<your json file>
"""

import io
from google.cloud import vision
from google.cloud.vision import AnnotateImageResponse
import json
import os
import glob

class OCR_VisionAPI():
    """Do OCR via gooogle Vision API and save result to json files
    """
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        self.result = {}

    def ocr_image(self,input_file):
        with io.open(input_file, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = self.client.document_text_detection(image=image)
        return response

    def ocr_multiple_images(self, input_files):
        result = {}
        for file in input_files:
            result[file] = self.ocr_image(file)
        return result

    def save_as_json(self, response, filename):
        data = AnnotateImageResponse.to_json(response)
        with open(filename, mode='wt', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
    def load_from_json(self,filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            temp = json.load(file)
        response = AnnotateImageResponse.from_json(temp)
        return response

    def get_json_filename(self, filename, filepath=''):
        basename_without_ext = os.path.splitext(os.path.basename(filename))[0]
        return filepath + basename_without_ext + '.json'

    def scan_and_save(self, input_files):
        status = {}
        for input_file in input_files:
            try:
                response = self.ocr_image(input_file)
                outputdir = 'output'
                os.makedirs(outputdir, exist_ok=True)
                outputfile = self.get_json_filename(input_file, outputdir+'/')
                self.save_as_json(response, outputfile)
                status[input_file] = True
            except Exception as e:
                print(e)
                status[input_file] = False
        return status



def load_from_json(filename):
    """load vision api result from json file

    Args:
        filename (string): json file

    Returns:
        google vision api annotation : response
    """
    with open(filename, mode='r', encoding='utf-8') as file:
        temp = json.load(file)
    response = AnnotateImageResponse.from_json(temp)
    return response



def ocr_folder_image(folder):
    """scan and ocr images in a folder

    Args:
        folder (string): folder path
    """
    file_lists = []
    ftypes = ('*.jpg', '*.JPEG', '*.png')
    for ftype in ftypes:
        file_lists += glob.glob(folder+ftype)
    
    ocr = OCR_VisionAPI()
    status = ocr.scan_and_save(file_lists)
    
    print(status)

if __name__=='__main__':
    import sys
    
    try:
        folder = sys.argv[1]
    except:
        # set current folder
        folder = './'

    ocr_folder_image(folder)
