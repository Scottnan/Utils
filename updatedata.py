# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 10:28:50 2018

@author: wangxin3
"""
import os
import cx_Oracle
import numpy as np
import xlrd
import time
import logging
import getpass


class Xyj_update_data():

    def __init__(self,path_data = r'Z:\data\cn\equity\test',path_file = r'Z:\data\wind数据查询表.xlsx',password = 'readeronly/readeronly@wande'):
        self.lujing = path_data
        self.path_file = path_file
        conn=cx_Oracle.connect(password)
        self.cur=conn.cursor()#游标
        self.username = getpass.getuser()
        self.logger = self.logging_set()
        
    def logging_set(self):
        logger = logging.getLogger()  
        logger.setLevel(logging.INFO)    # Log等级总开关  
          
        # 第二步，创建一个handler，用于写入日志文件  
        logfile = self.lujing+r'\update_log.txt'
        fh = logging.FileHandler(logfile, mode='a')  
        fh.setLevel(logging.DEBUG)   # 输出到file的log等级的开关  
          
        # 第三步，再创建一个handler，用于输出到控制台  
        ch = logging.StreamHandler()  
        ch.setLevel(logging.WARNING)   # 输出到console的log等级的开关  
          
        # 第四步，定义handler的输出格式  
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")  
        fh.setFormatter(formatter)  
        ch.setFormatter(formatter)  
          
        # 第五步，将logger添加到handler里面  
        logger.addHandler(fh)  
        logger.addHandler(ch)  
        return logger
        
    def mkdir(self,path):
        path = path.lower()
        folder = os.path.exists(path)
        if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        else:
            pass
    		
    def update(self,cur,lujing,table_type,table_name,date_index):
    
    
        sql = "select column_name,column_id,data_type from all_tab_columns where Table_Name= '" + table_name.upper() + "'"
        cur.execute(sql)
        data_column = cur.fetchall()#所有记录
        
        data_column = np.array(data_column)
        column = list(data_column[np.lexsort([np.array(list(map(int,data_column[:,1])))]),0])
        
        data_type = list(data_column[np.lexsort([np.array(list(map(int,data_column[:,1])))]),-1])
        remove_id = ['OBJECT_ID','OPDATE','OPMODE','RATING_MEMO']
        for key in remove_id:
            try:
                data_type.remove(data_type[column.index(key)])
                column.remove(key)
            except:
                pass
        columns = ",".join(column)
        
        data_type = (",".join(data_type)).replace('VARCHAR2','STRING').split(",")
            
        sql = "select " + columns + " from " + table_name
        
        
        if date_index != '':
            file_lists = os.listdir(lujing + "\\" + table_type + "\\" + table_name)
            if len(file_lists) > 1:
                date = []
                for file in file_lists:
                    try:
                        date.append(int(file[:-4]))
                    except:
                        pass
                date = np.max(date)
            else:
                date = 0
                self.update_all(cur,lujing,table_type,table_name,date_index)
                return
            sql = sql + " where " + date_index + " >= " + str(date)
            cur.execute(sql)
            data_update = cur.fetchall()#所有记录
            data_update2 = np.array(data_update)
            
            date = list(np.unique(data_update2[:,column.index(date_index)]))
            
            for i in date:
                a = data_update2[data_update2[:,column.index(date_index)] == i]
                file = lujing + "\\" + table_type + "\\" + table_name +"\\"+str(i)+'.txt'
                with open(file,'w') as f:
                    f.write(("|".join(column) + "\n").lower())
                    for j in a:
                        b = [str(x) for x in j]
                        f.write(("|".join(b) + "\n").replace("None",""))
            file = lujing + "\\" + table_type + "\\" + table_name +"\\summary.txt"
            with open(file,'w') as f:
                f.write("header|type\n")
                for i in range(len(column)):
                    f.write(("|".join([column[i],data_type[i]]) + "\n").lower())
        else:
            cur.execute(sql)
            data_update = cur.fetchall()#所有记录
            file = lujing + "\\" + table_type + "\\" + table_name +"\\"+ table_name +'.txt'
            with open(file,'w') as f:
                f.write(("|".join(column) + "\n").lower())
                for j in data_update:
                    b = [str(x) for x in j]
                    f.write(("|".join(b) + "\n").replace("None",""))
            file = lujing + "\\" + table_type + "\\" + table_name +"\\summary.txt"
            with open(file,'w') as f:
                f.write("header|type\n")
                for i in range(len(column)):
                    f.write(("|".join([column[i],data_type[i]]) + "\n").lower())
    
    def update_all(self,cur,lujing,table_type,table_name,date_index):
        
        sql = "select column_name,column_id,data_type from all_tab_columns where Table_Name= '" + table_name.upper() + "'"
        cur.execute(sql)
        data_column = cur.fetchall()#所有记录
        
        data_column = np.array(data_column)
        column = list(data_column[np.lexsort([np.array(list(map(int,data_column[:,1])))]),0])
        data_type = list(data_column[np.lexsort([np.array(list(map(int,data_column[:,1])))]),-1])
        remove_id = ['OBJECT_ID','OPDATE','OPMODE','RATING_MEMO']
        for key in remove_id:
            try:
                data_type.remove(data_type[column.index(key)])
                column.remove(key)
            except:
                pass
        columns = ",".join(column)
        
        data_type = (",".join(data_type)).replace('VARCHAR2','STRING').split(",")
            
        #sql = "select " + columns + " from " + table_name
        date_first = 19800101
        enddate = 19800001
        num = 1
        while enddate < int(time.strftime('%Y%m%d',time.localtime(time.time()))):
            startdate,enddate = date_first + 10000 * num,date_first + 10000 * (num-1)
            sql = "select " + columns + " from " + table_name
            try:
                sql = sql + " where " + date_index + " >= " + str(enddate) + " and " + date_index + " <= " + str(startdate)
                cur.execute(sql)
                data_update = cur.fetchall()#所有记录
                data_update2 = np.array(data_update)
                
                date = list(np.unique(data_update2[:,column.index(date_index)]))
                
                for i in date:
                    a = data_update2[data_update2[:,column.index(date_index)] == i]
                    file = lujing + "\\" + table_type + "\\" + table_name +"\\"+str(i)+'.txt'
                    with open(file,'w') as f:
                        f.write(("|".join(column) + "\n").lower())
                        for j in a:
                            b = [str(x) for x in j]
                            f.write(("|".join(b) + "\n").replace("None",""))
            except:
                pass
            num = num + 1
        file = lujing + "\\" + table_type + "\\" + table_name +"\\summary.txt"
        with open(file,'w') as f:
            f.write("header|type\n")
            for i in range(len(column)):
                f.write(("|".join([column[i],data_type[i]]) + "\n").lower())
                
    
    
               
    def read_index(self,path_file):
        file = xlrd.open_workbook(path_file)
        table = file.sheets()[0]   #获取第一个sheet
        table_name = []
        table_type = []
        table_dateindex = []
        for i in range(1,table.nrows):
            row = table.row_values(i)      #读取第i行的数据
            table_type.append(row[2])
            table_name.append(row[0].upper())
            table_dateindex.append(row[3])
        return table_type,table_name,table_dateindex
    
    def main(self):
        table_type,table_name,table_dateindex = self.read_index(self.path_file)
        fail_name = []
        message = {}
        message['author'] = self.username
        for i in range(len(table_type)):
            self.mkdir(self.lujing + "\\" + table_type[i])
            self.mkdir(self.lujing + "\\" + table_type[i] + "\\" + table_name[i])
            message['table_type'] = table_type[i]
            message['table_name'] = table_name[i]
            
            try:
                self.update(self.cur,self.lujing,table_type[i],table_name[i],table_dateindex[i])
                message['update_result'] = 'success'
                self.logger.info(str(message))
            except:
                message['update_result'] = 'failed'
                self.logger.info(str(message))
                fail_name.append(table_name[i])
        self.logger.info("filed table:" + str(fail_name))
        return fail_name


if __name__ == '__main__':
    
    Xyj_update_data = Xyj_update_data(path_data = r'Z:\data\cn\equity\test',path_file = r'Z:\data\wind数据查询表.xlsx',password = 'readeronly/readeronly@wande')
    Xyj_update_data.main()