Simple Minecraft Nick Checker

## How to use
```
py src/main.py <args(-arg=value)...>
```

## Arguments
  ### size: Length of the nicks checked. (min 1, max 16)
  ### delay: Delay (in seconds) beetwen each request. (min 1)
  ### req_size: Ammount of nicks checked p/request (min 1, max 10)
  ### only_letters: If true, only checks nicks with letters
  ### log_invalids: If true, logs the invalid nicks in a .txt file (data/invalids.txt)
  ### log_valids: If true, logs the valid nicks in a .txt file (data/invalids.txt)
