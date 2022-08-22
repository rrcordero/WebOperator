##############################################################################################################################
## Filestore and JMS
##############################################################################################################################

import os

# Deployment Information
domainname = os.environ.get('DOMAIN_NAME', 'base_domain')
admin_name = os.environ.get('ADMIN_NAME', 'AdminServer')
cluster_name = os.environ.get("CLUSTER_NAME", "DockerCluster")
domainhome = os.environ.get('DOMAIN_HOME', '/u01/oracle/user_projects/domains/' + domainname)

print('admin_name  : [%s]' % admin_name);

# Read Domain in Offline Mode
# ===========================
readDomain(domainhome)


#Create a Persistent Store
#================================================
cd('/')
myfilestore=create('DockerFileStore', 'FileStore')

cd('/FileStores/DockerFileStore')
myfilestore.setDirectory('/u01/oracle/user_projects/domains/base_domain/FileStore')

cd('/')
assign('FileStore', 'DockerFileStore', 'Target', cluster_name)


# Create a JMS Server
# ===================
cd('/')
jmsserver=create('DockerJMSServer', 'JMSServer')
print('Create JMSServer : [%s]' % 'DockerJMSServer')

cd('/JMSServers/DockerJMSServer')
set('PersistentStore', 'DockerFileStore')
print('FileStore_name     : [%s]' % getMBean('/FileStores/DockerFileStore'))

cd('/')
assign('JMSServer', 'DockerJMSServer', 'Target', admin_name)

# Create a JMS System resource
# ============================
cd('/')
create('DockerJMSSystemResource', 'JMSSystemResource')
cd('JMSSystemResource/DockerJMSSystemResource/JmsResource/NO_NAME_0')

# Create a JMS Queue and its subdeployment
# ========================================
myq = create('DockerQueue','Queue')
myq.setJNDIName('jms/DockerQueue')
myq.setSubDeploymentName('DockerQueueSubDeployment')

cd('/JMSSystemResource/DockerJMSSystemResource')
create('DockerQueueSubDeployment', 'SubDeployment')

# Target resources to the servers
# ===============================
cd('/')
assign('JMSSystemResource.SubDeployment', 'DockerJMSSystemResource.DockerQueueSubDeployment', 'Target', 'DockerJMSServer')

# Update Domain, Close It, Exit
# ==========================
updateDomain()
closeDomain()