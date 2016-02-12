# -*- coding: utf-8 -*-
# Copyright 2015 Kerem Güneş
#    <http://qeremy.com>
#
# Apache License, Version 2.0
#    <http://www.apache.org/licenses/LICENSE-2.0>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Couch():
   """
   Couch object.

   @module couch
   @object couch.Couch
   @author Kerem Güneş <qeremy[at]gmail[dot]com>
   """

   # Name.
   # @const str
   NAME = "Couch"

   # Version.
   # @const str
   VERSION = "1.0.0"

   # Debug
   # @const bool
   DEBUG = False

   # Config.
   # @var dict
   config = {}

   def __init__(self, config = {}, debug = False):
      """
      Object constructor.

      @param  {dict} config
      @param  {bool} debug
      """
      # check debug option
      if "debug" not in config:
         config["debug"] = debug

      # set debug
      self.DEBUG = config["debug"]

      self.setConfig(config)

   def setConfig(self, config = {}):
      """
      Set config.

      @param  {dict} config
      @return {None}
      """
      if config:
         for i in config:
            self.config[i] = config[i]

   def getConfig(self):
      """
      Get config.

      @return {dict}
      """
      return self.config
