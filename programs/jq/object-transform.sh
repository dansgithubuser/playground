cat samsara.json | jq -r 'to_entries[] | [.key, .value.vehicle.externalIds["samsara.vin"]] | @tsv'
