# Login Wrappers for OpenShift 4

This repository contains python based login wrappers for external OpenShift 4 IDPs.

## Background

Because of an limitation in the OpenID implementation in OpenShift 4, it is currently not possible to login via `oc login` with your username and password.

Instead you need to login with your OpenShift token, which could be created via the web ui. 

Maybe you're looking for a solution to login via command line only (e.g. for a login in your CI Pipeline). This repository could help you here. It contains python based login wrappers for different IDPs. The wrapper takes care of obtaining the OpenShift token for you.

## Usage

Credentials can be provided via environment variables.

```
export OPENSHIFT_CLUSTER=clusterid.clusterdomain.com
export OPENSHIFT_USERNAME=slauger
export OPENSHIFT_PASSWORD=Z29ob21leW91YXJlZHJ1bmsK

-bash$ oc login https://api.${OPENSHIFT_CLUSTER}:6443 --token $(./oc_login_keycloak.py)
Logged into "https://api.clusterid.clusterdomain.com:6443" as "slauger" using the token provided.
```

## Currently available wrappers

- Keycloak

## On the Roadmap

- Microsoft ADFS
- Gitlab (optional with 2FA)

## Authors

- [slauger](https://github.com/slauger)
