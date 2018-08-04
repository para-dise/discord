#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
import asyncio
import discord
import sys
import threading

MAIN_THREAD = threading.current_thread()

TOKENFILE = "tokens.txt"

def create_bot(token):
    if threading.current_thread() != MAIN_THREAD:
        asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    checker = discord.Client(loop=loop)

    @checker.event
    async def on_ready():
        print(checker.http.token)

    checker.run(token, bot=False)

with open(TOKENFILE) as f:
    tokens = [line.rstrip() for line in f]
pool = ThreadPoolExecutor(len(tokens))
futures = [pool.submit(partial(create_bot, token)) for token in tokens]
for x in as_completed(futures):
    print(x.exception())
