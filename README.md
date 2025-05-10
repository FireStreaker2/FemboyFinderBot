<div align="center">
  <div>
    <img src="./images/astolfo.jpg" height="128" />
    <h1>FemboyFinderBot</h1>
  </div>

  <div>
    <img src="https://img.shields.io/badge/Made%20for-Femboys-pink" />
    <img src="https://img.shields.io/badge/Made%20with-Pycord-blue" />
  </div>
</div>

# About

A simple image bot that uses the [FemboyFinder API](https://github.com/FireStreaker2/FemboyFinder#api) to bring images to discord! Supports both guild install AND user install.

# Usage

## Setup

```bash
$ git clone https://github.com/FireStreaker2/FemboyFinderBot.git
$ cd FemboyFinderBot
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ systemctl start redis
$ cp .env.example .env
$ python main.py
```

## Statistics

Please install redis with your system's respective package manager before starting it! Redis is used to keep track of total femboy usage.

### Backups

If you would like to keep snapshots of your redis data you can edit your redis config like so:

```
# /etc/redis/redis.conf
save 900 1
save 300 10
save 60 10000

dbfilename dump.rdb
dir ./
rdbcompression yes
rdbchecksum yes
```

## Sharding

By default the bot is sharded, as the official instance is thousands of servers. If you are selfhosting it is likely you will be starting from very little servers, in which case it would be better to disable sharding initially. For more info, please refer to the [official discord documentation](https://discord.com/developers/docs/events/gateway#sharding).

```diff
# main.py
- bot = commands.AutoShardedBot(intents=config["intents"])
+ bot = commands.Bot(intents=config["intents"])
```

## Configuration

When running the bot, there are a few environment variables that can be added in order to customize it.

- `TOKEN`: The bot token
- `STATUS`: What the bot is "watching"
- `FEMBOY_COUNT`: Manually set the amount of femboys found so far
- `MONTHLY_RESET`: Whether to reset the count every month
- `API`: API endpoint for [FemboyFinder](https://github.com/FireStreaker2/FemboyFinder)

> Note that the `FEMBOY_COUNT` can also be achieved via `redis-cli`!

## Commands

| Command  | Description                           |
| -------- | ------------------------------------- |
| `/find`  | Find an image with the specified tags |
| `/about` | Send the about message                |
| `/stats` | Send the bot statistics               |
| `/help`  | Send the help message                 |

# Support

For support regarding FemboyFinderBot, you can join our Discord server:
[![Support Server](https://invidget.switchblade.xyz/bruQhB8Eg5?theme=dark)](https://discord.gg/bruQhB8Eg5)

# License

[MIT](https://github.com/FireStreaker2/FemboyFinderBot/blob/main/LICENSE)
