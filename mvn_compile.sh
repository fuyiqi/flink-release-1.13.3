mvn clean install -T 2C -Dfast -Dmaven.compile.fork=true -DskipTests -Dscala-2.11 -Drat.skip=true -Dmaven.javadoc.skip=true -Dcheckstyle.skip=true -Dskip.npm
# mvn dependency:get -DremoteRepositories=http://repo1.maven.org/maven2/ -DgroupId=org.apache.maven.plugins -DartifactId=maven-gpg-plugin -Dversion=1.4
