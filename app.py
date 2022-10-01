from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
cors = CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# No cacheing at all for API endpoints.
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

# Create the receiver API POST endpoint:
@app.route("/receiver", methods=["POST"])
def postME():
    data = request.get_json()
    num = processJson(data,[(0,1),(2,2)])
    return str(num)


@app.route('/')
def index():
    return render_template('index.html')

tower_op_radius = 5
opt = 10

def integrate(function, data):
    sum = 0
    for i in range(0, len(data)):
            sum += function(data[i])
    return sum

def processJson(data, posList):
    sigma = {}
    tStrength = {}
    towerLoc = {} 
    listOfPoints = []

    for i,pair in enumerate(posList):
        towerLoc[i] = pair
        listOfPoints.append(pair)

    towersInRange={}
    servicedPairs={}
    for i in range(0,len(data)):
        for j in range(0,len(data)):
            for k in range(0,len(posList)):
                if(math.dist((i,j),towerLoc[k])):
                    if((i,j) not in towersInRange):
                        towersInRange[(i,j)] = []
                    towersInRange[(i,j)].append(k)
                    if(k not in servicedPairs):
                        servicedPairs[k] = []
                    servicedPairs[k].append((i,j))
    # {0: [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], 
    # 1: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]}
    #0
    #foo = lambda x, y, key: data[x][y]/(math.dist(towerLoc[key],(x,y)))
    
    for key in servicedPairs:
        sigma[key] = integrate(lambda pt: data[pt[0]][pt[1]] / (math.dist(towerLoc[key],pt) if (math.dist(towerLoc[key],pt) != 0) else 0.001),servicedPairs[key])
    
    for key in sigma:
        tStrength[key] = math.exp(-(sigma[key]) - opt)

    def measureEffect(point):
        sum = 0
        for tid in towersInRange[point]:
            sum += tStrength[tid] / math.dist(towerLoc[tid], point)
        return sum

    metric = integrate(lambda point: data[point[0]][point[1]] * measureEffect(point), listOfPoints)

    return metric

    



