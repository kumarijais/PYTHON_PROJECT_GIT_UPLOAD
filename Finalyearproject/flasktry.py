import os
import tokentry
import time
import math
import docx2txt
import requests
import  mysql.connector
from flask import Flask,render_template,request,redirect,session,abort,json,send_from_directory,flash
from werkzeug.utils import secure_filename
from flask import Mail, Message

ANSWER_FOLDER='./answersubmissions'
UPLOAD_FOLDER = './uploads'
ANS_EXTENSIONS=set(['txt'])
ALLOWED_EXTENSIONS = set(['txt','doc','docx'])

'''def func_cookies():
    print("Hello")
    s=requests.session()
    s.get('http://httpbin.org/cookies/set',params={'foo':'bar'})
    s.cookies.keys()
    s.get('http://httpbin.org/cookies').json()
    s.cookies.clear()
    s.cookies.keys()
    s.get('http://httpbin.org/cookies').json()'''

app = Flask(__name__)
app.secret_key = 'random string'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ANSWER_FOLDER']=ANSWER_FOLDER
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'onlinesystem2k17@gmail.com'
app.config['MAIL_PASSWORD'] = 'mckvie@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_ansfile(ansfilename):
    return '.' in ansfilename and \
           ansfilename.rsplit('.', 1)[1].lower() in ANS_EXTENSIONS

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] =  "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = 'public, max-age=0'
    return r

@app.route('/')
def main():
    #name = {"First": "Ankit", "Last": "Gaurav"}
    return render_template('home.html')

@app.route('/tlogin')
def tlogin():
    return render_template("teacherlogin.html")

@app.route('/slogin')
def slogin():
    return render_template("studentlogin.html")

@app.route('/alogin')
def alogin():
    return render_template("Adminlogin.html")

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/avalidateLogin', methods=['POST'])
def avalidateLogin():
    try:
        _username = request.form['t1']
        _password = request.form['t2']
       # con = mysql.connect()
        #cursor = con.cursor()
        cnx = mysql.connector.connect(user='root', password='Mehwash', host='127.0.0.1', database='finalyear')
        curs = cnx.cursor()
        curs.execute("select * from admin where username=%s and password=%s",(_username,_password,))
        data = curs.fetchall()
        curs.close()
        cnx.close()
        if len(data) > 0:
            session['auser'] = _username
            return render_template("adminprofile.html")
        else:
            return render_template('error.html', error='Wrong Email address or Password.')
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/tvalidateLogin', methods=['POST'])
def tvalidateLogin():
    try:
        _username = request.form['t1']
        _password = request.form['t2']
       # con = mysql.connect()
        #cursor = con.cursor()
        cnx = mysql.connector.connect(user='root', password='Mehwash', host='127.0.0.1', database='finalyear')
        curs = cnx.cursor()
        curs.execute("select * from teacher where username=%s and password=%s",(_username,_password,))
        data = curs.fetchall()
        curs.close()
        cnx.close()
        if len(data) > 0:
            session['tuser'] = _username
            return render_template("teacherprofile.html",name=session['tuser'])
        else:
            return render_template('error.html', error='Wrong Email address or Password.')
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/svalidateLogin', methods=['POST', 'GET'])
def svalidateLogin():
    if request.method == 'GET':
        return render_template('home.html')
    try:
        _username = request.form['t1']
        _password = request.form['t2']

       # con = mysql.connect()
        #cursor = con.cursor()
        cnx = mysql.connector.connect(user='root', password='Mehwash', host='127.0.0.1', database='finalyear')
        curs = cnx.cursor()
        curs.execute("select * from student where username=%s and rollno=%s",(_username,_password,))
        data = curs.fetchall()
        curs.close()
        cnx.close()
        if len(data) > 0:
            session['user_name']=_username
            session['user_pass'] = _password
            return render_template("studentprofile.html",name=session['user_name'], password =session['user_pass'])
        else:
            return render_template('error.html', error='Wrong Email address or Password.')
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('adminprofile.html')

    if request.method == 'POST':
            roll=request.form['roll']
            sem=request.form['sem']
            dept=request.form['dept']
            cc=request.form['cc']
            if roll and sem and dept and cc:
                cnx = mysql.connector.connect(user='root', password='Mehwash', host='127.0.0.1', database='finalyear')
                curs = cnx.cursor()
                at=0
                curs.execute("""Insert into taketest (rollno,semester,dept,course_code,attempt) values(%s,%s,%s,%s,%s)""",
                             (roll,sem,dept,cc,at))
                cnx.commit()
                flash("Inserted Successfully")
                return render_template("adminprofile.html")
            else:
                return json.dumps({'html': '<span>Enter the required fields</span>'})
            curs.close()
            cnx.close()



