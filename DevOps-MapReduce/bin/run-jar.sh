spark-submit  \
--class JarEnterPoint \
--deploy-mode client \
--conf "spark.executor.memoryOverhead=10g" \
--conf "spark.driver.extraJavaOptions=-Dlog4jspark.root.logger=ERROR,console" \
--jars /path/to/jar/on/cluster/spark.jar \
/path/to/execute/program.jar \
$1
