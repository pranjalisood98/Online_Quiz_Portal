# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 14:50:19 2019

"""

class ums:
  def __init__(self, server):
    self.server = server
    
  def register(self, username, password, admin=True):
    val = (username, password)
    cursor = self.server.cursor()
    if admin:
      cursor.execute("USE admin;")
    else:
      cursor.execute("USE student;")
    
    sql = "select username from users where username= '" + username + "';"
    cursor.execute(sql)
    rec = cursor.fetchall()
    if len(rec) != 0:
      return False
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(sql, val)
    self.server.commit()
    return True
  
  def login(self, username, password, admin=True):
#    val = (username, password)
    cursor = self.server.cursor()
    if admin:
      cursor.execute("USE admin;")
    else:
      cursor.execute("USE student;")
    
    sql = "select password from users where username= '" + username + "';"
    cursor.execute(sql)
    rec = cursor.fetchall()
    if len(rec) == 0:
      return False
    if rec[0][0] == password:
      return True
    else: 
      return False
    
    
import mysql.connector

server = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="1234"
)

ums_obj = ums(server)
check = ums_obj.register("naman","1234", admin=False)
print(check)