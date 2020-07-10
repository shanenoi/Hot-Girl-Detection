#!/usr/bin/env python
# coding: utf-8

# In[1]:


from lib_supporter.db_management_libs import *
from lib_supporter.lib_other import *
from os import mkdir, getcwd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import re
import time


# In[2]:


user_account = {
    "email": "automail.robort@yandex.com",
    "pass": "fGwk093oiVtdJPuc8z2wtFjGcvzSi6eonkvWTjZa8glIE6uYJdvLTJv9dJWJVDgMy68Bozma3kKGkWDw"
}


# In[3]:


dataset_folder = "./data"

def init_folder(name, specified_folder:str=".") -> str:
    path = f'{getcwd()}/{specified_folder}/{name}'
    print(path)
    try:
        mkdir(path)
    except Exception as error:
        print(error)
    finally:
        return path

temp = init_folder('temp', dataset_folder)
users_folder = init_folder('database', dataset_folder)
users_images = init_folder('images', dataset_folder)


# In[4]:


options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})


# In[5]:


driver = webdriver.Chrome(
    chrome_options=options,
    executable_path=ChromeDriverManager().install()
)


# In[6]:


web_ctrl = WebControl(driver)


# In[7]:


# Login
web_ctrl.driver.get('https://facebook.com')

mail_holder = web_ctrl.driver.find_element_by_id('email')
mail_holder.clear()
mail_holder.send_keys(user_account['email'])

pass_holder = web_ctrl.driver.find_element_by_id('pass')
pass_holder.clear()
pass_holder.send_keys(user_account['pass'])

web_ctrl.driver.find_element_by_id('u_0_b').click()


# In[8]:


current_task = CurrentTask('create_db_and_download_images')
current_task.source(f'{temp}/user')


# In[9]:


sql = SQL
DB_ARCHITECTURE = {
    "images": {
        "images": [
            # internal path
            sql.TYPE_TEXT
        ],
        "faces": [
            # this field will content faces and its id.
            # x0;y0;x0+w0;y0+h0:id1|x1;y1;x1+w1;y1+h1:id2 ....
            sql.TYPE_TEXT
        ],
        "result": [
            # this field will content faces id and gender, beauty classified
            # male:id1;id2;id3|female_1:id4;id5;id6|female_1:id7;id8;id9
            sql.TYPE_TEXT
        ]
    },
    "friends": {
        "friends": [
            sql.TYPE_TEXT
        ],
    }
    
}


# In[10]:


