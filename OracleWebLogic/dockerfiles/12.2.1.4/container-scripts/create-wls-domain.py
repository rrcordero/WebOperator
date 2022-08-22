domain_name  = os.environ.get("DOMAIN_NAME", "base_domain")
admin_name  = os.environ.get("ADMIN_NAME", "AdminServer")
admin_listen_port   = int(os.environ.get("ADMIN_LISTEN_PORT", "7001"))
domain_path  = '/u01/oracle/user_projects/domains/%s' % domain_name
production_mode = os.environ.get("PRODUCTION_MODE", "prod")
administration_port_enabled = os.environ.get("ADMINISTRATION_PORT_ENABLED", "true")
administration_port = int(os.environ.get("ADMINISTRATION_PORT", "9002"))
cluster_name = 'DockerCluster'

print('domain_name                 : [%s]' % domain_name);
print('admin_listen_port           : [%s]' % admin_listen_port);
print('domain_path                 : [%s]' % domain_path);
print('production_mode             : [%s]' % production_mode);
print('admin name                  : [%s]' % admin_name);
print('administration_port_enabled : [%s]' % administration_port_enabled);
print('administration_port         : [%s]' % administration_port);


# Open default domain template
# ============================
readTemplate("/u01/oracle/wlserver/common/templates/wls/wls.jar")

set('Name', domain_name)
setOption('DomainName', domain_name)

# Set Administration Port 
# =======================
if administration_port_enabled != "false":
   set('AdministrationPort', administration_port)
   set('AdministrationPortEnabled', 'true')

# Disable Admin Console
# --------------------
# cmo.setConsoleEnabled(false)

# Configure the Administration Server and SSL port.
# =================================================
cd('/Servers/AdminServer')
set('Name', admin_name)
set('ListenAddress', '')
set('ListenPort', admin_listen_port)
if administration_port_enabled != "false":
   create('AdminServer','SSL')
   cd('SSL/AdminServer')
   set('Enabled', 'True')

# Define the user password for weblogic
# =====================================
cd(('/Security/%s/User/weblogic') % domain_name)
cmo.setName(username)
cmo.setPassword(password)

# Write the domain and close the domain template
# ==============================================
setOption('OverwriteDomain', 'true')
setOption('ServerStartMode',production_mode)

# Create Node Manager
# ===================
cd('/NMProperties')
set('ListenAddress','')
set('ListenPort',5556)
set('CrashRecoveryEnabled', 'true')
set('NativeVersionEnabled', 'true')
set('StartScriptEnabled', 'false')
set('SecureListener', 'false')
set('LogLevel', 'FINEST')

# Set the Node Manager user name and password 
# ===========================================
cd('/SecurityConfiguration/%s' % domain_name)
set('NodeManagerUsername', username)
set('NodeManagerPasswordEncrypted', password)


# Create a cluster
# ================
cd('/')
cl=create(cluster_name, 'Cluster')


# Write Domain
# ============
writeDomain(domain_path)
closeTemplate()

#################################################################################################
## DataSource Deploy
#################################################################################################


#domainname = os.environ.get('DOMAIN_NAME', 'base_domain')
#domainhome = os.environ.get('DOMAIN_HOME', '/u01/oracle/user_projects/domains/' + domainname)
#cluster_name = os.environ.get("CLUSTER_NAME", "DockerCluster")
#admin_name = os.environ.get("ADMIN_NAME", "AdminServer")

#print('Domain Home      : [%s]' % domainhome);
#print('Domain Name       : [%s]' % domainname);
#print('Admin Name       : [%s]' % admin_name);
#print('Cluster Name     : [%s]' % cluster_name);

#dsname=('DockerDS')
#dsjndiname=('jdbc/DockerDS')
#dsdbname=('default;create=true')
#dsdriver=('org.apache.derby.jdbc.ClientDataSource')
#dsurl=('jdbc:derby://localhost:1527/default;ServerName=localhost;databaseName=default;create=true')
#dsusername=('usuario')
#dspassword=('password')
#dstestquery=('SQL SELECT 1 FROM SYS.SYSTABLES')
#dsmaxcapacity=('1')

#nmConnect('weblogic', 'welcome1', 'localhost', '5556', 'base_domain', '/u01/oracle/user_projects/domains/base_domain', 'plain')
#readDomain(domainhome)

#create(dsname, 'JDBCSystemResource')
#cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
#cmo.setName(dsname)

#cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
#create('myJdbcDataSourceParams','JDBCDataSourceParams')
#cd('JDBCDataSourceParams/NO_NAME_0')
#set('JNDIName', java.lang.String(dsjndiname))
#set('GlobalTransactionsProtocol', java.lang.String('None'))

#cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
#create('myJdbcDriverParams','JDBCDriverParams')
#cd('JDBCDriverParams/NO_NAME_0')
#set('DriverName', dsdriver)
#set('URL', dsurl)
#set('PasswordEncrypted', dspassword)
#set('UseXADataSourceInterface', 'false')

#print 'create JDBCDriverParams Properties'
#create('myProperties','Properties')
#cd('Properties/NO_NAME_0')
#create('user','Property')
#cd('Property/user')
#set('Value', dsusername)

#cd('../../')
#create('databaseName','Property')
#cd('Property/databaseName')
#set('Value', dsdbname)

#print 'create JDBCConnectionPoolParams'
#cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
#create('myJdbcConnectionPoolParams','JDBCConnectionPoolParams')
#cd('JDBCConnectionPoolParams/NO_NAME_0')
#set('TestTableName','SQL SELECT 1 FROM DUAL')

#assign('JDBCSystemResource', dsname, 'Target', cluster_name)

#updateDomain()
#closeDomain()


#################################################################################################
## APP Deploy
#################################################################################################

domainhome = os.environ.get('DOMAIN_HOME', '/u01/oracle/user_projects/domains/base_domain')
admin_name = os.environ.get('ADMIN_NAME', 'AdminServer')
appname    = os.environ.get('APP_NAME', 'simple-app')
appfile    = os.environ.get('APP_FILE', 'simple-app.war')
appdir     = os.environ.get('APP_DIR', '/u01/oracle/container-scripts/despliegue/')
cluster_name = os.environ.get('CLUSTER_NAME', 'DockerCluster')

print('Domain Home      : [%s]' % domainhome);
print('Admin Name       : [%s]' % admin_name);
print('Cluster Name     : [%s]' % cluster_name);
print('Application Name : [%s]' % appname);
print('appfile          : [%s]' % appfile);
print('appdir           : [%s]' % appdir);

#nmConnect('weblogic', 'welcome1', 'localhost', '5556', 'base_domain', '/u01/oracle/user_projects/domains/base_domain', 'plain')
readDomain(domainhome)

cd('/')
app = create(appname, 'AppDeployment')
app.setSourcePath(appdir + '/' + appfile)
app.setStagingMode('nostage')

assign('AppDeployment', appname, 'Target', cluster_name)

updateDomain()
closeDomain()

# Exit WLST
# =========
exit()
