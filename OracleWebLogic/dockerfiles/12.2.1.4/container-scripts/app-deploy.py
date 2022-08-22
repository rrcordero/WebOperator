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

exit()
