#!/usr/bin/env /usr/bin/python2.7
import __future__
import time, os, sys
import argparse
import unittest
import pylxca

try:
    from pylxca.pylxca_cmd.lxca_pyshell import *
    pyshell()
except Exception as e:
    print "-"*20
    print "Error:",e
    print "Sugesstion: Please install pyLXCA before run (try using easy_install pylxca)"
    print "Exiting.."
    print "-"*20
    sys.exit(-1)

def get_args():
    parser = argparse.ArgumentParser(description='pylxca function tests usage')
    parser.add_argument('-l', action='store', dest='lxca_ip', required=True,
                        help='Store LXCA IP value')
    parser.add_argument('-n', action='store_false', default=True,dest='no_verify',
                        help='Set a no_verify to false')
    parser.add_argument('-c', action='append', dest='chassis',required=True, default=[],
                        help='Specify chassis as chassis1,chassis2..',)
    parser.add_argument('-u', action='store', dest='user', type=str, default='USERID',
                        help = 'Specify username. default:"USERID"')
    parser.add_argument('-p', action='store', dest='password', type=str, default = "CME44ibm",
                        help = 'Specify password. default: "CME44ibm" ')
    parser.add_argument('--version', action='version', version='%(prog)s v0.1')

    return(parser.parse_args())

class TestCase(unittest.TestCase):
    arg = get_args()
    _ip          = 'https://' + arg.lxca_ip
    _user        = arg.user
    _passwd      = arg.password
    _noverify    = 'True' if arg.no_verify else 'False'
    _chassis     = arg.chassis
    _conn        = None

    @classmethod
    def setUpClass(self):
        print "Initializing testing environment.."
        self._conn = connect(self._ip, self._user, self._passwd, self._noverify)
        # expecting conn not equal to None
        if self._conn is None:
            raise TypeError("connection to LXCA fails. Check Credentials")

    @classmethod
    def tearDownClass(self):
        print "tearDown testing environment.."
        self._conn.disconnect()
        # expecting conn equal to None
        if self._conn.session is not None:
            raise TypeError("Disconnection to LXCA fails.")

class examples(TestCase):

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    @unittest.skipIf(pylxca.__version__ < (1, 0), #condition
                     "below_test_format function is not supported in this library version") # reason
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass
    def test_examples(self):
        # expecting True
        self.assertTrue(True)
        # expecting equal
        self.assertEqual('val', 'val', 'val must be equal')
        #expecting False
        self.assertFalse(False)

class General(TestCase):
    def test_connect(self):
        self.assertIsNotNone(self._conn, "test_connect should not None")

    def test_disconnect(self):
        self._conn.disconnect()
        self.assertIsNone(self._conn.session, "test_disconnect should None")

    # def test_exit(self):
    #     pass
    #def test_help(self):
    #     pass
    # def test_ostream(self):
    #     pass

    @classmethod
    @unittest.skipIf(1==1, "Skipping tearDown. Not required")
    def tearDownClass(self):
        print "tearDown testing environment.."
        self._conn.disconnect()
        # expecting conn equal to None
        if self._conn.session is not None:
            raise TypeError("Disconnection to LXCA fails.")

class Inventory(TestCase):
    def test_chassis(self):
        chassisList = chassis(self._conn)
        chassisList = chassisList['chassisList']
        self.assertTrue(isinstance(chassisList,list), "ChassList Found")
        if chassisList.__len__() == 0:
            raise ValueError("No chassis is managed")

    def test_cmms(self):
        cmmList = cmms(self._conn)
        cmmList = cmmList['cmmList']
        self.assertTrue(isinstance(cmmList,list), "cmmList Found")
        if cmmList.__len__() == 0:
            raise ValueError("No CMM is Found")

    def test_fanmuxes(self):
        fanMuxList = fanmuxes(self._conn)
        fanMuxList = fanMuxList['fanMuxList']
        self.assertTrue(isinstance(fanMuxList,list), "fanMuxList Found")
        if fanMuxList.__len__() == 0:
            raise ValueError("No fanMuxList is Found")

    def test_fan(self):
        fanList = fans(self._conn)
        fanList = fanList['fanList']
        self.assertTrue(isinstance(fanList,list), "fanList Found")
        if fanList.__len__() == 0:
            raise ValueError("No fanList is Found")

    def test_nodes(self):
        nodeList = nodes(self._conn, status = 'managed')
        nodeList = nodeList['nodeList']
        self.assertTrue(isinstance(nodeList,list), "nodeList Found")
        if nodeList.__len__() == 0:
            raise ValueError("No nodeList is Found")

    def test_powersupplies(self):
        powerList = powersupplies(self._conn)
        self.assertTrue(isinstance(powerList, dict), "powerList Found")
        raise ValueError("TODO list")
        # nodeList = nodeList['nodeList']
        # self.assertTrue(isinstance(nodeList,list), "nodeList Found")
        # if nodeList.__len__() == 0:
        #     raise ValueError("No nodeList is Found")

    def test_scalablesystems(self):
        scalablesystemList = scalablesystem(self._conn)
        self.assertTrue(isinstance(scalablesystemList, dict), "scalablesystemList Found")
        raise ValueError("TODO list")

    def test_switches(self):
        switchesList = switches(self._conn)
        self.assertTrue(isinstance(switchesList, dict), "switchesList Found")
        raise ValueError("TODO list")

class ServerConfiguration(TestCase):
    pass

class EndpointManagement(TestCase):
    def test_discover(self):
        pass
    def test_manage(self):
        pass
    def test_unmanage(self):
        pass
class FirmwareUpdates(TestCase):
    pass

class UserManagement(TestCase):
    pass

class ServiceSupport(TestCase):
    pass

class logs(TestCase):
    pass


if __name__ == "__main__":
#run_method:1
#    unittest.main()

#run_method:2
#    suite = unittest.TestLoader().loadTestsFromTestCase(examples)
#    unittest.TextTestRunner(verbosity=2).run(suite)

#run_method:3
#   suite = unittest.TestSuite()
#   suite.addTest(examples("test_format"))
#   suite.addTest(examples("test_examples"))
#   unittest.TextTestRunner(verbosity=2).run(suite)

# run_method:4
    tests = [Inventory]
    for test in tests:
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        unittest.TextTestRunner(verbosity=2).run(suite)
