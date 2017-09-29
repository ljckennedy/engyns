# engyns.py
# Load balancer for Qlik Sense
import falcon
import engynsresource
import waitress


# falcon.API instances are callable WSGI apps
# waitress-serve --port=8000 engyns:app
# to run this
app = falcon.API()

# things will handle all requests to the '/things' URL path
app.add_route('/loadbalancing/control', engynsresource.Control())
app.add_route('/loadbalancing/prioritize', engynsresource.Prioritize())


waitress.serve(app, port=8000, url_scheme='http')
