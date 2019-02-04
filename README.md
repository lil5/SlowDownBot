# SlowDownBot
IRC bot that asks people to stop posting for 30 seconds and think

## Requirements

- python3
- ability to set bot to *'op'* on irc channel

## Usage

```
slowircbot.py [options]

OPTIONS:
-h, --help    Show this help message
-k, --kick    Kick people who do not respect the curfew (default off)
-b, --ban     Ban people who do not respect the curfew (default off)
-s, --server  IRC Server (default irc.freenode.net)
-p, --port    IRC Server Port (default 6667)
-n, --nick    Nick of bot (default SlowDownBot)
-c, --channel Channel to enforce curfew on (with #)
-t, --time    Waiting time of curfew in seconds (default 30)

```

> :pensive: If set to `-k` or `--kick` any user can rejoin using this:
>
> `/rejoin #channel`

> :warning: If set to `-b` or `--ban` the user will not be able to return to the channel.

## Example

1. Run bot

   `slowircbot.py -k --server=irc.freenode.net -p6667 --nick=MindfullBot --channel=#testslowbot -t20`

2. In irc channel

   `/op MindfullBot`

## License

[MLP-2.0](https://github.com/lil5/SlowDownBot/blob/master/LICENSE)
