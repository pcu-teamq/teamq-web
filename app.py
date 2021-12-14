from flask import Flask, render_template, session, url_for, request, redirect
import pymysql
import pandas as pd

app = Flask(__name__)
app.secret_key = 'sample_secret'

def connectsql():
    conn = pymysql.connect(host='localhost', user = 'root', passwd = '', db = 'arduino', charset='utf8')
    return conn

@app.route('/')
# 세션유지를 통한 로그인 유무 확인
def index():
    if 'username' in session:
        username = session['username']

        return render_template('post.html', logininfo = username)
    else:
        username = None
        return render_template('login.html', logininfo = username )

@app.route('/post')
# board테이블의 게시판 제목리스트 역순으로 출력
def post():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query1 = "SELECT tag, NAME, LOG, TIME, ID FROM board ORDER BY tag DESC" # ORDER BY 컬럼명 DESC : 역순출력, ASC : 순차출력
    cursor.execute(query1)
    post_list = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('post.html', postlist = post_list, logininfo=username)
    
@app.route('/logout')
# username 세션 해제
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
# GET -> 로그인 페이지 연결
# POST -> 로그인 시 form에 입력된 id, pw를 table에 저장된 id, pw에 비교후 일치하면 로그인, id,pw 세션유지
def login():
    if request.method == 'POST':
        userid = request.form['id']
        userpw = request.form['pw']

        logininfo = request.form['id']
        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT * FROM tbl_user WHERE user_name = %s AND user_passwd = %s"
        value = (userid, userpw)
        cursor.execute(query, value)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        for row in data:
            data = row[0]
        
        if data:
            session['username'] = request.form['id']
            session['password'] = request.form['pw']
            return render_template('post.html', logininfo = logininfo)
        else:
            return render_template('loginError.html')
    else:
        return render_template ('login.html')    

@app.route('/regist', methods=['GET', 'POST'])
# GET -> 회원가입 페이지 연결
# 회원가입 버튼 클릭 시, 입력된 id가 tbl_user의 컬럼에 있을 시 에러팝업, 없을 시 회원가입 성공
def regist():
    if request.method == 'POST':
        userid = request.form['id']
        userpw = request.form['pw']

        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT * FROM tbl_user WHERE user_name = %s"
        value = userid
        cursor.execute(query, value)
        data = (cursor.fetchall())
        #import pdb; pdb.set_trace()
        if data:
            conn.rollback() # 이건 안 써도 될 듯
            return render_template('registError.html') 
        else:
            query = "INSERT INTO tbl_user (user_name, user_passwd) values (%s, %s)"
            value = (userid, userpw)
            cursor.execute(query, value)
            data = cursor.fetchall()
            conn.commit()
            return render_template('registSuccess.html')
        cursor.close()
        conn.close()
    else:
        return render_template('regist.html')           

if __name__ == '__main__':
    app.run(debug=True)
