#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018-2-10

@author: qi
'''
from wopiserver_django.settings import WOPI_FILE_DIR
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import json
import hashlib
import base64
import os


def file_iterator(filename, chunk_size=512):
    '''read file'''
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def wopiGetFileInfo(request):
    '''Get file info. Implements the CheckFileInfo WOPI call'''
    print('Get file info. Implements the CheckFileInfo WOPI call')
    url = request.GET.get('url', None)
    try:
        file_path = os.path.join(WOPI_FILE_DIR, url)
        rf = open(file_path, 'rb')
        f = rf.read()

        json_data = {'BaseFileName': url.split('/')[-1], 'OwnerId': 'qi', 'Size': len(f)}
        dig = hashlib.sha256(f).digest()
        json_data['SHA256'] = base64.b64encode(dig).decode()
        json_data['Version'] = '1'
        json_data['SupportsUpdate'] = True
        json_data['UserCanWrite'] = True
        json_data['SupportsLocks'] = True
    except Exception as _:
        json_data = {}
    return HttpResponse(json.dumps(json_data, ensure_ascii=False), content_type='application/json; charset=utf-8')


def wopiFileContents(request):
    '''Request to file contents, Implements the GetFile WOPI call'''
    print('Request to file contents, Implements the GetFile WOPI call')
    url = request.GET.get("url", None)
    file_path = os.path.join(WOPI_FILE_DIR, url)
    if (request.method == 'GET'):
        print('get file contents')
        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(url)
        return response
    elif (request.method == 'POST'):
        print('Update file with new contents. Implements the PutFile WOPI call')
        with open(file_path, 'wb+') as f:
            f.write(request.body)
            f.close()
        return HttpResponse('')
