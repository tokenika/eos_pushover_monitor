Pure Python3 script that monitors chosen EOS Block Producers in configured networks and uses [Pushover](https://pushover.net/) to alert.
## Usage
Copy `config.ini.example` to `config.ini`, set your `Token` to your [application token](https://pushover.net/apps) and `UserKey` which is visible in [dashboard](https://pushover.net/) after you log in.

To specify which Block Producer accounts you desire to monitor, set `monitor_names` value (per network) with comma-separated account names, for example `tokenika,other.bp,yetanother.bp`.

You can add your own networks based on example configuration, in general you can add new networks using sections aka. `[MyNewNetwork]` and list few BP to compare with as `other_bp_account = http://other_bp_node_adress:other_bp_api_port`. 

