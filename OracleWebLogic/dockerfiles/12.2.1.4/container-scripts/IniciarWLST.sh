#Metodo de conexion contra WLST

# Set environment.
. /u01/oracle/user_projects/domains/base_domain/bin/setDomainEnv.sh

java -Dweblogic.security.TrustKeyStore=DemoTrust -Dweblogic.secury.allowCryptoJDefaultJCEVerification=true weblogic.WLST

connect("weblogic","welcome1","t3s://localhost:9002")


