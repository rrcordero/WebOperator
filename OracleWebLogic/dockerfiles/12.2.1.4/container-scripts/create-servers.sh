# Set environment

. /u01/oracle/user_projects/domains/base_domain/bin/setDomainEnv.sh

# Create the managed servers.
cd /u01/oracle/container-scripts/

java -Dweblogic.security.TrustKeyStore=DemoTrust -Dweblogic.secury.allowCryptoJDefaultJCEVerification=true weblogic.WLST create_managed_server.py -p DockerDomain-ms1.properties

java -Dweblogic.security.TrustKeyStore=DemoTrust -Dweblogic.secury.allowCryptoJDefaultJCEVerification=true weblogic.WLST create_managed_server.py -p DockerDomain-ms2.properties
