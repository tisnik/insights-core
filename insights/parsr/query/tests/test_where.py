import json

from insights.parsr.query import from_dict, make_child_query as q


DATA = json.loads('''
{
  "kind": "ClusterVersion",
  "apiVersion": "config.openshift.io/v1",
  "metadata": {
    "name": "version",
    "selfLink": "/apis/config.openshift.io/v1/clusterversions/version",
    "uid": "11111111-2222-3333-4444-555555555555",
    "resourceVersion": "1",
    "generation": 1,
    "creationTimestamp": "2019-08-04T23:16:46Z"
  },
  "spec": {
    "clusterID": "55555555-4444-3333-2222-111111111111",
    "upstream": "xxxxx://xxx.xxxxxxxxx.xxx/xxx/xxxxxxxxxxxxx/xx/xxxxx",
    "channel": "stable-4.2"
  },
  "status": {
    "desired": {
      "version": "4.2.0-0.ci-2019-08-04-183142",
      "image": "registry.svc.ci.openshift.org/ocp/release@sha256:63b65452005d6e9e45bb92a7505524db0e406c3281d91bdc1a4f5c5cf71b01c5",
      "force": false
    },
    "history": [
      {
        "state": "Completed",
        "startedTime": "2019-08-04T23:17:08Z",
        "completionTime": "2019-08-04T23:32:14Z",
        "version": "4.2.0-0.ci-2019-08-04-183142",
        "image": "registry.svc.ci.openshift.org/ocp/release@sha256:63b65452005d6e9e45bb92a7505524db0e406c3281d91bdc1a4f5c5cf71b01c5",
        "verified": false
      }
    ],
    "observedGeneration": 1,
    "versionHash": "############",
    "conditions": [
      {
        "type": "Available",
        "status": "True",
        "lastTransitionTime": "2019-08-04T23:32:14Z",
        "message": "Done applying 4.2.0-0.ci-2019-08-04-183142"
      },
      {
        "type": "Failing",
        "status": "True",
        "lastTransitionTime": "2019-08-05T15:04:39Z",
        "reason": "ClusterOperatorNotAvailable",
        "message": "Cluster operator console is still updating"
      },
      {
        "type": "Progressing",
        "status": "False",
        "lastTransitionTime": "2019-08-04T23:32:14Z",
        "reason": "ClusterOperatorNotAvailable",
        "message": "Error while reconciling 4.2.0-0.ci-2019-08-04-183142: the cluster operator console has not yet successfully rolled out"
      },
      {
        "type": "RetrievedUpdates",
        "status": "False",
        "lastTransitionTime": "2019-08-04T23:17:08Z",
        "reason": "RemoteFailed",
        "message": "Unable to retrieve available updates: currently installed version 4.2.0-0.ci-2019-08-04-183142 not found in the stable-4.2 channel"
      }
    ],
    "availableUpdates": null
  }
}
''')

d = from_dict(DATA)


def test_values():
    assert d.status.conditions.status.values == ["True", "True", "False", "False"]


def test_where():
    assert len(d.status.conditions.where("type", "Progressing")) == 1

    res = d.status.conditions.where(q("type", "Progressing") | q("status", "True"))
    assert len(res) == 3

    # because only two of the resulting conditions have children named reason.
    assert res.reason.values == ["ClusterOperatorNotAvailable", "ClusterOperatorNotAvailable"]
