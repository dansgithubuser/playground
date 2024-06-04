cat samsara.json | jq -r 'to_entries[] | select([.value.behaviorLabels[].label] | inside(["harshTurn", "followingDistance"]))'
