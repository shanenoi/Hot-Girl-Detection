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
        "friends": {
            "type": "str",
            "function": "document.querySelectorAll",
            "value": '[data-tab-key="friends"]',
            "attribute": "item(0).click()"
        },
        "images": {
            "type": "str",
            "function": "document.querySelectorAll",
            "value": '[data-tab-key="photos"]',
            "attribute": "item(0).click()"
        },
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
    
    @staticmethod
    def convert_jsScript(meta: dict) -> str:
        if meta['type'] == 'list':
            return (
                """temp = {}('{}');\n""" +
                """result = [];\n""" +
                """for(var i=0; i<temp.length; i++) {{\n""" +
                """    result.push(temp[i].{})\n""" +
                """}}\n""" +
                """return result;"""
            ).format(
                meta['function'],
                meta['value'],
                meta['attribute']
            )
        
        elif meta['type'] == 'str':
            return """return {}('{}').{}""".format(
                meta['function'],
                meta['value'],
                meta['attribute']
            )
        
        elif meta['type'] == 'void':
            return """{}({})""".format(
                meta['function'],
                meta['value']
            )
        
        elif meta['type'] == 'attribute':
            return """return {}""".format(
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

    def __init__(self, section_id: str):
        """
            * define inital section id
        """
        self.file = None
        self.section = section_id

    def source(self, file_name: str) -> None:
        """
            * Specify source to save processes
        """
        try:
            self.file = open(file_name, 'r+')
        except FileNotFoundError:
            self.file = open(file_name, 'w+')

    @staticmethod
    def __crossbreed(sentence1: str, sentence2: str) -> str:
        sentence1, sentence2 = (
            [sentence2, sentence1]
            if len(sentence1) < len(sentence2)
            else [sentence1, sentence2]
        )
        result = ''
        for index in range(len(sentence1)):
            if index < len(sentence2):
                result += chr(
                    ord(sentence1[index]) + ord(sentence2[index])
                )
            else:
                result += chr(
                    ord(sentence1[index]) + 32 # space
                )
        return result

    def add(self, container: object) -> None:
        """
            * Save process name what you done
        """
        if not self.isdone(container):
            self.file.write(
                self.__crossbreed(
                    self.section, str(container)
                )
            )
        else:
            print(f"[{self.section}]: {container} is available!")
    
    def isdone(self, container: object) -> bool:
        """
            * Check this process
        """
        self.file.seek(0)
        return self.__crossbreed(
                self.section, str(container)
        ) in self.file.read()