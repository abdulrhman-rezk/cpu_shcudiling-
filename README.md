# smart cpu scheduler

a small app that simulate cpu scheduling .. but the quantum is not fixed
a machine learning model read every process and decide if it cpu bound or io bound
io bound processes get a big quantum .. cpu bound get a small one
then it compare the result with the normal round robin (fixed quantum) and show charts

i made it while learning machine learning basics (scikit-learn) .. nothing fancy

## the idea in one line
io bound processes suffer with the normal round robin .. big quantum let them finish fast and the waiting time go down

## how to run
first train the model
```
cd model_training
python data_gen.py
python train.py
```

then run the app
```
cd ../smart_scheduler
python main.py
```

you need the packages first
```
pip install -r requirements.txt
```

## the files
- model_training/data_gen.py -> generate fake processes data (10000 rows)
- model_training/train.py -> train the model and save it
- smart_scheduler/processes.py -> Process class + generate random processes
- smart_scheduler/scheduler.py -> the model prediction + round robin simulation
- smart_scheduler/main.py -> the cli app (heart of the project)

## how it look
```
what the model decided
----------------------------------------------------------------------
PID     Burst   IO      Memory  Type            Quantum
----------------------------------------------------------------------
P1      12ms    15      512MB   io bound        20ms
P2      120ms   2       256MB   cpu bound       5ms
----------------------------------------------------------------------
scheduling comparison
----------------------------------------------------------------------
PID     Burst   std RR WT       AI RR WT        saved
----------------------------------------------------------------------
P1      12ms    398ms           20ms            378ms
```

thats it