@app.route('/acceptrule', methods=['POST'])

def acceptrule():
    if request.method == 'GET':
        return render_template('studentprofile.html')

    if request.method == 'POST':
        z = request.form['paper_code']
        s = request.form['semester']
        session['paper_code']=z
        session['sem']=s
        cnx = mysql.connector.connect(user='root', password='Mehwash', host='127.0.0.1', database='finalyear')
        curs = cnx.cursor()
        curs.execute("select attempt from taketest where rollno=%s and semester=%s and course_code=%s",(session['user_pass'], s,z,))
        data = curs.fetchall()
        curs.close()
        cnx.close()
        #print(s);
        #print(data[0][0])
        if(data[0][0]==0):
            try:
                return render_template("rule.html")
            except mysql.connector.Error as err:
                print ("Query failed")
                print (err)
            '''filename=z+".txt"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filepath = os.path.join(os.path.abspath('./'), filepath)
            if(os.path.isfile(filepath)):
                with open(filepath,'r')as fr:
                    content= [line.split('?') for line in fr.readlines()]
                    #t=fr.read()
                    #content=t.split("?")
                return render_template("qpaper.html",content=content)

            else:
                return "Sorry,Paper not uploaded!"'''
        else:
            curs.close()
            cnx.close()
            return render_template("studentprofile.html", msg="Test Already Taken",
                                   name=session['user_name'], password =session['user_pass'])


@app.route('/taketest', methods=['GET', 'POST'])
def taketest():
    if request.method == 'GET':
        return render_template('qpaper.html')

    if request.method == 'POST':
        if(request.form.get("check1")):
            cnx = mysql.connector.connect(user='root', password='Mehwash', host='127.0.0.1', database='finalyear')
            curs = cnx.cursor()
            sql1 = "UPDATE taketest SET attempt=1 WHERE rollno=%s and semester=%s and course_code=%s"
            data = (session['user_pass'], session['sem'], session['paper_code'])
            curs.execute(sql1, data)
            cnx.commit()
            curs.close()
            cnx.close()
            filename = session['paper_code'] + ".txt"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filepath = os.path.join(os.path.abspath('./'), filepath)
            if (os.path.isfile(filepath)):
                with open(filepath, 'r')as fr:
                    content = [line.split('?') for line in fr.readlines()]
                    # t=fr.read()
                    # content=t.split("?")
                return render_template("qpaper.html", content=content)

            else:
                return "Sorry,Paper not uploaded!"
        else:
            return render_template("studentprofile.html",name=session['user_name'], password =session['user_pass'])

@app.route('/new', methods=['GET', 'POST'])

def new():
    if request.method == 'GET':
        return render_template('qpaper.html')

    if request.method == 'POST':

        #if request.form["action"]=="Save":
            x = request.form['textarea']
            # y=request.form['fsave']
            f1=session['user_pass']
            f1=f1.replace("/","_")
            print(f1)
            f2=session['paper_code']
            f=f1+"_"+f2+".txt"
            print(f)
            filepath = os.path.join(app.config['ANSWER_FOLDER'], f)
            filepath = os.path.join(os.path.abspath('./'), filepath)
            with open(filepath,'w')as wr:
                 wr.write(x)
            #func_cookies()

            return render_template('studentprofile.html',name=session['user_name'], password =session['user_pass'])
    #else:
         #return render_template("studentprofile.html")




@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return render_template('teacherprofile.html')

    if request.method == 'POST':
        # check if the post request has the file part
        sub=request.form["subject"]

        if 'file_to_upload' not in request.files:
            return 'No file part'
        file = request.files['file_to_upload']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            filepath= os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filepath = os.path.join(os.path.abspath('./'), filepath)
            #print ('filepath: ' + filepath)
            file.save(filepath)
            #this_file=self.request.params['file_to_upload'].filename
            #(this_file_name, this_file_extension) = os.path.splitext(filename)
            '''if this_file_extension=='.txt':
                with open(filename, encoding='utf8') as f:
                    return f.read()'''
            #if this_file_extension=='.docx':
               # my_text = docx2txt.process(file)
                #print(my_text)
               # temp=tokentry.process_content(filepath)
            #else:
            temp = tokentry.process_content(filepath,sub)
            return send_from_directory('./',temp)
        else:
            return "Not a Proper Extensions"


