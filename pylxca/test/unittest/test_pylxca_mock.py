import mock
from nose.tools import assert_equals
from nose.tools import assert_raises
from nose.tools import assert_true
from nose.tools import assert_is_instance
import requests

from nose.tools import assert_dict_contains_subset
from requests.exceptions import HTTPError
import pylxca.pylxca_api.lxca_connection as lxca_connection

try:
    from pylxca.pylxca_cmd.lxca_pyshell import *
except Exception as e:
    print "-" * 20
    print "Error:", e
    print "Sugesstion: Please install pyLXCA before run (try using easy_install pylxca)"
    print "Exiting.."
    print "-" * 20
    sys.exit(-1)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.text = json_data
        self.status_code = status_code

    def text(self):
        return self.text

    def raise_for_status(self):
        pass
class TestPylxcaApi:
    '''
    this test shows how to mock connect and test_connection method of lxca_connection
    by calling connect of pylxca we expect instance of lxca_connection object as returned
    '''
    @mock.patch("pylxca.pylxca.pylxca_api.lxca_connection.test_connection", autospec=True)
    @mock.patch("pylxca.pylxca.pylxca_api.lxca_connection.connect", autospec=True)
    def test__connect_mock(self, connect_mock, test_connection_mock):

        connect_mock.return_value = True
        test_connection_mock.return_value = True
        con = connect("https://10.240.29.217", "USERID", "Passw0rd", "True")
        print con

        assert_is_instance(con, lxca_connection, "Is not Connection object")

    @mock.patch("pylxca.pylxca.pylxca_cmd.lxca_pyshell.nodes", autospec=True)
    def test__nodes_mock(self,nodes):
        con = connect("https://10.240.29.217","USERID","Passw0rd","True")
        print con
        node_dict = {'nodeList':[]}
        nodes.return_value = node_dict

        ret_nodes = nodes(con)
        print ret_nodes

        assert_equals(ret_nodes, node_dict)

    @mock.patch("pylxca.pylxca.pylxca_api.lxca_rest.get_nodes", autospec=True)
    def test__nodes_rest_mock(self,get_nodes):
        con = connect("https://10.240.29.217","USERID","Passw0rd","True")
        print con
        resp = MockResponse('{"nodeList": []}', 200)
        get_nodes.return_value = resp

        ret_nodes = nodes(con)
        print ret_nodes

        assert_equals(ret_nodes["nodeList"], [])

    @mock.patch("pylxca.pylxca.pylxca_api.lxca_rest.get_nodes", autospec=True)
    def test__nodes_rest_mock_exception(self,get_nodes):
        con = connect("https://10.240.29.217","USERID","Passw0rd","True")
        print con
        resp = MockResponse('{"nodeList": []}', 200)
        #get_nodes.side_effect = HTTPError(mock.Mock(status=404), 'not found')
        get_nodes.side_effect = Exception("Invalid argument 'status'")
        get_nodes.return_value = resp
        assert_raises(Exception,nodes, con)

    # invalid status parameter for nodes should throw exception
    def test__nodes_invalid_status_exception(self):
        con = connect("https://10.240.29.217","USERID","Passw0rd","True")
        assert_raises(Exception,nodes, con,None,None,"unknown")

    @mock.patch.object(requests, 'get')
    def test__nodes_valid_status(self, request_get):
        request_get.return_value = MockResponse('{"nodeList": []}', 200)
        con = connect("https://10.240.29.217","USERID","Passw0rd","True")
        try:
            nodes(con, None, None,"managed")
        except :
            assert_true(False," Got exception and not expecting it")

        assert_true(True," No Exception")

    @mock.patch('requests.session')
    def test_should_mock_session_get(self, session_mock):
        session_mock.return_value = mock.MagicMock(get=mock.MagicMock(return_value=MockResponse('{"nodeList": []}', 200)))
        con = connect("https://10.240.29.217", "USERID", "Passw0rd", "True")
        try:
            nodes(con, None, None, "managed")

        except Exception as e:
            print str(e)
            assert_true(False, " Got exception and not expecting it")

        assert_true(True, " No Exception")
