echo "Ejecutando BUILD java"

cd OracleJava/java-8/
sudo ./build.sh

echo "Ejecutando BUILD Weblogic 12c"

cd ../../OracleWebLogic/dockerfiles/
sudo ./buildDockerImage.sh -v 12.2.1.4 -d -c

echo "Iniciando Imagen Oracle Server"
sudo docker container run -d -p 7001:7001 -p 9002:9002 -it --name nodoWeblogic -v /u01/oracle/user_projects/domains/base_domain:/u01/oracle/properties "oracle/weblogic:12.2.1.4-developer"
