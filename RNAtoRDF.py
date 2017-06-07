#!/usr/bin/python
import argparse
import settings
import os
import md5

import jinja2
from jinja2 import Template

env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.abspath('.')))
#loader=FileSystemLoader('templates'))

parser = argparse.ArgumentParser(description='Render a RNA dataset in RDF.')
parser.add_argument('-i','--inputfile', help='RNA data input file',  required=True,  default='CGCflagship_RNAseq_PerGeneCounts_Normalised.txt' )
parser.add_argument('-t','--template',  help='Template file',        required=True,  default='RNAseq_Template.ttl')
args = vars(parser.parse_args())

allthedata = { "CGC.W.CTR.T0.R1":{"ENSG00000000003":333.274970691942, "ENSG00000000419":664.23553186519}, "CGC.W.CTR.T6.R1":{"ENSG00000000003":329.100263826416, "ENSG00000000419":884.299945548844}}
def fairfy(data):
    for sid in data:
        newid = "http://purl.org/fair/cgc/sample/"+md5.new(sid).hexdigest()
        data[newid] = data[sid]
        del(data[sid])


template = env.get_template(args['template'])

fairfy(allthedata)

torender = {"settings":{"host":settings.host}, "rnadata":allthedata}

#print(template.render(torender))
with open("test_"+args['template'], "w") as f:  
    f.write(template.render(torender))
