import multiprocessing
import re

from uuid import getnode

class ServingMode(object):
  ALL = 'all'
  COLLECTOR = 'collector'
  READONLY = 'readonly'

# In debug mode, print every request to standard out.
debug = False

# Profile each request?
profile = False

# If `serving_mode = ServingMode.ALL`, you can access any of the
# endpoints (e.g., `put`, `get`, `delete`, etc.) from this Kronos
# instance.  In production, you will likely want a web-facing Kronos
# instance in `ServingMode.COLLECTOR` mode, which will only open up
# the `put` endpoint.  This way, javascript/frontend logging requests
# can come in from any remote machine, but remote machines can't get
# or delete the data in the Kronos store.
#
# Separately, behind a firewall, you will want to run a server in
# `ServingMode.READONLY` mode, which allows read-only access to the
# data for analytics processing without having to worry about errant
# puts/deletes.
serving_mode = ServingMode.COLLECTOR

# Backend storage engine configurations.  Below, 'memory' is a name we
# assign to an `InMemoryStorage` engine that we'll reference later in
# the configuration.  Check out other backend configurations for
# storage backends like cassandra (tests/conf/cassandra.py).
storage = {
  'memory': {
    'backend': 'kronos.storage.memory.InMemoryStorage',
    'max_items': 100000,
  },
  'cassandra': {
    'backend': 'kronos.storage.cassandra.CassandraStorage',
    'hosts': ['127.0.0.1'],
    'keyspace_prefix': 'kronos_test',
    # Set to a value greater than 0 or you will get an UnavailableException
    'replication_factor': 1,
    'timewidth_seconds': 2,  # Keep this small for test environment.
    'shards_per_bucket': 3,
    'read_size': 10
  },
}

# Default namespace for clients that don't specify one on their requests.
default_namespace = 'kronos'

# Maps namespace => { stream_prefix => {
#                      backends => {
#                        backend_name => {} },
#                      read_backend => backend_name } }
#
# Namespaces are akin to tablespaces/databases in relational database
# systems.  `stream_prefix` allows you to handle different streams in
# a namespace differently.  For example, you might want slightly
# different settings for bursty streams.  Note that while you can
# write to multiple `backends`, you must specify a single
# `read_backend` to return data from. Here's an edited snippet from
# some production systems:
#
# namespace_to_streams_configuration = {
#   default_namespace: {
#     '': {
#      'backends': {
#        'cassandra': {
#          'timewidth_seconds': 60*60*24*7 # 1 week.
#          },
#        'memory': None
#        },
#      'read_backend': 'cassandra'
#      },
#    'product.web.views': {
#      'backends': {
#        'cassandra': {
#          'timewidth_seconds': 60*60 # 1 hour.
#          }
#        },
#      'read_backend': 'cassandra'
#      },
# ...
#
# Let's break this down: for the `default_namespace`, any stream with
# prefix `''` (the default) stores its data into both `cassandra` and
# `memory` (names we set in `storage` above).  The Cassandra time
# width is a week, meaning we bucket a week's worth of data by
# default.  However, streams with the prefix `product.web.views` are
# higher-throughput, and we store them in one-hour buckets to avoid
# overloading a single Cassandra key.  We write the data out to both
# Cassandra and the memory store (our `backends`), but if a user
# retrieves data, we'll pull it out of Cassandra (the `read_backend`).
namespace_to_streams_configuration = {
  default_namespace: {
    '': {
      'backends': {
        'cassandra': {
          'timewidth_seconds': 60*60*24*7 # 1 week.
          },
        'memory': None
        },
      'read_backend': 'cassandra'
      },
    }
  }
}

# Instance-related settings.
node = {
  'id': hex(getnode()),  # Unique ID for this Kronos server.
  'flush_size': 131072,  # Number of bytes to flush at a time for /get endpoint.
  'greenlet_pool_size': 500,  # Greenlet poolsize per process.  Balance against
                              # the parallelism of upstream processes, like
                              # uWSGI.
  'gipc_pool_size': multiprocessing.cpu_count(),
  'log_directory': 'logs',
  'cors_whitelist_domains': map(re.compile, [
    # Domains that match any regex in this list will be allowed to
    # talk to this Kronos instance.  Allows CORS-compliant clients
    # (e.g., web browsers) to respect your wishes for performing XHR
    # requests from only certain domains.
  ])
}

# Stream settings.  `format` specifies what a valid stream name looks
# like. Kronos will use the stream name as part of the key that events
# are stored under for each backend.  Ensure that each backend that
# you use accepts patterns defined by `format`.
stream = {
  'format': re.compile(r'^[a-z0-9\_]+(\.[a-z0-9\_]+)*$', re.I)
}
