# based on Refine-Python Library

import os.path, time
import requests
import json

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse


class Refine:

    def __init__(self, server_ip='127.0.0.1', server_port=3333):
        self.server = 'http://' + server_ip + ':' + str(server_port)

    def new_project(self, file_path, options=None):
        file_name = os.path.split(file_path)[-1]
        project_name = file_name
        data = {'project-name': project_name}
        files = {'project_file': open(file_path)}
        url = self.server + '/command/core/create-project-from-upload'
        if options is not None:
            url += '?options=' + json.dumps(options)

        response = requests.post(url, data, files=files)
        if response.ok:
            project_id = urlparse.parse_qs(
                response.url.split('?')[-1]
            )['project'][0]
            return RefineProject(self.server, project_id, project_name)

        print "Error at creating project: " + project_name
        return None


class RefineProject:
    def __init__(self, server, id, project_name):
        self.server = server
        self.id = id
        self.project_name = project_name

    def wait_until_idle(self, polling_delay=0.5):
        data = {'project': self.id}
        while True:
            response = requests.post(
                self.server + '/command/core/get-processes', data
            )
            response_json = response.json()
            condition = (
                'processes' in response_json and
                len(response_json['processes']) > 0
            )
            if condition:
                time.sleep(polling_delay)
            else:
                return

    def apply_facet(self, operation={}, wait=True):
        data = {
            'engine': json.dumps(operation)
        }
        response = requests.post(
            self.server + '/command/core/compute-facets?project=' + self.id, data
        )
        response_json = response.json()
        if 'code' in response_json:
            if response_json['code'] == 'error':
                raise Exception(response_json['message'])
            elif response_json['code'] == 'pending':
                if wait:
                    self.wait_until_idle()
                return 'ok'

        return response_json  # can be 'ok' or 'pending'

    def apply_operations(self, file_path, wait=True):
        fd = open(file_path)
        operations_json = fd.read()

        data = {
            'operations': operations_json,
            'project': self.id
        }
        response = requests.post(
            self.server + '/command/core/apply-operations', data
        )
        response_json = response.json()
        if response_json['code'] == 'error':
            raise Exception(response_json['message'])
        elif response_json['code'] == 'pending':
            if wait:
                self.wait_until_idle()
            return 'ok'

        return response_json['code']  # can be 'ok' or 'pending'

    def export_rows(self, format='csv'):
        data = {
            'engine': '{"facets":[],"mode":"row-based"}',
            'project': self.id,
            'format': format
        }
        response = requests.post(
            self.server + '/command/core/export-rows', data
        )
        return response.content

    def delete_project(self):
        data = {
            'project': self.id
        }
        response = requests.post(
            self.server + '/command/core/delete-project', data
        )
        response_json = response.json()
        return 'code' in response_json and response_json['code'] == 'ok'
