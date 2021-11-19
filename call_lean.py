import os
import datetime
import time
import numpy as np
from pathlib import Path
from shutil import copyfile , rmtree

def call_lean( project_name, objective_value, **kwargs ):
	
	time.sleep( np.random.randint(0,4) )
	ts = '%s' % datetime.datetime.now()
	ts = ts.replace(".","").replace(" ","").replace("-","").replace(":","")
		
	log_path = project_name+"/backtests/"+ts+"/"
	try:
		
		Path(log_path).mkdir(parents=True, exist_ok=True)
		Path(log_path+"__pycache__").mkdir(parents=True, exist_ok=True)
		
		copyfile( "./{0}/main.py".format(project_name), log_path+"main.py" )
		#copyfile( "./{0}/__pycache__/main.cpython-36.pyc".format(project_name), log_path+"__pycache__/main.cpython-36.pyc" )
		
		create_json_for_optimization(log_path, **kwargs)

		command = "lean backtest  {0} --detach --output {1}  ".format(
			log_path, 
			log_path + ts
			)

		os.system( command )
		counter = -1
		while True:
			counter += 1
			time.sleep(4)
			if os.path.exists( log_path + ts+"/log.txt" ):
				time.sleep(6)
				break
			if counter >3:
				break

		res = read_log( log_path+ ts )
		time.sleep(2)
		os.system("rm -rf {0}".format(log_path))

		if objective_value in res.keys():
			return res[objective_value]
		else: 
			return 1e-10

	except Exception as e:
		os.system("rm -rf {0}".format(log_path))
		return 1e-20

def create_json_for_optimization( path , **kwargs):

	f = open( path + "config.json","w" )
	params = '"parameters": {'
	for key, value in kwargs.items():
		params += '\n\t\t\"{0}\": \"{1}\",'.format( key, value )
	params = params[:-1] + "\n}"

	tmp = "algorithm-language\": \"Python\",\n\t{0},\n\t\"description\": \"\",\n\t\"local-id\": 468148409".format(params)
	f.write(  "{\n\t\"" + tmp+ "\n}" )
	f.flush()
	f.close()


def read_log( path ):
	f = open(path+"/log.txt")
	data = f.read().split("STATISTICS:: ")
	res = {}
	for d in data:
		if "TRACE" not in d and "DEBUG" not in d and "LOG" not in d:
			try:
				val = d.replace("%","").replace("$","").strip().lower().split()
				res.update({"_".join(val[:-1]):float(val[-1])})
			except Exception as e:
				val = None
	f.close()
	
	return res