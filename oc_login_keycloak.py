#!/usr/bin/env python3
# 
# Python Wrapper for requesting a login token for OpenShift 4 clusters using the Keycloak IDP
#
# @author Simon Lauger <simon@lauger.de>

import os
import re
import requests
import html

# cluster and it's credentials
cluster  = os.getenv('OPENSHIFT_CLUSTER')
username = os.getenv('OPENSHIFT_USERNAME')
password = os.getenv('OPENSHIFT_PASSWORD')

# api urls
login_url = "https://oauth-openshift.apps.{}/oauth/token/request".format(cluster)
token_url = "https://oauth-openshift.apps.{}/oauth/token/display".format(cluster)

# start python requests session
session = requests.Session()

# request to login page (redirects to keycloak)
login_page = session.get(login_url)

# extract target url
login_url_idp = html.unescape(re.search('action="(.*)" method="post"', login_page.text).group(1))

idp_page = session.post(login_url_idp, data={
    'username': username,
    'password': password,
  },
)

# CSRF stuff
code = re.search('<input type="hidden" name="code" value="(.*)">', idp_page.text).group(1)
csrf = re.search('<input type="hidden" name="csrf" value="(.*)">', idp_page.text).group(1)

# request token
token_page = session.post(token_url, data={
    'code': code,
    'csrf': csrf,
  },
)

# print out our token
print(re.search('<code>(.*)</code>', token_page.text).group(1))
