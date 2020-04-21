#!/usr/bin/env python
# coding: utf-8

# In[2]:


from selenium import webdriver

import requests
import re


# In[8]:


class WebControl(object):
    
    def __init__(self, driver: webdriver):
        self.driver = driver

        
    @staticmethod
    def get_content(url: str) -> bytes:
        return requests.get(url).content

    
    def execute_js_script(self, script: str) -> None:
        try:
            return self.driver.execute_script(script)
        except Exception as error:
            print(f"Error at {self}: {error} with script: {script}")
            return False

        
    def scroll_to_end(self) -> None:
        self.execute_js_script("window.scrollTo(0,document.body.scrollHeight);")


# In[4]:


class CrawlingJs(object):
    
    crawling_by_js = {
        "list_friends": {
            "type": "list",
            "function": "document.getElementsByClassName",
            "value": "fsl fwb fcb",
            "attribute": "getElementsByTagName('a')[0].getAttribute('href')"
        },
        "list_images": {
            "type": "list",
            "function": "document.getElementsByClassName",
            "value": "uiMediaThumbImg",
            "attribute": "getAttribute('style')"
        },
        "user_name": {
            "type": "str",
            "function": "document.getElementById",
            "value": "fb-timeline-cover-name",
            "attribute": "innerText"
        },
        "scroll_to_the_end_of_page": {
            "type": "void",
            "function": "window.scrollTo",
            "value": "0,document.body.scrollHeight"
        },
        "length_page": {
            "type": "attribute",
            "function": "document.body.scrollHeight"
        }
    }
    
    default_link = {
        "list_friends": "https://www.facebook.com/{}/friends",
        "list_images": "https://www.facebook.com/{}/photos"
    }
    
    @staticmethod
    def convert_jsScript(meta: dict) -> str:
        if meta['type'] == 'list':
            return (
                'temp = {}("{}");\n' +
                'result = [];\n'
                'for(var i=0; i<temp.length; i++) {{\n' +
                '    result.push(temp[i].{})\n' +
                '}}\n' +
                'return result;'
            ).format(
                meta['function'],
                meta['value'],
                meta['attribute']
            )
        
        elif meta['type'] == 'str':
            return 'return {}("{}").{}'.format(
                meta['function'],
                meta['value'],
                meta['attribute']
            )
        
        elif meta['type'] == 'void':
            return "return {}({})".format(
                meta['function'],
                meta['value']
            )
        
        elif meta['type'] == 'attribute':
            return "return {}".format(
                meta['function']
            )


# In[5]:


class CurrentTask(object):
    """
        [-] Save Process
        [-] You can use it for
            [+] URL scanning
            [+] Array processing
            ...
        [-] Come from https://github.com/shanenoi/Crawling/blob/master/lib_for_crawling.py#L33
    """

    def __init__(self, file_name: str):
        try:
            self.file = open(file_name, 'r+')
        except FileNotFoundError:
            self.file = open(file_name, 'w+')

    def add(self, container) -> None:
        self.file.write(
            self.hash_object(container)
        )

        
    @staticmethod
    def __hash(value, p_num: int = 3264) -> str:
        ar = [str(ord(i)) for i in str(value)]
        temp = sorted([int(''.join(ar)), p_num])
        temp = str(temp[0] / temp[1])
        return temp.replace('e-', '').replace('.', '')

    
    def hash_object(self, value):
        return self.__hash(str(
            value.__repr__()
        ))

    
    def isdone(self, container) -> bool:
        self.file.seek(0)
        return self.hash_object(container) in self.file.read()