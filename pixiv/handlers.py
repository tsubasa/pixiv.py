import urllib2

class RedirectCatchHeader(urllib2.HTTPRedirectHandler):

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """ Catch redirect header """
        raise urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
