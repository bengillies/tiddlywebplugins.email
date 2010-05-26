"""
TODO: add in policy checking and mapping email addresses to users
"""
from tiddlyweb.commands import make_command
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.recipe import Recipe
from tiddlyweb import control
from tiddlywebplugins.utils import get_store
from tiddlyweb.store import Store,NoTiddlerError, NoBagError, NoRecipeError
from tiddlyweb.config import config

import feedparser
import datetime
import logging
import re
from string import Template
