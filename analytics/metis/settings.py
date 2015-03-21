DEBUG = False

# Port to listen for request on.
PORT = 8151

# All enabled executors.
EXECUTORS = [
  'metis.core.execute.python.PythonExecutor',
  # 'metis.core.execute.spark.SparkExecutor',
]

# The default executor to use, if none is specified in the request.
DEFAULT_EXECUTOR = 'metis.core.execute.python.PythonExecutor'

# A list of the data sources available to query
DATA_SOURCES = {
  'kronos': {  # A meaningful name... can be anything
    'type': 'metis.core.query.kronos.source.KronosSource',
    'pretty_name': 'Kronos',  # Displayed to the user
    'url': 'http://localhost:8150',  # Kronos server URL
    'namespace': 'kronos',
  },
}

DATA_SOURCE_ADAPTERS = [
  'metis.core.query.kronos.adapters.Python',
  # 'metis.core.query.kronos.adapters.Spark',
]

# SPARK_HOME = '/path/to/spark-1.0.0'
# SPARK_MASTER = 'local'
