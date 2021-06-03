from flask import *  
import io
import urllib.request
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as canv
from matplotlib.figure import Figure
import base64

app = Flask(__name__)  

@app.route('/', methods=['GET'])
def plot():
    #connect to the osa and download trace data
    trace_url="http://flaskosa.herokuapp.com/cmd/TRACE"
    req=urllib.request.urlopen(trace_url)
    raw_data = req.read()
    #reattempt to get trace data if random string is returned
    while "instrument_model" not in str(raw_data): 
        req=urllib.request.urlopen("trace_url")
        raw_data = req.read()

    #extract information from json
    data=json.loads(raw_data)
    x=data["xdata"]
    x_label = data["xlabel"]+" (" + data["xunits"]+")"
    y=data["ydata"]
    y_label = data["ylabel"]+" (" + data["yunits"]+")"
    date = data["timestamp"].split(".")
    time=date[2].split()
    title="OSA Measurement at 20%s-%s-%sT%s (UTC)" %(date[0],date[1],time[0],time[1])

    #create figure using matplotlib
    img=io.BytesIO()
    fig=Figure()
    axis = fig.add_subplot(1,1,1)
    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.plot(x,y)
    canv(fig).print_png(img)

    #save and display the image in html page
    img_64_string = "data:image/png;base64,"
    img_64_string += base64.b64encode(img.getvalue()).decode('utf8')
    return render_template("plot.html", image=img_64_string)


if __name__ == '__main__':  
   app.run(debug = True)  
