#!/bin/bash


########### SIGTERM handler ############
function _term() {
   echo "Stopping container."
   echo "SIGTERM received, shutting down the server!"
   ${DOMAIN_HOME}/bin/stopWebLogic.sh
}

########### SIGKILL handler ############
function _kill() {
   echo "SIGKILL received, shutting down the server!"
   kill -9 $childPID
}

# Set SIGTERM handler
trap _term SIGTERM

# Set SIGKILL handler
trap _kill SIGKILL

#Define DOMAIN_HOME
export DOMAIN_HOME=/u01/oracle/user_projects/domains/$DOMAIN_NAME
echo "Domain Home is: " $DOMAIN_HOME

ADD_DOMAIN=1
if [ ! -f ${DOMAIN_HOME}/servers/AdminServer/logs/AdminServer.log ]; then
    ADD_DOMAIN=0
fi

mkdir -p $ORACLE_HOME/properties
# Create Domain only if 1st execution
if [ $ADD_DOMAIN -eq 0 ]; then
   PROPERTIES_FILE=/u01/oracle/properties/domain.properties
   if [ ! -e "$PROPERTIES_FILE" ]; then
      echo "A properties file with the username and password needs to be supplied."
      exit
   fi

   # Get Username
   USER=`awk '{print $1}' $PROPERTIES_FILE | grep username | cut -d "=" -f2`
   if [ -z "$USER" ]; then
      echo "The domain username is blank.  The Admin username must be set in the properties file."
      exit
   fi
   # Get Password
   PASS=`awk '{print $1}' $PROPERTIES_FILE | grep password | cut -d "=" -f2`
   if [ -z "$PASS" ]; then
      echo "The domain password is blank.  The Admin password must be set in the properties file."
      exit
   fi

   # Create an empty domain
   wlst.sh -skipWLSModuleScanning -loadProperties $PROPERTIES_FILE  /u01/oracle/container-scripts/create-wls-domain.py

   mkdir -p  ${DOMAIN_HOME}/servers/AdminServer/security/
   chmod -R g+w  ${DOMAIN_HOME}
   echo "username=${USER}" >> $DOMAIN_HOME/servers/AdminServer/security/boot.properties
   echo "password=${PASS}" >> $DOMAIN_HOME/servers/AdminServer/security/boot.properties
   ${DOMAIN_HOME}/bin/setDomainEnv.sh
fi

# Start NodeManager
cd /u01/oracle/user_projects/domains/base_domain/bin
nohup ./startNodeManager.sh > nodemanager.log &

# Start Admin Server and tail the logs
nohup ${DOMAIN_HOME}/startWebLogic.sh &

sleep 60
. ${DOMAIN_HOME}/bin/setDomainEnv.sh
cd /u01/oracle/container-scripts

java -Dweblogic.security.TrustKeyStore=DemoTrust -Dweblogic.secury.allowCryptoJDefaultJCEVerification=true weblogic.WLST createWeblogicMachine.py

java -Dweblogic.security.TrustKeyStore=DemoTrust -Dweblogic.secury.allowCryptoJDefaultJCEVerification=true weblogic.WLST createMultipleDataSource.py

java -Dweblogic.security.TrustKeyStore=DemoTrust -Dweblogic.secury.allowCryptoJDefaultJCEVerification=true weblogic.WLST create_managed_server.py -p DockerDomain-ms1.properties

java -Dweblogic.security.TrustKeyStore=DemoTrust -Dweblogic.secury.allowCryptoJDefaultJCEVerification=true weblogic.WLST create_managed_server.py -p DockerDomain-ms2.properties


childPID=$!
wait $childPID


