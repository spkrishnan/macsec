import yaml
import sys
import random
import datetime
import logging
import time
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.op.lldp import *
from jnpr.junos.op.phyport import *
from jinja2 import Template
from logging import *
from junver import *

# Open the macsec_data.yml file and the template file
with open('macsec_data.yml') as fh:
	data = yaml.load(fh.read())

with open('macsec_template.j2') as t_fh:
	t_format = t_fh.read()


lgr = logging.getLogger('macsec')
lgr.setLevel(logging.INFO)

# Create a log handler
fh = logging.FileHandler('macsec.log')
fh.setLevel(logging.INFO)

frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)
lgr.addHandler(fh)

# Generate the keys necessary for MACsec configuration
CKN = '{0:04}'.format(random.randint(1, 10000))
CAK = '{0:020}'.format(random.randint(10000000, 400000000000))

# Create two containers for the two nodes. These containers will hold the values that will be fed into the template
DATA_NODE1 = {}
DATA_NODE2 = {}

# Assign Values to the variables required for the template
DATA_NODE1['CA_NAME'] = data['N1_CA_NAME']
DATA_NODE1['INTERFACE_NAME'] = data['N1_INT']

DATA_NODE2['CA_NAME'] = data['N2_CA_NAME']
DATA_NODE2['INTERFACE_NAME'] = data['N2_INT']

DATA_NODE1['CKN'] = str(CKN)
DATA_NODE1['CAK'] = str(CAK)

DATA_NODE2['CKN'] = str(CKN)
DATA_NODE2['CAK'] = str(CAK)

# Load the template into a variable called template
template = Template(t_format)

# Log the configuration that will be pushed to the nodes. The log messages are written to the log file opened earlier
lgr.info('Node1 macsec')
lgr.info(template.render(DATA_NODE1))

lgr.info('\nNode2 macsec')
lgr.info(template.render(DATA_NODE2))

# Provide information required to connect to the device
N1 = Device(host=data['N1_IP'],user=data['N1_USER'],password=data['N1_PASS'])
N2 = Device(host=data['N2_IP'],user=data['N2_USER'],password=data['N2_PASS'])


# Open connection to Node1
N1.open()

# Open connection to Node2
N2.open()

###############################################################
# This section checks if the nodes have Controlled version of
# software installed. If not, the script exits
###############################################################
CHECKVER_N1 = JunVerTable(N1).get()
CHECKVER_N2 = JunVerTable(N2).get()

# Check if N1 has MACsec image
if 'jcrypto-ex' not in CHECKVER_N1:
 print ("\n\n**************************************************")
 print (data['N1_IP'] + " does not have MACsec software")
 print "Exiting Script"
 print "MACsec configuration aborted"
 print "**************************************************\n"
 lgr.info(data['N1_IP'] + " does not have MACsec software")
 lgr.info('Aborting MACsec Configuration')
 N1.close()
 N2.close()
 sys.exit()

# Check if N2 has MACsec image
if 'jcrypto-ex' not in CHECKVER_N2:
 print ("\n\n**************************************************")
 print (data['N2_IP'] + " does not have MACsec software")
 print "Exiting Script"
 print "MACsec configuration aborted"
 print "**************************************************\n"
 lgr.info(data['N1_IP'] + " does not have MACsec software")
 lgr.info('Aborting MACsec Configuration')
 N1.close()
 N2.close()
 sys.exit()

###############################################################



# *** Configure Node1 ***
print "Configuring Node1"
N1_CONF = Config(N1)
N1_CONF.load(template.render(DATA_NODE1), format='set')
N1_CONF.commit()

# *** Configure Node2 ***
print "Configuring Node2"
N2_CONF = Config(N2)
N2_CONF.load(template.render(DATA_NODE2), format='set')
N2_CONF.commit()


print "MACsec configuration completed"
 
# Close connections to Node1 and Node2
N1.close()
N2.close()
