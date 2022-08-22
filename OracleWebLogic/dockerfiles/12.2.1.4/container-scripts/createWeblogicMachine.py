connect('weblogic','welcome1', 't3s://localhost:9002')
 
edit()
startEdit()
 
# DockerMachine = the new WebLogic Machine
cmo.createUnixMachine('DockerMachine')
 
cd('/Machines/DockerMachine/NodeManager/DockerMachine')
cmo.setListenAddress('localhost')
cmo.setNMType('plain')
 
 
activate()
 
# This is the end of the script
