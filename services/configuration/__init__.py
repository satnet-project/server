"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtubiopa@calpoly.edu'

# RPC4django RPC methods automatic detection
from services.configuration.jrpc.views import bands, rules, tle
from services.configuration.jrpc.views.channels import groundstations
from services.configuration.jrpc.views.channels import spacecraft
from services.configuration.jrpc.views.segments import groundstations
from services.configuration.jrpc.views.segments import spacecraft

# It is also necessary to import the signals
from services.configuration.signals import push, tle
