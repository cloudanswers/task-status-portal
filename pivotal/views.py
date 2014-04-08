from django.shortcuts import render
from django.http import Http404
import hashlib
import requests
import urllib
from django_project.settings import SECRET_KEY, PIVOTAL_API_TOKEN


def _verify_hash(project_id, label, hash_key):
    if not (project_id and label and hash_key):
        raise Http404('Project not found')

    key = "|".join((project_id, label, SECRET_KEY))
    true_hash = hashlib.sha256(key).hexdigest()

    if true_hash != hash_key:
        raise Http404('Project not found')


def _get_stories(project_id, label):
    stories_url = "https://www.pivotaltracker.com" \
                  "/services/v5/projects/%s/stories" \
                  "?with_label=%s" % (project_id, label)
    res = requests.get(stories_url,
                       headers={"X-TrackerToken": PIVOTAL_API_TOKEN})
    if res.status_code != 200:
        raise Exception('error with pivotal tracker: %s' % res.content)

    return res.json()


def stories(request, project_id, tag_filter, hash_key):
    _verify_hash(project_id, tag_filter, hash_key)
    context = {
        'stories': _get_stories(project_id, tag_filter),
    }
    return render(request, 'pivotal_stories.html', context)