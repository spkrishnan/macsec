macsec
======

This script is used to automate MACsec configuration between two devices.

"macsec_script.py" is the main python script.

"macsec_data.yml" file is the input file. Network Admin trying to configure MACsec would edit this file and provide the following information:
- Connectivity Association Name
- IP address of the two nodes
- Interface names on the two nodes

"macsec_template.j2" is the Jinja template file

The py script checks the software version of the devices to make sure they are macsec capable and pushes down the config to the nodes and commits the nodes. 

I am working on updating the script to include MACsec verification after the MACsec configuration is installed. I will update the script after I test this. 
