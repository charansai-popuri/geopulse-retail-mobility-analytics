# Spark and Sedona Setup (Windows)

## Versions that work together
| Tool | Version |
|---|---|
| Java | Temurin 17.0.21 |
| Python | 3.14.2 |
| PySpark | 4.1.4 |
| Apache Sedona | 1.9.1 (jar: sedona-spark-shaded-4.1_2.13) |
| pandas | 2.3.3 |

## Steps
1. Install Java 17, then check `java -version`.
2. Create the environment: `python -m venv .venv`, then activate it.
3. Install the packages: `pip install -r requirements.txt`
   (the PySpark download is about 455 MB; use `--retries 10 --timeout 120` on a slow connection).
4. Windows only: loading the Sedona jar through `spark.jars.packages` failed with
   "HADOOP_HOME and hadoop.home.dir are unset" because Hadoop needs winutils.exe on Windows.
   Fix: copy the downloaded jar into PySpark's own jars folder:
   `.venv\Lib\site-packages\pyspark\jars\`
   (the jar is in `%USERPROFILE%\.ivy2.5.2\jars` after one failed run).
5. Test: `python spatial\hello_sedona.py`

## Expected test output
```
+-----------------------+
|store_a                |
+-----------------------+
|POINT (77.5946 12.9716)|
+-----------------------+
```
Warnings about winutils, the native Hadoop library, Geotools and replaced functions are harmless here.