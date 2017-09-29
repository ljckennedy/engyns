import qrspy.qrspy as qs
import pprint


class QlikLoad:
    """
    gets the load from a QS Engine
    """

    def __init__(self, server, client_cert=False, client_key=False, root=False,):
        userdirectory = 'internal'
        userid = 'sa_repository'
        self.qrs = qs.ConnectQlik(server=server,
                                  certificate=(client_cert, client_key),
                                  root=root,
                                  userdirectory=userdirectory,
                                  userid=userid)
        # pprint.pprint(self.qrs.get_about())

    def get_load(self):
        """
        Gets the Engine Load
        """
        return self.qrs.get_health()
