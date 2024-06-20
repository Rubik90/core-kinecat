"""Hooks to modify the Cat's flow of execution.

Here is a collection of methods to hook into the Cat execution pipeline.

"""

from cat.mad_hatter.decorators import hook
from cat.log import log

@hook(priority=1)
def before_cat_reads_message(user_message_json: dict, cat) -> dict:
    
    return user_message_json


@hook(priority=1)
def before_cat_sends_message(message: dict, cat):
  

    return message
