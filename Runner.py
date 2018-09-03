import json
from datetime import datetime
from engine import Engine

# read raw_data.json
file_object = open('raw_data.json', 'r')
file_content = file_object.readline()
signal_list = json.loads(file_content)
# initialize Engine with rule file name
engine = Engine("rules.txt")
print "Rules object : " + str(engine.rules)
# pass each signal to Engine
start = datetime.now()
for signal in signal_list:
    # print signal
    engine.check_rule_for_signal(signal)
end = datetime.now()
print end-start