@app.route('/ssignup', methods=['POST'])
def ssignup():
    try:
        _fname = request.form['fname']
        _sname = request.form['sname']
        _name = _fname+" "+_sname
        _sb = request.form['subject']
        _yr = request.form['year']
        _roll = request.form['roll']
        _ins=request.form['instname']
        _ins=_ins.lower();
        _rollno = _sb+"/"+_yr+"/"+_roll
        _email= request.form['email']
        if _name and _roll and _sb and _yr and _email:
            if _ins == 'mckvie':
                cnx = mysql.connector.connect(user='root', password='Mehwash', host='127.0.0.1', database='finalyear')
                curs = cnx.cursor()
                curs.execute("""Insert into student (username,rollno,email) values(%s,%s,%s)""",(_name, _rollno, _email))
                cnx.commit()
                curs.close()
                cnx.close()
                return render_template("studentlogin.html")
            else:
                flash(" wrong field")
                return render_template("wrong.html")

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
        curs.close()
        cnx.close()
    except Exception as e:
        print(e)
        curs.close()
        cnx.close()
        return render_template('studentregister.html')


@app.route('/tsignup', methods=['POST'])
def tsignup():
    try:
        _fname = request.form['fname']
        _sname = request.form['sname']
        _name = _fname+" "+_sname
        _sb = request.form['subject']
        _yr = request.form['year']
        _roll = request.form['roll']
        _ins=request.form['instname']
        _ins=_ins.lower();
        _pswd=request.form['pswd']
        _cpswd=request.form['cpswd']

        #_rollno = _sb+"/"+_yr+"/"+_roll
        _email= request.form['email']
        if _name and _roll and _email:
            if _ins == 'mckvie':
                if _pswd==_cpswd:
                    cnx = mysql.connector.connect(user='root', password='Mehwash', host='127.0.0.1', database='finalyear')
                    curs = cnx.cursor()
                    curs.execute("""Insert into teacher (username,enroll_no,email,password,dept) values(%s,%s,%s,%s,%s)""",
                             (_name, _roll, _email,_pswd,_sb))
                cnx.commit()
                return render_template("teacherlogin.html")
            else:
                flash(" wrong field")
                return render_template("wrong.html")

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
        curs.close()
        cnx.close()
    except Exception as e:
        print(e)
        curs.close()
        cnx.close()
        return render_template('teacherregister.html')


@app.route('/forgetpswd')
def forgetpswd():
    return render_template("forgetpassword.html")



@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/fpwd',methods=['POST'])
def fpwd():
    _uname=request.form['uname']
    cat=request.form['cat']
    cnx = mysql.connector.connect(user='root', password='Mehwash', host='127.0.0.1', database='finalyear')
    curs = cnx.cursor()
    if(cat=='Student'):
        curs.execute("select rollno,email from student where username=%s",(_uname,))
        data=curs.fetchall()
    else:
        curs.execute("select password,email from teacher where username=%s", (_uname,))
        data = curs.fetchall()

    msg=str(data[0][0])
    recepient=data[0][1]
    msgpass="Hello!"+_uname+",Your Password is:"+msg
    msg = Message("Password Check", sender='onlinesystem2k17@gmail.com', recipients=[recepient])
    msg.body = msgpass
    mail.send(msg)
    return "Pls,Check your email!Sent"

    #print ("message="+msg+"receiver=")

@app.route('/sregister')
def sregister():
    return render_template("studentregister.html")

@app.route('/tregister')
def tregister():
    return render_template("teacherregister.html")


@app.route('/logout')
def logout():
    session.pop('tuser',None)
    session.pop('sem',None)
    session.pop('auser', None)
    session.pop('user_name', None)
    session.pop('user_pass', None)
    session.pop('paper_code',None)
    return render_template("home.html")


if __name__ == "__main__":
    app.run(port=8080, debug=True)