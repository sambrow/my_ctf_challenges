FROM maven:3.8-jdk-8 as build
COPY challengeApp /challengeApp
RUN mvn -f /challengeApp/pom.xml clean install

FROM tomcat:9.0
COPY --from=build /challengeApp/target/ChallengeApp-1.war /usr/local/tomcat/webapps/ROOT.war
RUN sed -i 's/port="8080"/port="80"/' ${CATALINA_HOME}/conf/server.xml
ENV FLAG=wsc{j4v4_ch4ls_4r3_r4r3_513156}
EXPOSE 80
