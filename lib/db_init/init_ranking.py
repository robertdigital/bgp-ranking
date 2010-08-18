#!/usr/bin/python
# -*- coding: utf-8 -*-


import os 
import sys
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read("../../etc/bgp-ranking.conf")
root_dir = config.get('directories','root')
sys.path.append(os.path.join(root_dir,config.get('directories','libraries')))

from db_models.ranking import *
from sqlalchemy import Index

ranking_metadata.drop_all()
ranking_metadata.create_all()

# Creation of the "default AS", see fetch_asn.py for more informations 
ASNs(asn=unicode('-1'))

r_session = RankingSession()
r_session.execute("create index i_whois on IPsDescriptions (whois(50));")
r_session.execute("create index i_ipdesc_time_ans on IPsDescriptions (asn_id, timestamp);")
r_session.commit()
r_session.close()
