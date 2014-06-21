import json
from django.shortcuts import render
from django.http import Http404, HttpResponse
import hashlib
import requests
import urllib
from django_project.settings import SECRET_KEY, PIVOTAL_API_TOKEN, \
    TOGGL_WORKSPACE_ID, TOGGL_API_TOKEN
import toggl


def _verify_hash(project_id, label, hash_key):
    if not (project_id and label and hash_key):
        raise Http404('Project not found')

    key = "|".join((project_id, label, SECRET_KEY))
    true_hash = hashlib.sha256(key).hexdigest()

    print true_hash, hash_key

    if true_hash != hash_key:
        raise Http404('Project not found')


def _get_json(url):

    print "getting url", url

    res = requests.get(url, headers={"X-TrackerToken": PIVOTAL_API_TOKEN})

    if res.status_code != 200:
        raise Exception('error with pivotal tracker: %s' % res.content)

    return res.json()


def _get_stories(project_id, label):
    url = "https://www.pivotaltracker.com" \
          "/services/v5/projects/%s/stories" \
          "?with_label=%s" % (project_id, label)
    return _get_json(url)


def _get_story(project_id, story_id):
    url = "https://www.pivotaltracker.com" \
          "/services/v5/projects/%s/stories/%s" \
          % (project_id, story_id)
    return _get_json(url)


def _get_tasks(project_id, story_id):
    url = "https://www.pivotaltracker.com" \
          "/services/v5/projects/%s/stories/%s/tasks" \
          % (project_id, story_id)
    return _get_json(url)


def _get_comments(project_id, story_id):
    url = "https://www.pivotaltracker.com" \
          "/services/v5/projects/%s/stories/%s/comments" \
          % (project_id, story_id)
    return _get_json(url)


def stories(request, project_id, tag_filter, hash_key):
    _verify_hash(project_id, tag_filter, hash_key)
    context = {
        'stories': _get_stories(project_id, tag_filter),
        'show_completed': request.GET.get('show_completed'),
    }
    return render(request, 'pivotal_stories.html', context)


def story_details(request, project_id, tag_filter, hash_key, story_id):
    _verify_hash(project_id, tag_filter, hash_key)
    context = {
        'story': _get_story(project_id, story_id),
        'comments': _get_comments(project_id, story_id),
        'tasks': _get_tasks(project_id, story_id),
    }
    return render(request, 'pivotal_story_detail.html', context)


def tasks(request, project_id, tag_filter, hash_key, story_id):
    _verify_hash(project_id, tag_filter, hash_key)
    context = {
        'story': _get_story(project_id, story_id),
        'tasks': _get_tasks(project_id, story_id),
    }
    return render(request, 'pivotal_tasks.html', context)


def tasks(request, project_id, tag_filter, hash_key, story_id):
    _verify_hash(project_id, tag_filter, hash_key)
    found_project = None
    for project in toggl.get_projects(TOGGL_WORKSPACE_ID):
        if project.get('name').endswith('#%s' % story_id):
            found_project = project
            break
    if not found_project:
        return [{'none found'}]
    data = toggl.get_project_hours(TOGGL_WORKSPACE_ID, found_project.get('id'))
    return HttpResponse(json.dumps(data), mimetype='application/json')