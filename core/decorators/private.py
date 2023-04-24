#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
def init(fn):
  async def wrapper(*args,**kwargs):
    message = args[0].message
    print(message)
    if message.chat.type == 'private':
      return await fn(*args,**kwargs)
    else:
      return False
  return wrapper