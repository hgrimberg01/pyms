pyms
====

A simple memory status(like ps, only with memory) to display memory statistics. Written in Python 2 hence the Py. 
Project for EECS 678 - Operating Systems to learn about memory maps
and /procfs

WARNING - MUST HAVE ROOT PERMISSIONS


﻿Requirements:

-Superuser priveleges

-Python 2.6+



Instructions:

(assuming python is on system PATH)

sudo python ms.py

OR


Give ms.py execute permissions

chmod +x ms.py

and then

./ms.py


***********
The only flag is 

--sort={rss/swp/etc...)

--sort=rss- sorts rss one way

--sort=rss sorts rss the other way


LICENSED UNDER APACHE V2.0

#   Copyright 2013 Howard Grimberg and Aditya Balasubrmanian
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
