#!/usr/bin/env python
import re
import urllib2
import json
from sys import argv
prog = re.compile("^https://github\.com/([^/]+)/([^/]+)/issues/([0-9]+)$")
SAMPLE_URL = "https://github.com/ScalaWilliam/aptgit/issues/19"
result = prog.search(SAMPLE_URL)
assert result, SAMPLE_URL
assert result.groups() == ("ScalaWilliam", "aptgit", "19"), result.groups()

SAMPLE_DATE = "2018-04-29T06:33:49Z"

price_search = re.compile("Price: (\$\d+)")
SAMPLE_PRICE = "Here is some ... \n\n.. Price: $20.00. \n\n"
result = price_search.search(SAMPLE_PRICE)
assert result, SAMPLE_PRICE
assert result.groups() == ("$20",), result.groups()

url = argv[1]
print "Looking at: %s" % url
result = prog.search(argv[1])
if result:
    (user, repo, issue) = result.groups()
    issue_api_url = "https://api.github.com/repos/%s/%s/issues/%s" % (user, repo, issue)
    article_name = "%s-%s-%s" % (user, repo, issue)
    response = urllib2.urlopen(issue_api_url)
    response_str = response.read()
    obj = json.loads(response_str)
    result = price_search.search(obj['body'])
    assert result, "price not found in body: %s" % obj['body']
    (price) = result.groups()
    
    post_date = obj['created_at'][0:10]
    post_id = "%s-%s" %(post_date, article_name)
    post_file = "_posts/%s.md" % post_id
    post_url = "http://work.scalawilliam.com/%s/" % article_name

    title = "%s: %s" % (repo, obj['title'])
    post_body_lines = [
        "---",
        "title: \"%s\"" % title,
        "price: \"%s\"" % price,
        "date: %s" % post_date,
        "---",
        "",
        "- Issue: [%s](%s)" % (obj['url'], obj['url'])
    ]

    body = "\n".join(post_body_lines)
    with open(post_file, 'w') as f:
        f.write(body)
    
    print "Written to %s." % post_file
    print "Add this to the issue:"
    print ""
    issue_addition_fragments = [
        "Under the [ScalaWilliam Work rules](http://work.scalawilliam.com/rules/),",
        " to reserve this task to yourself, "
        "please say \"I'm taking on this\". ",
        "This was posted on %s" % post_url
    ]
    print "".join(issue_addition_fragments)

    