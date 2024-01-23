#!/usr/bin/env python3
from mitmproxy import http
from urllib.parse import urlparse


def response(packet):

    content_type = packet.response.headers.get('content-type', None)

    try:
        if 'image' in content_type:
            url = packet.request.url 
    
            file_name = f"images/{url.replace('/', '_').replace(':', '_').replace('jpeg', 'jpg')}"
            image_raw = packet.response.content 

            print(file_name)
            #print(image_raw)

            with open(file_name, "wb") as f:
                f.write(image_raw)

    except Exception as e:
        pass
    

