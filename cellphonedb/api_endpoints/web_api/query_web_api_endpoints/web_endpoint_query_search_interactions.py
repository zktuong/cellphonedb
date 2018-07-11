import json

from flask import request, Response

from cellphonedb import extensions
from cellphonedb.api_endpoints.web_api.web_api_endpoint_base import WebApiEndpointBase


class WebEndpointQuerySearchInteractions(WebApiEndpointBase):
    def post(self):
        parameters = json.loads(request.get_data(as_text=True))

        receptor = parameters['receptor']

        interactions = extensions.cellphonedb_flask.cellphonedb.query.search_interactions(receptor)

        if interactions.empty:
            self.attach_error(
                {'code': 'result_not_found', 'title': '%s is not CellPhoneDB interactor' % receptor,
                 'details': '%s is not present in CellPhoneDB interactor enabled table' % receptor})
        else:
            self._attach_csv(interactions.to_csv(index=False, sep=','), 'ligands')

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
