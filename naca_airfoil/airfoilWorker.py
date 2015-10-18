from celery import Celery
from dolfin_convert import gmsh2xml

app = Celery('airfolWorker',backend='amqp',broke='amqp://')

@app.task
runAirfoil(meshPath)

