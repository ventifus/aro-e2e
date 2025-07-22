#!/usr/bin/python
#
# Copyright (c) 2020  haiyuazhang <haiyzhan@micosoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from types import LambdaType
from os import path

__metaclass__ = type


DOCUMENTATION = """
---
module: azure_rm_openshifthcpcluster
version_added: '1.2.0'
short_description: Manage Azure Red Hat OpenShift HCP Cluster instance
description:
    - Create, update and delete instance of Azure Red Hat OpenShift HCP Cluster instance.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - Resource name.
        required: true
        type: str
    location:
        description:
            - Resource location.
        required: true
        type: str
    TODO
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Andrew Denton (@ventifus)
"""

EXAMPLES = """
- name: Create openshift cluster
  azure_rm_openshifthcpcluster:
    resource_group: "myResourceGroup"
    name: "myCluster"
    location: "eastus"
    cluster_profile:
      cluster_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/clusterResourceGroup"
      domain: "mydomain"
    service_principal_profile:
      client_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      client_secret: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    network_profile:
      pod_cidr: "10.128.0.0/14"
      service_cidr: "172.30.0.0/16"
    worker_profiles:
      - name: worker
        vm_size: "Standard_D4s_v3"
        subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/Microsoft.Network/virtualNetworks/myVnet/subnets/worker"
        disk_size: 128
        count: 3
    master_profile:
      vm_size: "Standard_D8s_v3"
      subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/master"
- name: Create openshift cluster with multi parameters
  azure_rm_openshifthcpcluster:
    resource_group: "myResourceGroup"
    name: "myCluster"
    location: "eastus"
    cluster_profile:
      cluster_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/clusterResourceGroup"
      domain: "mydomain"
      fips_validated_modules: Enabled
    service_principal_profile:
      client_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      client_secret: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    network_profile:
      pod_cidr: "10.128.0.0/14"
      service_cidr: "172.30.0.0/16"
      outbound_type: Loadbalancer
      preconfigured_nsg: Disabled
    worker_profiles:
      - name: worker
        vm_size: "Standard_D4s_v3"
        subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/Microsoft.Network/virtualNetworks/myVnet/subnets/worker"
        disk_size: 128
        count: 3
        encryption_at_host: Disabled
    master_profile:
      vm_size: "Standard_D8s_v3"
      subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/master"
      encryption_at_host: Disabled
- name: Delete OpenShift HCP Cluster
  azure_rm_openshifthcpcluster:
    resource_group: myResourceGroup
    name: myCluster
    location: eastus
    state: absent
"""

RETURN = """
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/xx-xx-xx-xx/resourceGroups/mycluster-eastus/providers/Microsoft.RedHatOpenShift/hcpOpenShiftClusters/mycluster
name:
    description:
        - Resource name.
    returned: always
    type: str
    sample: mycluster
type:
    description:
        - Resource type.
    returned: always
    type: str
    sample: Microsoft.RedHatOpenShift/hcpOpenShiftClusters
location:
    description:
        - Resource location.
    returned: always
    type: str
    sample: eatus
properties:
    description:
        - Properties of a OpenShift HCP Cluster.
    returned: always
    type: complex
    sample: null
    contains:
        TODO
"""

import time
import json
import random
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient, SendRequestException


class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMHCPOpenShiftManagedClusters(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            location=dict(type="str", required=True),
            name=dict(type="str", required=True),
            resource_group=dict(
                type="str",
                required=True,
            ),
            managed_resource_group=dict(type="str", required=False),
            subnet_id=dict(
                type="str",
                required=True,
            ),
            network_security_group_id=dict(
                type="str",
                required=True,
            ),
            network=dict(
                type="dict",
                required=False,
                options=dict(
                    network_type=dict(type="str", choices=["OVNKubernetes"], default="OVNKubernetes"),
                    pod_cidr=dict(type="str", required=False, default="10.128.0.0/14"),
                    service_cidr=dict(type="str", required=False, default="172.30.0.0/16"),
                    machine_cidr=dict(type="str", required=False, default="10.0.0.0/16"),
                    host_prefix_length=dict(type="int", required=False, default=23),
                ),
                default=dict(
                    network_type="OVNKubernetes",
                    pod_cidr="10.128.0.0/14",
                    service_cidr="172.30.0.0/16",
                    machine_cidr="10.0.0.0/16",
                    host_prefix_length=23,
                ),
            ),
            api_visibility=dict(
                type="str",
                required=False,
                choices=["Public", "Private"],
                default="Public",
            ),
            outbound_type=dict(
                type="str",
                required=False,
                choices=["LoadBalancer", "UserDefinedRouting"],
                default="LoadBalancer",
            ),
            version=dict(
                type="str",
                required=True,
            ),
            channel_group=dict(
                type="str",
                required=False,
                default="stable"
            ),
            control_plane_identities=dict(
                type="dict",
                required=True,
            ),
            data_plane_identities=dict(
                type="dict",
                required=True,
            ),
            service_identity=dict(
                type="str",
                required=True,
            ),
            rp_mode=dict(type="str", choices=["production", "development"], default="production"),
            api_version=dict(type="str", default="2024-06-10-preview"),
        )

        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction

        self.body = {}
        self.body["properties"] = {}
        self.query_parameters = {}
        self.header_parameters = {}

        self.header_parameters["Content-Type"] = "application/json; charset=utf-8"
        self.rp_mode = None
        self.api_version = None

        super(AzureRMHCPOpenShiftManagedClusters, self).__init__(
            derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=True
        )

    def get_resource_id(self):
        return path.join(
            "subscriptions",
            self.subscription_id,
            "resourceGroups",
            self.resource_group,
            "providers",
            "Microsoft.RedHatOpenShift",
            "hcpOpenShiftclusters",
            self.name,
        )

    def exec_module(self, **kwargs):
        self.body = {
            "properties": {
                "version": dict(),
                "dns": dict(),
                "network": dict(),
                "console": dict(),
                "api": dict(),
                "platform": {
                    "operatorsAuthentication": {
                        "userAssignedIdentities": dict(),
                    },
                },
            },
            "identity": {
                "type": "UserAssigned",
                "userAssignedIdentities": dict(),
            },
        }
        for key in list(self.module_arg_spec.keys()) + ["tags"]:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == "managed_resource_group":
                    self["properties"]["platform"]["managedResourceGroup"] = kwargs[key]
                elif key == "subnet_id":
                    self.body["properties"]["platform"]["subnetId"] = kwargs[key]
                elif key == "network_security_group_id":
                    self.body["properties"]["platform"]["networkSecurityGroupId"] = kwargs[key]
                elif key == "api_visibility":
                    self.body["properties"]["api"]["visibility"] = kwargs[key]
                elif key == "outbound_type":
                    self.body["properties"]["platform"]["outboundType"] = kwargs[key]
                elif key == "version":
                    self.body["properties"]["version"]["id"] = kwargs[key]
                elif key == "channel_group":
                    self.body["properties"]["version"]["channelGroup"] = kwargs[key]
                elif key == "network":
                    network = dict()
                    network_type = kwargs[key].get("network_type")
                    if network_type:
                        network["networkType"] = network_type
                    pod_cidr = kwargs[key].get("pod_cidr")
                    if pod_cidr:
                        network["podCidr"] = pod_cidr
                    service_cidr = kwargs[key].get("service_cidr")
                    if service_cidr:
                        network["serviceCidr"] = service_cidr
                    machine_cidr = kwargs[key].get("machine_cidr")
                    if machine_cidr:
                        network["machineCidr"] = machine_cidr
                    host_prefix_length = kwargs[key].get("host_prefix_length")
                    if host_prefix_length:
                        network["hostPrefix"] = host_prefix_length
                    if network:
                        self.body["properties"]["network"] = network
                elif key == "service_identity":
                    self.body["identity"]["userAssignedIdentities"][kwargs[key]] = dict()
                    self.body["properties"]["platform"]["operatorsAuthentication"]["userAssignedIdentities"]["serviceManagedIdentity"] = kwargs[key]
                elif key == "control_plane_identities":
                    for v in kwargs[key].values():
                        self.body["identity"]["userAssignedIdentities"][v] = dict()
                    self.body["properties"]["platform"]["operatorsAuthentication"]["userAssignedIdentities"]["controlPlaneOperators"] = kwargs[key]
                elif key == "data_plane_identities":
                    # data plane identities don't go in self.body["identity"]["userAssignedIdentities"]
                    self.body["properties"]["platform"]["operatorsAuthentication"]["userAssignedIdentities"]["dataPlaneOperators"] = kwargs[key]
                else:
                    self.body[key] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(
            GenericRestClient, base_url=self._cloud_environment.endpoints.resource_manager
        )
        self.query_parameters["api-version"] = self.api_version
        self.results["api_version"] = self.api_version
        if self.rp_mode != "production":
            self.results["rp_mode"] = self.rp_mode

        self.url = self.get_resource_id()

        old_response = self.get_resource()

        if not old_response:
            self.log("OpenShiftHCPCluster instance doesn't exist")

            if self.state == "absent":
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log("OpenShiftHCPCluster instance already exists")

            if self.state == "absent":
                self.to_do = Actions.Delete
            else:
                self.results["id"] = old_response["id"]
                self.results["name"] = old_response["name"]
                self.results["type"] = old_response["type"]
                self.results["location"] = old_response["location"]
                self.results["properties"] = old_response["properties"]
                self.results["tags"] = old_response.get("tags")
                self.results["systemData"] = old_response.get("systemData")
                return self.results

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log("Need to Create / Update the OpenShiftManagedCluster instance")

            if self.check_mode:
                self.results["changed"] = True
                return self.results

            response = self.create_update_resource()

            self.results["changed"] = True
            self.log("Creation / Update done")
        elif self.to_do == Actions.Delete:
            self.log("OpenShiftManagedCluster instance deleted")
            self.results["changed"] = True

            if self.check_mode:
                return self.results

            self.delete_resource()

            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_resource():
                time.sleep(20)
        else:
            self.log("OpenShiftManagedCluster instance unchanged")
            self.results["changed"] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]
            self.results["name"] = response["name"]
            self.results["type"] = response["type"]
            self.results["location"] = response["location"]
            self.results["properties"] = response["properties"]
            self.results["identity"] = response.get("identity")
            self.results["tags"] = response.get("tags")
            self.results["systemData"] = response.get("systemData")

        return self.results

    def create_update_resource(self):
        if self.to_do == Actions.Create:
            self.set_default()
        # RP_MODE=development hack
        if self.rp_mode == "development":
            self.mgmt_client._client._base_url = "https://localhost:8443/"
            self.mgmt_client._client._pipeline._transport.connection_config.verify = False

        try:
            response = self.mgmt_client.query(
                self.url, "PUT", self.query_parameters, self.header_parameters, self.body, self.status_code, 600, 30
            )
        except SendRequestException as e:
            self.log("Error attempting to create the OpenShiftManagedCluster instance.")
            error_code = None
            error_message = None
            if e.response.startswith("{"):
                err = json.loads(e.response)
                if "error" in err:
                    error_code = err["error"].get("code")
                    error_message = err["error"].get("message")
                    error_target = err["error"].get("target")
                    if error_target:
                        error_message += f" (target: {error_target})"
                    error_details = err["error"].get("details")
                    if error_details:
                        for detail in error_details:
                            error_message += f"\n -- {detail.get('code')}: {detail.get('message')} ({detail.get('target')})"
            if error_code and error_message:
                self.fail(f"Error creating OpenShiftManagedCLuster: {e.status_code}: {error_code}: {error_message} -- {e}\n\n{self.body}")
            else:
                self.fail(f"Error creating OpenShiftManagedCluster: {e.status_code}: {e.response}")
        except Exception as e:
            self.log("Error attempting to create the OpenShiftManagedCluster instance.")
            self.fail(f"Error creating the OpenShiftManagedCluster instance: {self.url}: {e}\n\n{self.body}")

        if hasattr(response, "body"):
            response = json.loads(response.body())
        elif hasattr(response, "context"):
            response = response.context["deserialized_data"]
        else:
            self.fail(f"Create or Updating fail, no match message return, return info as {response}")

        return response

    def delete_resource(self):
        # self.log('Deleting the OpenShiftManagedCluster instance {0}'.format(self.))
        if self.rp_mode == "development":
            self.mgmt_client._client._base_url = "https://localhost:8443/"
            self.mgmt_client._client._pipeline._transport.connection_config.verify = False
        try:
            response = self.mgmt_client.query(
                self.url, "DELETE", self.query_parameters, self.header_parameters, None, self.status_code, 600, 30
            )
            self.log(f"Delete response: {response}")
        except Exception as e:
            self.log("Error attempting to delete the OpenShiftManagedCluster instance.")
            self.fail(f"Error deleting the OpenShiftManagedCluster instance: {e}")

        return True

    def get_resource(self):
        # self.log('Checking if the OpenShiftManagedCluster instance {0} is present'.format(self.))
        found = False
        try:
            if self.rp_mode == "development":
                self.mgmt_client._client._base_url = "https://localhost:8443/"
                self.mgmt_client._client._pipeline._transport.connection_config.verify = False

            response = self.mgmt_client.query(
                self.url, "GET", self.query_parameters, self.header_parameters, None, self.status_code, 600, 30
            )
            found = True
            response = json.loads(response.body())
            found = True
            self.log(f"Response: {response}")
            # self.log("OpenShiftManagedCluster instance : {0} found".format(response.name))
        except Exception as e:
            self.log("Did not find the OpenShiftManagedCluster instance.")
        if found is True:
            return response

        return False

    def random_id(self):
        random_id = "".join(random.choice("abcdefghijklmnopqrstuvwxyz")) + "".join(
            random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for key in range(7)
        )
        return random_id

    def set_default(self):
        pass


def main():
    AzureRMHCPOpenShiftManagedClusters()


if __name__ == "__main__":
    main()
