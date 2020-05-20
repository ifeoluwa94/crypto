from flask import Flask, Markup, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def line():

    coin1 = request.form.get("coin")

    import pgdb #  PostgreSQL database adapter for Python

    if coin1 in ('BTC','LTC','ETH','XRP'):
        event ='event'
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('eventlog',event,"'"+coin1+"'") 
        conn = pgdb.connect(host="34.105.201.48",database="crypto_db", user="postgres", password="12345")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()


    if coin1 == None or coin1=='Choose below':
        coin1 = 'BTC'
    
    conn = pgdb.connect(host="34.105.201.48",database="crypto_db", user="postgres", password="12345")  # create connection instance to postgre DB
    cursor = conn.cursor()
    q1= 'select currency_code, Date,price_close from (select currency_code,left(time_period_end,10) as Date,price_close from history where currency_code='+"'"+coin1+"'"+'order by currency_code asc, left(time_period_end,10)  desc limit 100) t order by currency_code asc, Date asc'
    q2 = 'select  left(time_period_end,7) as Year_, round(AVG(CAST (price_close AS decimal)),0) as AVRG  from history where currency_code='+"'"+coin1+"'"+' group by currency_code, left(time_period_end,7) order by Year_ asc'
    cursor.execute(q1)


    options = list()
    for row in cursor.fetchall():
        options.append(row)
    
    dates = list()
    price = list()
    currency = list()
    for a in range(len(options)):
        dates.append(options[a][1:2][0])
        price.append(options[a][2:3][0])
        currency.append(options[a][0:1][0])


    conn = pgdb.connect(host="34.105.201.48",database="crypto_db", user="postgres", password="12345")  # create connection instance to postgre DB
    cursor = conn.cursor()
    cursor.execute(q2)

    options2 = list()
    for row in cursor.fetchall():
        options2.append(row)

    dates2 = list()
    price2 = list()
    for a in range(len(options2)):
        dates2.append(str(options2[a][0:1][0]))
        price2.append(options2[a][1:2][0])
        

    labels = dates
    values = price

    labels2 =dates2
    values2 = price2


    line_labels=labels
    line_values=values

    line_labels2=labels2
    line_values2=values2

    if coin1 == 'BTC':
        maxi = 12000
        steps = 10
    elif coin1 == 'ETH':
        maxi = 300
        steps = 10
    elif coin1 == 'XRP':
        maxi = 5
        steps = 0.1
    else:
        maxi = 100
        steps = 10
    return render_template('index.html', title='Historical crypto currency chart', max=maxi, step=steps,labels=line_labels,labels2=line_labels2, values=line_values, values2= line_values2,lab = coin1+' closing price trend')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    #app.run(debug=True,host='0.0.0.0',port=8080)

#app.run("localhost", "9999", debug=True)