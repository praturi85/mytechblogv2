from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.collection import Scope, Collection

# Connect to Couchbase
cluster = Cluster("couchbases://cb.jwj94tyzao6ctshc.cloud.couchbase.com", ClusterOptions(PasswordAuthenticator("admin", "Admin123$")))
bucket = cluster.bucket("techblog")
collection_articles = bucket.scope("default").collection("articles")
collection_comments = bucket.scope("default").collection("comments")
