#!/bin/bash

cd /home/luke/Plocha/Serverpanel/

/home/luke/Plocha/Serverpanel/Libraries/bin/hypercorn app:app --bind 127.0.0.1:1111 