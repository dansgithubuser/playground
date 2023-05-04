cat log.txt | grep --line-buffered --color=always -i -E '^|error' | GREP_COLORS='ms=01;33' grep --line-buffered --color=always -i -E '^|warn'
