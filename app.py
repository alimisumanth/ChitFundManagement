from flask import Flask,render_template,request
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route("/add")
def add():
    return render_template("newmember.html")
@app.route("/payments")
def payments():
    return render_template("Payments.html")
@app.route("/GroupDetails",methods=["GET","POST"])
def GroupDetails():
  if request.method=='POST':
    groupDetails=request.form.get('groupDetails')

    query="SELECT * FROM "+str(groupDetails)
    with sqlite3.connect("chitdb.sqlite") as c:
        cur = c.cursor()
        cur.execute(query)
        r=cur.fetchall()
        if len(r)>0:
            memberlist=[]
            for i in r:
                memberlist.append([i[0],i[1],i[2],i[3],i[4],i[5]])
            c.commit()
            return render_template("Members.html",members=memberlist)
        else:
            return render_template('result.html', msgf='No Details found.')
@app.route("/MemberDetails",methods=['POST','GET'])
def memberdetails():
  try:
    if request.method=='POST':
        membername=request.form.get('member')
        with sqlite3.connect('chitdb.sqlite') as con:
            cur=con.cursor()
            con.row_factory=sqlite3.Row
            cur.execute("SELECT * FROM GROUP1 where name=? UNION SELECT * FROM GROUP2 WHERE name=?",(membername,membername))
            result=cur.fetchall()
            if len(result)>0:
                memdetails=[]
                for i in result:
                    memdetails.append([i[1],i[2],i[3],i[4],i[5],i[6]])
                return render_template("MemberToGroup.html",res=memdetails)
            else:
                return render_template('result.html', msgf='No Details found. Please verify the name')

  except:
      return render_template('result.html', msgf='No Details found. Please verify the name')


@app.route('/newmembe',methods=['POST','GET'])
def newmember():

    if request.method=='POST':

        try:
            name1=request.form.get('name')
            paidAmount=request.form.get('paidAmount')
            group=request.form.get('Group')
            BalanceAmount=20000-int(paidAmount)
            sqlquery='INSERT INTO '+group+"(name,PaidAmount,RemainingMonths,BalanceAmount,groups)"+" VALUES("+'"'+str(name1)+'",'+str(paidAmount)+","+"19"+","+str(BalanceAmount)+",'"+str(group)+"')"
            with sqlite3.connect("chitdb.sqlite") as c:
                cur=c.cursor()
                cur.execute(sqlquery)
                c.commit()
                msgs = "New member added sucessfully"
                return render_template("result.html", msgs=msgs)
        except:
            msgf = "Failed to add new member"
            return render_template("result.html",msgf=msgf)

@app.route('/paymentdetails',methods=['POST','GET'])
def paymentdetails():
    if request.method=="POST":
        name1 = request.form.get('name')
        paidAmount = request.form.get('paidAmount')
        group = request.form.get('Group')
        sqlquery1 = "SELECT RemainingMonths,PaidAmount,BalanceAmount FROM " + group + ' where name="' + name1 + '"'
        with sqlite3.connect("chitdb.sqlite") as c:
            cur = c.cursor()
            cur.execute(sqlquery1)
            res=cur.fetchone()
            if res!=None :
                sqlquery4 = 'UPDATE ' + group + " SET RemainingMonths=" +str(res[0]-1) +",PaidAmount=" +str(res[1]+int(paidAmount)) + ",BalanceAmount=" + str((20000-int(paidAmount)+int(res[2]))) + ' where name="' + name1 + '"'
                print(sqlquery4)
                cur.execute(sqlquery4)
                message="Records Updated Sucessfully"
                c.commit()
                return render_template("result.html",msgs=message)
            else:
                return render_template("result.html",msgf="Failed to update the records. Please verify name and group")




if __name__ == '__main__':
    app.debug=True
    app.run()
