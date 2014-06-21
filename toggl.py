import json
from os import getenv
import requests
from requests.auth import HTTPBasicAuth

session = None


def get_session():
    global session
    if not session:
        session = requests.session()
        session.auth = HTTPBasicAuth(getenv('TOGGL_API_TOKEN'), 'api_token')
        session.headers['Content-type'] = 'application/json'
    return session


def get(url):
    if not url.startswith('http'):
        url = 'https://www.toggl.com' + url
    return get_session().get(url)


def post(url, data):
    if not url.startswith('http'):
        url = 'https://www.toggl.com' + url
    return get_session().post(url, data)


def get_projects(workspace_id):
    url = '/api/v8/workspaces/%s/projects' % workspace_id
    res = get(url)
    if res.status_code != 200:
        raise Exception('Error getting Toggl projects (%s): %s, %s' %
                        (url, res.status_code, res.content))
    else:
        return res.json()


def create_project(name, workspace_id, client_id):
    url = '/api/v8/projects'
    data = {
        'project': {
            'name': name,
            'wid': workspace_id,
            'cid': client_id,
            'is_private': False
        }
    }
    res = post(url=url, data=json.dumps(data))
    if 200 <= res.status_code < 300:
        return res.json()
    else:
        raise Exception('Error creating project (%s): %s, %s' %
                        (url, res.status_code, res.content))


def get_clients(workspace_id):
    url = '/api/v8/workspaces/%s/clients' % workspace_id
    res = get(url)
    if res.status_code != 200:
        raise Exception('Error getting Toggl projects (%s): %s, %s' %
                        (url, res.status_code, res.content))
    else:
        return res.json()


def get_project_hours(workspace_id, project_id):
    url = ('/reports/api/v2/details?user_agent=toggl_at_ccp.io'
           '&since=2014-01-01'
           '&workspace_id=%s'
           '&project_ids=%s' % (workspace_id, project_id))
    res = get(url)
    if res.status_code != 200:
        raise Exception('Error getting Toggl time entries (%s): %s, %s' %
                        (url, res.status_code, res.content))
    else:
        return res.json().get('data')