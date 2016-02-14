# -*- coding: utf-8 -*-
# Copyright 2015 Kerem Güneş
#    <k-gun@mail.com>
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

class Server():
   """
   Server object.

   @module couch
   @object couch.Server
   @author Kerem Güneş <k-gun@mail.com>
   """

   # Client object.
   # @var couch.Client
   client = None

   def __init__(self, client):
      """
      Object constructor.

      @param  {couch.Client} client
      """
      self.client = client

   def ping(self):
      """
      Ping server.

      @return bool
      """
      return (200 == self.client.head("/").getStatusCode())

   def info(self, key = None):
      """
      Get server info.

      @param  {str} key
      @return {mixed}
      """
      return self.client.get("/").getBodyData(key)

   def version(self):
      """
      Get server version.

      @return {str}
      """
      return self.info("version")

   def getActiveTasks(self):
      """
      Get active tasks.

      @return {list}
      """
      return self.client.get("/_active_tasks").getBodyData()

   def getAllDatabases(self):
      """
      Get all databases.

      @return {list}
      """
      return self.client.get("/_all_dbs").getBodyData()

   def getDatabaseUpdates(self, query = {}):
      """
      Get database events.

      @param  {dict} query
      @return {dict}
      """
      return self.client.get("/_db_updates", query).getBodyData()

   def getLogs(self, query = {}):
      """
      Get server logs.

      @param  {dict} query
      @return {str}
      """
      return self.client.get("/_log", query, {
         "Content-Type": None,
         "Accept": "text/plain",
      }).getBody()

   def getStats(self, path = ""):
      """
      Get server stats.

      @param  {dict} query
      @return {dict}
      """
      return self.client.get("/_stats/"+ path).getBodyData()

   def getUuid(self):
      """
      Get a new uuid.

      @return {str}
      """
      uuids = self.getUuids(1)
      if len(uuids):
         return uuids[0]

   def getUuids(self, count = 1):
      """
      Get new uuid(s).

      @param  {int} count
      @return {list}
      """
      return self.client.get("/_uuids/", {"count": count}).getBodyData("uuids")

   def replicate(self, query = {}):
      """
      Request, configure, or stop, a replication operation.

      @param  {dict} query
      @return {dict}
      @raises {Exception}
      """
      if "source" not in query or "target" not in query:
         raise Exception("Both source & target required!")

      return self.client.post("/_replicate", None, query).getBodyData()

   def restart(self):
      """
      Restarts the CouchDB instance.

      @return {bool}
      """
      return (202 == self.client.post("/_restart").getStatusCode())

   def getConfig(self, section = "", key = ""):
      """
      Get config(s).

      @param  {str} section
      @param  {str} key
      @return {mixed}
      """
      path = "%s/%s" % (section, key)

      return self.client.get("/_config/"+ path).getBodyData()

   def setConfig(self, section, key, value):
      """
      Set a config value.

      @param  {str}   section
      @param  {str}   key
      @param  {mixed} value
      @return {mixed}
      """
      path = "%s/%s" % (section, key)
      response = self.client.put("/_config/"+ path, None, value)

      if 200 == response.getStatusCode():
         return response.getBodyData()

      return False

   def removeConfig(self, section, key):
      """
      Delete a config.

      @param  {str} section
      @param  {str} key
      @return {mixed}
      """
      path = "%s/%s" % (section, key)
      response = self.client.delete("/_config/"+ path)

      if 200 == response.getStatusCode():
         return response.getBodyData()

      return False
