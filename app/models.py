from flask_login import UserMixin
from . import login_manager, mysql
import json

class User(UserMixin):
    def __init__(self, username, access):
        self.username = username
        self.access = access
    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    cur = mysql.connection.cursor()
    cur.execute("Select username,vender from login where username='"+username+"'")
    data = cur.fetchone()
    return User(data[0],data[1])

class Database():
    def login(username,password):
        cur = mysql.connection.cursor()
        cur.execute("Select * from login where username='"+username+"' and password='"+password+"'")
        data = cur.fetchone()
        if data:
            return True
        else:
            return False

    def getUser(username):
        cur = mysql.connection.cursor()
        cur.execute("Select * from admin where username ='"+ username+"'")
        data = cur.fetchone()
        if cur.rowcount != 0:
            return data
        cur.execute("Select * from vender where username ='"+username+"'")
        data = cur.fetchone()
        if cur.rowcount != 0:
            return data
        return "No data found"

    def addUser(data):
        cur = mysql.connection.cursor()
        try:
            if data['type'] == 'admin':
                cur.execute("insert into admin(username,password) values('"+data['username']+"','"+data['password']+"')")
            else:
                cur.execute("insert into vender(firm, \
                    firm_url,username,password,user_fname,mobile_no, \
                    pan_no,tan_no,vat_no) values('"+data['firm']+"','"+data['firm_url']+\
                    "','"+data['username']+\
                    "','"+data['password']+"','"+data['user_fname']+\
                    "','"+data['mobile_no']+"','"+data['pan_no']+"','"+data['tan_no']+\
                    "','"+data['vat_no']+"')")
        except Exception as e:
            print(e)
            return False
        mysql.connection.commit()
        return True
    
    def addProject(data):
        cur = mysql.connection.cursor()
        try:
            cur.execute("insert into project(title, state, district, project_category, bid_start_date,\
                bid_end_date) values('"+data['title']+"','"+data['state']+"','"+data['district']+"','"+data['project_category']+\
                "','"+data['bid_start_date']+"','"+data['bid_end_date']+"')")
            mysql.connection.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def getProject(project_id):
        cur = mysql.connection.cursor()
        try:
            cur.execute("Select * from project where project_id = '"+project_id+"'")
            data = cur.fetchone()
            return data
        except Exception as e:
            print(e)
            return False

    def addBid(data):
        cur = mysql.connection.cursor()
        cur.execute("insert into bidding(vender_id,tender_id, \
            project_id,cost,date \
                ) values('"+data['vender_id']+"','" \
                    +data['tender_id']+"','"+data['project_id']+"','"+data['cost']+\
                    "','"+data['date']+"')")
        mysql.connection.commit()
        return True

    def search_by(data):
        cur = mysql.connection.cursor()
        if data['method']=='project_category':
            cur.execute("select * from tender_category where tender_category_name='"+data['data']+"'")
            dept = cur.fetchone()
            if not dept:
                return []
            data['data'] = str(dept[0])
        cur.execute("select * from project where "+data['method']+"='"+data['data']+"'")
        data = cur.fetchall()
        if len(data)>0:
            data = list(data)
            for i in range(len(data)):
                data[i] = list(data[i])
                data[i][5] = data[i][5].strftime('%Y-%m-%d')
                data[i][6] = data[i][6].strftime('%Y-%m-%d')
            return json.dumps(data)
        else:
            return []
    def getContractor(uname):
        cur = mysql.connection.cursor()
        cur.execute("select * from vender where username = '"+uname+"'")
        data = cur.fetchone()
        return data
    
'''
    def search_by_state(data)
        cur = mysql.connection.cursor()
        cur.execute("select * from project where state='%s'",data)
        data = cur.fetchall()
        return data

    def search_by_district(data)
        cur = mysql.connection.cursor()
        cur.execute("Select * from project where district='%s'",data)
        data = cur.fetchall()
        return data
'''             
