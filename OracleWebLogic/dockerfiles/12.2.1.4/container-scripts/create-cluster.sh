# Set environment.
. /u01/oracle/user_projects/domains/base_domain/bin/setDomainEnv.sh

# Create the cluster.
cd /u01/oracle/container-scripts/

java -Dweblogic.security.TrustKeyStore=DemoTrust -Dweblogic.secury.allowCryptoJDefaultJCEVerification=true weblogic.WLST create_cluster.py -p DockerCluster.properties
