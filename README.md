# Emoji Predictor

## Format of provided CSV/text file

The CSV/text file is formatted as (class, data)

### class
0:  Happy face
1:  Heart emoji

### data
comma separated states of the pixels.
Each pixel is 1 if selected and 0 if not.

data comprises of 1600 such pixels (40x40 board). 

### Example row
```
1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,1,0,1,0,1 ...

1 + 1600 values
1 for class (value 1)
1600 for data points (values 2-1601, inclusive)
```

## How to run

NOTE: A MySQL server is needed to run the scripts. Hence, for now, the best way to run tasks on the data is to use the provided CSV/text file (data.csv or data.txt).

If you have a MySQL setup and have access to our database, you can run the project scripts by following these steps:

1. Clone the repo on your local system.
```
git clone https://github.com/rohan-kadkol/Emoji-Predictor.git
```
2. Go to the terminal and cd into the project directory
```
cd Emoji-Predictor
```
3. Create a Python virtual environment
```
python -m venv env
or
python3 -m venv env
```

4. Enter into your virtual environment
```
source env/bin/activate (Linux/Mac)
env/Scripts/activate.bat (Windows)
```

4. Install the project dependencies
```
pip install -r requirements.txt
or 
pip3 install -r requirements.txt
or
pip install requirements.txt -r
or
pip3 install requirements.txt -r
```

5. Run the scripts
```
python script_xyz.py
```