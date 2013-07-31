import unittest
from misc       import printdoc
from cloudfiles import ConnectionPool, Connection
from cloudfiles.authentication import MockAuthentication as Auth

class ConnectionPoolTest(unittest.TestCase):
    """
    ConnectionPool class tests.
    """
    @printdoc
    def test_connection(self):
        """
        Verify that ConnectionPool returns a Connection
        """
        conn = self.connpool.get()
        self.assert_(isinstance(conn, Connection))
        self.connpool.put(conn)

    @printdoc
    def test_connection(self):
        """
        Verify that ConnectionPool passes arguments through to Connections
        """
        conn = self.connpool.get()
        self.assert_(self.connpool.maxsize == 22)
        self.assert_(conn.timeout == 33)
        self.connpool.put(conn)

    def setUp(self):
        self.auth = Auth('jsmith', 'qwerty')
        self.connpool = ConnectionPool(auth=self.auth,
                                  poolsize=22,
                                  timeout=33,
                                  )
    def tearDown(self):
        del self.connpool
        del self.auth


# vim:set ai sw=4 ts=4 tw=0 expandtab:
