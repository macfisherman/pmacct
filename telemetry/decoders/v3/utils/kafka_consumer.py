#
#   pmacct (Promiscuous mode IP Accounting package)
#   pmacct is Copyright (C) 2003-2020 by Paolo Lucente
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
#   pmgrpcd and its components are Copyright (C) 2018-2020 by:
#
#   Matthias Arnold <matthias.arnold@swisscom.com>
#   Raphaël P. Barazzutti <raphael@barazzutti.net>
#   Juan Camilo Cardona <jccardona82@gmail.com>
#   Thomas Graf <thomas.graf@swisscom.com>
#   Paolo Lucente <paolo@pmacct.net>
#
from confluent_kafka import Consumer, KafkaError
import sys
from optparse import OptionParser

DEFAULT_TOPIC = "daisy.test.device-avro-raw"
DEFAULT_SERVER = "kafka.sbd.corproot.net:9093"
parser = OptionParser()
parser.add_option(
    "-t",
    "--topic",,
    default=str(DEFAULT_TOPIC),
    dest="topic",
    help="Topic to listen",
)
parser.add_option(
    "-s",
    "--servers",,
    default=str(DEFAULT_SERVER),
    dest="servers",
    help="Kafka servers",
)

(options, _) = parser.parse_args()

c = Consumer({
    'bootstrap.servers': options.servers,
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe([options.topic])
#c.subscribe(['Cisco-IOS-XR-qos-ma-oper.qos.nodes.node.policy-map.interface-table.interface.member-interfaces.member-interface.output.service-policy-names.service-policy-instance.statistics'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()
