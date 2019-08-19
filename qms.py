# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 23:51:21 2019

@author: Neo Andreson
"""

class qms:
  def __init__(self, server):
    self.server = server
    cursor = self.server.cursor()
    cursor.execute("Use admin;")
    sql = "create table if not exists question_papers (Qid int NOT NULL \
    AUTO_INCREMENT, Title varchar(255) NOT NULL, Time int, NumberOfQuestions int, PRIMARY KEY (Qid));"

    cursor.execute(sql)

  def insert_question(self, text, opt_list, answer):
    if len(opt_list) != 4:
      return False
    val = "('" + text + "',"
    for x in opt_list:
      val += "'" + str(x) + "',"
    val += "'" + answer + "');"
    sql = "insert into qp" + str(self.qid) + " values " + val
    cursor = self.server.cursor()
    cursor.execute(sql)
    self.server.commit()

  def create_new_paper(self, title, time, num):
    val = (title, time, num)
    self.title = title
    cursor = self.server.cursor()
    cursor.execute("Use admin;")
    sql = "insert into question_papers (Title, Time, NumberOfQuestions) \
    values (%s, %s, %s);"
    cursor.execute(sql, val)
    self.server.commit()
    self.qid = self.get_latest_qid()
    self.num = num
    sql = "create table if not exists qp" + str(self.qid) + " \
    (Description varchar(255), A varchar(255), B varchar(255), C varchar(255),\
    D varchar(255), Answer varchar(255));"
    cursor.execute(sql)

  def get_latest_qid(self):
    cursor = self.server.cursor()
    cursor.execute("Use admin;")
    cursor.execute("SELECT Qid FROM question_papers ORDER BY Qid DESC LIMIT 1")
    rec = cursor.fetchall()
    if len(rec) == 0:
      return False
    return int(rec[0][0])

#import mysql.connector
#
#server = mysql.connector.connect(
#  host="localhost",
#  user="root",
#  passwd="1234"
#)
#
#qms_obj = qms(server)
