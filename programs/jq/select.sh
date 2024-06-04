cat samsara.json | jq -r 'to_entries[] | select(.value.maxAccelerationGForce > 0)'
