#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sqlite3


# In[2]:


class SQL(object):
    # Data type
    TYPE_INT = "INT"
    TYPE_INTEGER = "INTEGER"
    TYPE_TINYINT = "TINYINT"
    TYPE_SMALLINT = "SMALLINT"
    TYPE_MEDIUMINT = "MEDIUMINT"
    TYPE_BIGINT = "BIGINT"
    TYPE_UNSIGNED_BIG_INT = "UNSIGNED BIG INT"
    TYPE_INT2 = "INT2"
    TYPE_INT8 = "INT8"
    TYPE_CHARACTER = lambda size: f"CHARACTER({size})"
    TYPE_VARCHAR = lambda size: f"VARCHAR({size})"
    TYPE_VARYING_CHARACTER = lambda size: f"VARYING CHARACTER({size})"
    TYPE_NCHAR = lambda size: f"NCHAR({size})"
    TYPE_NATIVE_CHARACTER = lambda size: f"NATIVE CHARACTER({size})"
    TYPE_NVARCHAR = lambda size: f"NVARCHAR({size})"
    TYPE_TEXT = "TEXT"
    TYPE_CLOB = "CLOB"
    TYPE_UNSPECIFIED = "BLOB"
    TYPE_REAL = "REAL"
    TYPE_DOUBLE = "DOUBLE"
    TYPE_DOUBLE_PRECISION = "DOUBLE PRECISION"
    TYPE_FLOAT = "FLOAT"
    TYPE_NUMERIC = lambda p,s: f"NUMERIC()"
    TYPE_DECIMAL = lambda p,s: f"DECIMAL()"
    TYPE_BOOLEAN = "BOOLEAN"
    TYPE_DATE = "DATE"
    TYPE_DATETIME = "DATETIME"
    # Data option
    OPT_NOTNULL = "NOT NULL"
    OPT_PRIMKEY = "PRIMARY KEY"
    OPT_AUTOINC = "AUTOINCREMENT"
    OPT_UNIQUE = "UNIQUE"
    # Numberic function
    FUNC_COUNT = lambda item: f"COUNT({item})"
    FUNC_SUM = lambda item: f"SUM({item})"
    FUNC_AVG = lambda item: f"AVG({item})"
    FUNC_MAX = lambda item: f"MAX({item})"
    FUNC_MIN = lambda item: f"MIN({item})"
    FUNC_ABS = lambda item: f"ABS({item})"
    FUNC_ROUND = lambda item: f"ROUND({item})"
    FUNC_CEIL = lambda item: f"CEIL({item})"
    FUNC_FLOOR = lambda item: f"FLOOR({item})"
    # String function
    FUNC_LEN = lambda item: f"LENGTH({item})"
    FUNC_CONCAT = lambda array: "CONCAT({})".format(", ".join(array))
    FUNC_UPPER = lambda item: f"UPPER({item})"
    FUNC_LOWER = lambda item: f"LOWER({item})"
    FUNC_INITCAP = lambda item: f"INITCAP({item})"


# In[3]:


class DataBase():

    def __init__(self, link_db: str):
        """[!]READ CLASS SQL ABOVE CAREFULLY TO DEFINE DATA TYPE OF FUNCTION CORRECTLY[!]"""
        self.connection = sqlite3.connect(link_db)
        self.cursor = self.connection.cursor()
        self.sql_syntax = SQL
        self.schedule = []
    
    def create_table(self, name: str, architecture: dict) -> None:
        """[+] Exp:
            architecture = {
                "id": [
                    self.sql_syntax.TYPE_INT,
                    self.sql_syntax.PRIMARY_KEY
                ],
                "name": [
                    self.sql_syntax.TYPE_VARCHAR(225)
                ]
            }
        """
        self.schedule.append(
            [
                "CREATE TABLE {} ({})".format(
                    name,
                    ", ".join(
                        "{} {}".format(key, " ".join(architecture[key]))
                        for key in architecture.keys()
                    )
                ),''
            ]
        )

    def list_items(self, table: list, items='*', condition=None) -> None:
        """[+] Exp:
            -------------
            table = ["staff", "salary"]
                or
            table = "staff"
            -------------
            items = "*"
                or
            items = [
                self.sql_syntax.FUNC_COUNT("ID"),
                self.sql_syntax.FUNC_CONCAT(["first_name", '"-"', "last_name"])
            ]
            -------------
        """
        self.schedule.append(
            [
                "SELECT {} FROM {} {}".format(
                    items if type(items) == str else ",".join(", "),
                    table if type(table) == str else ",".join(", "),
                    '' if not condition else 'WHERE {}'.format(condition)
                ),''
            ]
        )
        
    def insert_data(self, table: str, specify_columns: list, values: list) -> None:
        """[+] Exp:
            -------------
            table = "victim"
            -------------
            specify_columns = []
                or 
            specify_columns = ['id', 'ip addr', 'phone number']
            -------------
            values = [1, '192.168.1.12', 098989889] # it must be a list of string or numberic or both
        """
        self.schedule.append(
            [
                "INSERT INTO {} {} VALUES({})".format(
                    table,
                    '' if not specify_columns else "({})".format(", ".join(specify_columns)),
                    ", ".join(["?"]*len(values))
                ),values
            ]
        )
            

    def run(self) -> list:
        while self.schedule:
            temp = self.schedule.pop(0)
            print(temp)
            self.cursor.execute(temp[0], temp[1])
            result = self.cursor.fetchall()
            if result:
                yield result
        self.connection.commit()


# In[ ]:




