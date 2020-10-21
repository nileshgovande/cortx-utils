#!/bin/env python3

# CORTX Python common library.
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.

import errno

from cortx.utils.validator.error import VError
from cortx.utils.process import SimpleProcess


class NetworkV:
    """ Network related validations """

    def validate(self, args):
        """ Process network validations """

        if not isinstance(args, list) or len(args) < 1:
            raise VError(errno.EINVAL, "Invalid parameters %s" % args)

        action = args[0]

        if action == "management_vip":
            self.validate_management_vip(args[1])
        elif action == "cluster_ip":
            self.validate_cluster_ip(args[1])
        elif action == "public_data_ip":
            self.validate_public_data_ip(args[1:])
        elif action == "private_data_ip":
            self.validate_private_data_ip(args[1:])

        raise VError(errno.EINVAL, "Invalid parameter %s" % args)

    def validate_management_vip(self, management_vip):
        """ Validations for Management VIP """

        unreachable_ips = self.validate_ip_connectivity([management_vip])
        if len(unreachable_ips) != 0:
            raise VError(errno.ECONNREFUSED,
                         f"Pinging Management VIP {management_vip} failed")

        return

    def validate_cluster_ip(self, cluster_ip):
        """ Validations for Cluster IP """

        unreachable_ips = self.validate_ip_connectivity([cluster_ip])
        if len(unreachable_ips) != 0:
            raise VError(errno.ECONNREFUSED,
                         f"Pinging Cluster IP {cluster_ip} failed")

        return

    def validate_public_data_ip(self, public_data_ips):
        """ Validations for public data ip """

        unreachable_ips = self.validate_ip_connectivity(public_data_ips)
        if len(unreachable_ips) != 0:
            seperator = ", "
            raise VError(
                errno.ECONNREFUSED, f"Pinging following Public data Ips {seperator.join(unreachable_ips)} failed")

        return

    def validate_private_data_ip(self, private_data_ips):
        """ Validations for private data ip """

        unreachable_ips = self.validate_ip_connectivity(private_data_ips)
        if len(unreachable_ips) != 0:
            seperator = ", "
            raise VError(
                errno.ECONNREFUSED, f"Pinging following Private data Ips {seperator.join(unreachable_ips)} failed")

        return

    def validate_ip_connectivity(self, ips):
        """ Check if IPs are reachable """

        unreachable_ips = []
        for ip in ips:
            cmd = f"ping -c 1 {ip}"
            cmd_proc = SimpleProcess(cmd)
            run_result = cmd_proc.run()

            if run_result[2]:
                unreachable_ips.append(ip)

        return unreachable_ips
