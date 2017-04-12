rem 应用所在jboss
set jboss_home=D:\appserver\jboss-app-as-1.3
set java_home=C:\Java\jdk1.5.0_05
rem 应用名称
set ServiceName=appserver
rem jconsole端口
set JconsolePort=12345
set localip=172.17.4.197
rem 32位jdk最大设置1024M, 64位jdk无上限, 按应用服务器的内存情况合理分配, 但不要小于1024M
set JAVA_OPTS=-Xms1024M -Xmx1024M -XX:MaxNewSize=256m -XX:MaxPermSize=256m -Xss128K
rem 64位jdk请用JavaService64.exe
set JavaService=JavaService.exe
rem set JavaService=JavaService64.exe

rem 删除应用%ServiceName%
%JBOSS_HOME%\bin\%JavaService% -uninstall %ServiceName%

rem 安装应用%ServiceName%
%JBOSS_HOME%\bin\%JavaService% -install %ServiceName% %JAVA_HOME%\jre\bin\server\jvm.dll -Djava.class.path=%JBOSS_HOME%\bin\run.jar;%JAVA_HOME%\lib\tools.jar %JAVA_OPTS% -Dcom.sun.management.jmxremote.port=%JconsolePort% -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -Djboss.platform.mbeanserver -Djavax.management.builder.initial=org.jboss.system.server.jmx.MBeanServerBuilderImpl -Djava.util.logging.manager=org.jboss.logmanager.LogManager -Dorg.jboss.logging.Logger.pluginClass=org.jboss.logging.logmanager.LoggerPluginImpl  -Djava.rmi.server.hostname=%localip% -Dremoting.bind_by_host=false  -start org.jboss.Main -params -b 0.0.0.0 -C default -stop org.jboss.Main -method systemExit  -current "%JBOSS_HOME%\bin" -auto -overwrite