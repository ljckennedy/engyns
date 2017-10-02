"""engynsresource - qlik sense load balancing"""
import pprint
import random
import json
import falcon
import load
import time


class Prioritize(object):
    """Prioritize load balancing requests"""
    loads = {}

    def on_get(self, req, resp):
        """Handles GET requests"""
        pprint.pprint(req.headers)
        pprint.pprint(req.params)
        engines = req.get_param('engines') or None
        if not engines:
            resp.status = falcon.HTTP_418
            resp.body = ('\nThere is Nothing here - have a coffee\n')
        elif engines == 'all':
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = ('\nEngine prioritize requested: ' + engines)
        else:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = (
                '\nEngines prioritize requested (unknown): ' + engines)

    def on_post(self, req, resp):
        # pprint.pprint(req.headers)
        # pprint.pprint(req.params)
        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            doc = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')
        print('In: ')
        pprint.pprint(doc['QlikSenseEngines'])
        doc['QlikSenseEngines'] = self.balance(doc['QlikSenseEngines'])
        localtime = time.asctime(time.localtime(time.time()))
        print('Out: ' + localtime)
        pprint.pprint(doc['QlikSenseEngines'])
        # pprint.pprint(self.loads)
        resp.body = json.dumps(doc)

    def balance(self, qse):
        """
        calculate who gets the session
        """
        #print('Load balancing: ', qse)
        for en in qse:
            # hack  need to re-write
            engine = en[en.index('//') + 2:en.rindex(':')]
            server = engine + ':4242'
            #print('Engine is ', server)
            myload = load.QlikLoad(server=server,
                                   client_cert='C:/Dev/code/Python/qmi-qs-mn/client.pem',
                                   client_key='C:/Dev/code/Python/qmi-qs-mn/client_key.pem',
                                   root='C:/Dev/code/Python/qmi-qs-mn/root.pem')
            self.loads[en] = myload.get_load()
            pprint.pprint(self.loads[en]['apps']['calls'])
            # this is where I am up to
        srt = [item[0] for item in sorted(
            self.loads.items(), key=lambda k_v: k_v[1]['apps']['calls'], reverse=False)]
        # pprint.pprint(srt)
        # if random.randint(1, 2) == 2:
        #     print('Forced error')
        #     return ''
        # else:
        return srt


class Control(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        engines = req.get_param('engines') or None
        if not engines:
            resp.status = falcon.HTTP_418
            resp.body = ('\nThere is Nothing here - have a coffee\n')
        elif engines == 'all':
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = ('\nEngine control requested: ' + engines)
        else:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = ('\nEngine control requested (unknown): ' + engines)
