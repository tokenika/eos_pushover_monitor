import configparser
import logging
import time
import urllib.request
import urllib.parse
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

config = configparser.ConfigParser()
config.read('config.ini')

BLOCK_DIFFERENCE_TO_NOTIFY = 120
REFRESH_EVERY_N_SECONDS = 60 * 10
SECONDS_TO_REQUEST_TIMEOUT = 3


def get_info(node_address):
    logger.debug(f'get_info {node_address}')

    request = urllib.request.Request(f'{node_address}/v1/chain/get_info')
    response = urllib.request.urlopen(request, timeout=SECONDS_TO_REQUEST_TIMEOUT)
    return json.load(response)


def send_pushover_notification(network, bp_name):
    message = f'[{network}] Block producer {bp_name} has problems!'
    logger.error(message)

    request_data = urllib.parse.urlencode({
        'token': config['Pushover']['Token'],
        'user': config['Pushover']['UserKey'],
        'message': message,
        'priority': 2,
        'retry': 30,
        'expire': 10800,
    }).encode()
    request = urllib.request.Request('https://api.pushover.net/1/messages.json', data=request_data)
    response = urllib.request.urlopen(request)
    return response


networks = config.sections()
networks.remove('Pushover')

while True:
    for network in networks:
        print(f'Probing network: "{network}"')
        monitor_names = list(filter(None, config[network]['monitor_names'].split(',')))
        monitor = dict()

        head_block = 0

        block_producers = list(config[network])
        block_producers.remove('monitor_names')

        for bp_name in block_producers:
            bp_node_address = config[network][bp_name]
            try:
                bp_info = get_info(bp_node_address)
            except Exception:
                if bp_name in monitor_names:
                    send_pushover_notification(network, bp_name)
                continue

            bp_head_block_num = int(bp_info['head_block_num'])
            if head_block < bp_head_block_num:
                head_block = bp_head_block_num

            if bp_name in monitor_names:
                monitor[bp_name] = bp_head_block_num

        for bp_name in monitor:
            difference = abs(monitor[bp_name] - head_block)
            if difference >= BLOCK_DIFFERENCE_TO_NOTIFY:
                send_pushover_notification(network, bp_name)

    logger.info(f'Waiting {REFRESH_EVERY_N_SECONDS} seconds to check status again.')
    time.sleep(REFRESH_EVERY_N_SECONDS)
