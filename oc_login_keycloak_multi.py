#!/usr/bin/env python3
# 
# Python Wrapper for requesting a login token for OpenShift 4 clusters using the Keycloak IDP
#
# Use this one if multiple IDPs are installed in your OpenShift cluster.
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
idp      = os.getenv('OPENSHIFT_IDP')

# api urls
base_url = "https://oauth-openshift.apps.{}".format(cluster)
login_url = "https://oauth-openshift.apps.{}/oauth/token/request".format(cluster)
token_url = "https://oauth-openshift.apps.{}/oauth/token/display".format(cluster)

# start python requests session
session = requests.Session()

# request to login page (redirects to keycloak)
openshift_login_content = session.get(login_url)

# extract target url
keycloak_url = html.unescape(re.search('href="(\/oauth\/authorize\?.*idp={}.*response_type=code)"'.format(idp), openshift_login_content.text).group(1))

# extract post url
keycloak_content = session.get(base_url + keycloak_url)
keycloak_login_url = html.unescape(re.search('action="(.*)" method="post"', keycloak_content.text).group(1))

keycloak_login_content = session.post(keycloak_login_url, data={
    'username': username,
    'password': password,
  },
)

# CSRF stuff
code = re.search('<input type="hidden" name="code" value="(.*)">', keycloak_login_content.text).group(1)
csrf = re.search('<input type="hidden" name="csrf" value="(.*)">', keycloak_login_content.text).group(1)

# request token
token_page = session.post(token_url, data={
    'code': code,
    'csrf': csrf,
  },
)

# print out our token
print(re.search('<code>(.*)</code>', token_page.text).group(1))
