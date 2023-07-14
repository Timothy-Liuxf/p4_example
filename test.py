#################################################################################################
# BAREFOOT NETWORKS CONFIDENTIAL & PROPRIETARY
#
# Copyright (c) 2019-present Barefoot Networks, Inc.
#
# All Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property of
# Barefoot Networks, Inc. and its suppliers, if any. The intellectual and
# technical concepts contained herein are proprietary to Barefoot Networks, Inc.
# and its suppliers and may be covered by U.S. and Foreign Patents, patents in
# process, and are protected by trade secret or copyright law.  Dissemination of
# this information or reproduction of this material is strictly forbidden unless
# prior written permission is obtained from Barefoot Networks, Inc.
#
# No warranty, explicit or implicit is provided, unless granted under a written
# agreement with Barefoot Networks, Inc.
#
################################################################################

import logging
import random

from ptf import config
from collections import namedtuple
import ptf.testutils as testutils
from bfruntime_client_base_tests import BfRuntimeTest
import bfrt_grpc.client as gc
import grpc

logger = logging.getLogger('Test')
if not len(logger.handlers):
    logger.addHandler(logging.StreamHandler())

swports = []
for device, port, ifname in config["interfaces"]:
    swports.append(port)
    swports.sort()

if swports == []:
    swports = list(range(9))


class LpmMatchTest(BfRuntimeTest):
    """@brief Basic test for TCAM-based lpm matches.
    """

    def setUp(self):
        client_id = 0
        p4_name = "haha"
        BfRuntimeTest.setUp(self, client_id, p4_name)

    def runTest(self):
        ig_port = swports[1]
        eg_ports = [swports[5], swports[3]]

        seed = random.randint(1, 65535)
        logger.info("Using seed %d", seed)
        random.seed(seed)
        # num_entries = random.randint(5, 10)
        # num_entries = 1
        # print(num_entries)
        ips = (
            "10.0.4.234",
            "10.0.4.235",
            "10.0.4.236",
            "10.0.4.237"
        )
        ports = (
            156,
            164,
            172,
            180
        )
        num_entries = len(ips)

        # Get bfrt_info and set it as part of the test
        bfrt_info = self.interface.bfrt_info_get("haha")

        forward_table = bfrt_info.table_get("SwitchIngress.forward")
        forward_table.info.key_field_annotation_add("hdr.ipv4.dst_addr", "ipv4")

        key_random_tuple = namedtuple('key_random', 'vrf dst_ip prefix_len')
        tuple_list = []
        unique_keys = {}
        ip_list = self.generate_random_ip_list(num_entries, seed)
        lpm_dict = {}
        for i in range(num_entries):
            vrf = 0
            # dst_ip = getattr(ip_list[i], "ip")
            dst_ip = ips[i]
            p_len = 32
            tuple_list.append(key_random_tuple(vrf, dst_ip, p_len))
            logger.info("Adding %d %s %d", vrf, dst_ip, p_len)

            target = gc.Target(device_id=0, pipe_id=0xffff)
            key = forward_table.make_key([gc.KeyTuple('vrf', vrf),
                                         gc.KeyTuple('hdr.ipv4.dst_addr', dst_ip, prefix_len=p_len)])
            data = forward_table.make_data([gc.DataTuple('port', ports[i])],
                                         'SwitchIngress.hit')
            forward_table.entry_add(target, [key], [data])
            key.apply_mask()
            lpm_dict[key] = data

            continue

            # vrf = 0
            # dst_ip = getattr(ip_list[i], "ip")
            # dst_ip = "10.0.4.235"
            # p_len = 32
            # tuple_list.append(key_random_tuple(vrf, dst_ip, p_len))
            # logger.info("Adding %d %s %d", vrf, dst_ip, p_len)

            # target = gc.Target(device_id=0, pipe_id=0xffff)
            # key = forward_table.make_key([gc.KeyTuple('vrf', vrf),
            #                              gc.KeyTuple('hdr.ipv4.dst_addr', dst_ip, prefix_len=p_len)])
            # data = forward_table.make_data([gc.DataTuple('port', 164)],
            #                              'SwitchIngress.hit')
            # forward_table.entry_add(target, [key], [data])
            # key.apply_mask()
            # lpm_dict[key] = data
            # i += 1
            # vrf = 0
            # dst_ip = "10.0.4.236"
            # p_len = 32
            # tuple_list.append(key_random_tuple(vrf, dst_ip, p_len))
            # logger.info("Adding %d %s %d", vrf, dst_ip, p_len)

            # target = gc.Target(device_id=0, pipe_id=0xffff)
            # key = forward_table.make_key([gc.KeyTuple('vrf', vrf),
            #                              gc.KeyTuple('hdr.ipv4.dst_addr', dst_ip, prefix_len=p_len)])
            # data = forward_table.make_data([gc.DataTuple('port', 172)],
            #                              'SwitchIngress.hit')
            # forward_table.entry_add(target, [key], [data])
            # key.apply_mask()
            # lpm_dict[key] = data

