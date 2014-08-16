MACSEC SCRIPT OVERVIEW
======================

This script is used to automate MACsec configuration between two devices.

"macsec_script.py" is the main python script.

"macsec_data.yml" file is the input file. Network Admin trying to configure MACsec would edit this file and provide the following information:
- Connectivity Association Name
- IP address of the two nodes
- Interface names on the two nodes

"macsec_template.j2" is the Jinja template file

The py script checks the software version of the devices to make sure they are macsec capable and pushes down the config to the nodes and commits the nodes. 

I am working on updating the script to include MACsec verification after the MACsec configuration is installed. I will update the script after I test this. 

Please let me know if you have any suggestions to make the script better.

HOW TO USE THE SCRIPT:
=====================
STEP1: Ensure that you have the JUNOS EZ environment setup. This post provides good information for setting this up. 
http://lamejournal.com/2013/12/02/installing-junos-ez-library-easy-sdn-part-1/

STEP2: Copy the following files "macsec_data.yml", "macsec_script.py", "macsec_template.j2", "junver.py", "junver.yml" to a single directory

STEP3: Edit "macsec_data.yml" file and provide the necessary information

STEP4: Run the python script "python macsec_script.py"