class Pers(object):
    
    def __init__(self, web_control, user_id):
        self.user_db = DataBase(f'{users_folder}/{user_id}.db')
        self.user_id = user_id
        self.web_ctrl = web_control
        self.web_ctrl.driver.get(f'https://facebook.com/{user_id}')
    
    def get_user_name(self):
        return self.web_ctrl.driver.execute_script(
            CrawlingJs\
            .convert_jsScript(
                CrawlingJs\
                .crawling_by_js['user_name']
            )
        )
    
    def load_more(self):
        self.web_ctrl.driver.execute_script(
            CrawlingJs\
            .convert_jsScript(
                CrawlingJs\
                .crawling_by_js['scroll_to_the_end_of_page']
            )
        )
        
    @staticmethod
    def get_image_name_and_size(url: str) -> list:
        full_url = re.findall('(https://[^()]+)', url)[0]
        result = re.findall('(\d+x\d+)|(\w+.jpg)',full_url)
        return [
            f'{result[0][0]}__{result[1][1]}',
            full_url
        ]
    
    @staticmethod
    def get_friend_name(url: str) -> str:
        return re.findall(
            'https://www.facebook.com/((profile\.php\?id=\d+)|([^/?]+))',
            url
        )[0][0]
        
    def get_list_friends(self):
        return map(
            self.get_friend_name,
            self.web_ctrl.driver.execute_script(
                CrawlingJs\
                .convert_jsScript(
                    CrawlingJs\
                    .crawling_by_js['list_friends']
                )
            )
        )
    
    def get_list_images(self):
        return map(
            self.download_image,
            self.web_ctrl.driver.execute_script(
                CrawlingJs\
                .convert_jsScript(
                    CrawlingJs\
                    .crawling_by_js['list_images']
                )
            )
        )
    
    def download_image(self, url):
        values = self.get_image_name_and_size(url)
        internal_path = f'{users_images}/{values[0]}'
        if not current_task.isdone(values[0]):
            with open(internal_path, 'wb') as imf:
                imf.write(self.web_ctrl.get_content(values[1]))
            current_task.add(values[0])
        else:
            print(f"[+] {values[0]} was downloaded!")
        return internal_path
    
    def create_userdb(self):
        if not current_task.isdone(self.user_id):
            for table in DB_ARCHITECTURE.keys():
                self.user_db.create_table(
                    name=table,
                    architecture=DB_ARCHITECTURE[table]
                )
            current_task.add(self.user_id)
        else:
            print(f"[+] {self.user_id} was created!")
        # because this function will return generator
        list(self.user_db.run())
            
    def save(self, n_friends:int = 0, n_images: int = 0):
        """
        [+] n_friends: the number of scrolling to the bottom of friends page
        [+] n_images: the number of scrolling to the bottom of images page
        """
        self.web_ctrl.driver.execute_script(
                CrawlingJs\
                .convert_jsScript(
                    CrawlingJs\
                    .crawling_by_js['friends']
                )
        )
        current = self.web_ctrl.driver.execute_script(
                CrawlingJs\
                .convert_jsScript(
                    CrawlingJs\
                    .crawling_by_js['length_page']
                )
        )
        for i in range(n_friends):
            while (self.web_ctrl.driver.execute_script(
                    CrawlingJs\
                    .convert_jsScript(
                        CrawlingJs\
                        .crawling_by_js['length_page']
                    )
            ) == current):
                self.web_ctrl.driver.execute_script(
                    CrawlingJs\
                    .convert_jsScript(
                        CrawlingJs\
                        .crawling_by_js['scroll_to_the_end_of_page']
                    )
                )
                current = self.web_ctrl.driver.execute_script(
                    CrawlingJs\
                    .convert_jsScript(
                        CrawlingJs\
                        .crawling_by_js['length_page']
                    )
                )
        friends = list(self.get_list_friends())
        self.web_ctrl.driver.execute_script(
            "console.log('hello');"
        )
        time.sleep(3)
        
        self.web_ctrl.driver.execute_script(
                CrawlingJs\
                .convert_jsScript(
                    CrawlingJs\
                    .crawling_by_js['images']
                )
        )
        current = self.web_ctrl.driver.execute_script(
                CrawlingJs\
                .convert_jsScript(
                    CrawlingJs\
                    .crawling_by_js['length_page']
                )
        )
        for i in range(n_images):
            while (self.web_ctrl.driver.execute_script(
                    CrawlingJs\
                    .convert_jsScript(
                        CrawlingJs\
                        .crawling_by_js['length_page']
                    )
            ) == current):
                self.web_ctrl.driver.execute_script(
                    CrawlingJs\
                    .convert_jsScript(
                        CrawlingJs\
                        .crawling_by_js['scroll_to_the_end_of_page']
                    )
                )
                current = self.web_ctrl.driver.execute_script(
                    CrawlingJs\
                    .convert_jsScript(
                        CrawlingJs\
                        .crawling_by_js['length_page']
                    )
                )
        images = list(self.get_list_images())
        time.sleep(3)

        while images or friends:
            if images:
                self.user_db.insert_data(
                    table="images",
                    specify_columns=['images'],
                    values=[images.pop(0)]
                )
            if friends:
                self.user_db.insert_data(
                    table="friends",
                    specify_columns=['friends'],
                    values=[friends.pop(0)]
                )
        list(self.user_db.run())


# In[11]:


p = Pers(web_ctrl, 'profile.php?id=100006220096058')
p.create_userdb()


# In[12]:


p.save(
    n_friends=6,
    n_images=6
)


# In[ ]:




