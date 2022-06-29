from flask import Flask, request, send_from_directory, render_template, jsonify, make_response, send_from_directory, current_app
from flask_apscheduler import APScheduler



# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

# create app
app = Flask('Joe2Go', static_url_path='/static')

app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()



@scheduler.task('interval', id='do_job_1', seconds=86400, misfire_grace_time=900)
def job1():
  f = open('orders.txt', 'w')
  f.write("")
  print("orders cleared")




@app.route('/compile', methods=['GET'])
def compileOrder():
  f = open('orders.txt', 'r')
  Lines = f.readlines()
  count = 1
  order = ""
  length = len(Lines)
  
  # Strips the newline character
  for line in Lines:
    if count != length:
      count += 1
      a = ("{}".format(line.strip()))
      order = order+a+", "
    else: 
      count += 1
      a = ("{}".format(line.strip()))
      order = order+a

  
  order = order[:-1]  
  print(order)
  
  return render_template('compiled.html', order=order)

  
@app.route('/', methods=['GET', 'POST'])
def registerOrder():
  if request.method == 'POST':
      order = request.form.get('order')
      print(order)

      f = open('orders.txt', 'a')
      write = order+"\n"
      f.write(write)
      f.close()


    
  return '''
  <html>
  <head>
  <title>Joe2Go Order</title>
  <link rel="shortcut icon" href="/static/favicon.ico">

  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <link rel="manifest" href="/static/manifest.json" crossorigin="use-credentials">
  
  </head>
  
  <body>
  <div style="height: 30%;"></div>
  <div class="w3-container w3-mobile" style="width: 100%;">
   <h2 style="font-size: 70px; text-align: center;">Type your order here: </h2>
  <div style="width: 100%;" class="w3-display-container">
  
  <form method="POST">
  <h2 style="font-size: 50px; text-align: center;">Type your order here: <input w3-hide class="w3-input w3-mobile w3-display-middle" style="width: 80%;" type="text" name="order"></h2></div>
  <br><br><br>
       <input type="submit" value="Submit" class=" 
w3-display-middle w3-mobile w3-button w3-white w3-border w3-border-red w3-round-large w3-center" style="font-size: 40px; width: 50%; height: 10%; text-align: center; float: center;">
   </form>
  </div>


  
  <script>
  if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('./serviceWorker.js')
    .then(function(registration) {
      // Registration was successful
      console.log('ServiceWorker registration successful with scope: ', registration.scope);
      console.log(registration.scope)
      console.log(registration.scope)
  
    }).catch(function(err) {
      // registration failed :(
      console.log('ServiceWorker registration failed: ', err);
    });
  }
  </script>
  <div class="w3-container" style="font-size: 40px; text-align: center; width: 100%; height: 20%; padding-top: 40%;">
  <a href="/compile">Compile the order here</a>
  </div>

  </body>
  </html>'''




@app.route('/serviceWorker.js', methods=['GET'])
def sw():
    return app.send_static_file('serviceWorker.js')
  
app.run(host='0.0.0.0', port=8080)
