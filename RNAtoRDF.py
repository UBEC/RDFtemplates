#!/usr/bin/python
import argparse
import settings
import os
import md5

import jinja2
from jinja2 import Template

env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.abspath('/Users/jdeligt/code/RDFtemplates/')))
#loader=FileSystemLoader('templates'))

parser = argparse.ArgumentParser(description='Render a RNA dataset in RDF.')
parser.add_argument('-i','--inputfile', help='RNA data input file',  required=True,  default='CGCflagship_RNAseq_PerGeneCounts_Normalised.txt' )
parser.add_argument('-t','--template',  help='Template file',        required=True,  default='RNAseq_Template.ttl')
args = vars(parser.parse_args())

#allthedata = { "CGC.W.CTR.T0.R1":{"ENSG00000000003":333.274970691942, "ENSG00000000419":664.23553186519}, "CGC.W.CTR.T6.R1":{"ENSG00000000003":329.100263826416, "ENSG00000000419":884.299945548844}}

def readrnadata(infile):
    data = {}
    with open(infile, 'r') as datafile:
        header = datafile.readline().strip().split("\t")
        for sample in header:
            data[sample] = {}

        for dataline in datafile:
            content = dataline.strip().split("\t")
            for i in range(1, len(content)) :
                data[header[i-1]][content[0]] = content[i]
    return(data)



def fairfy(data):
    for sid in data:
        newid = md5.new(sid).hexdigest()
        data[newid] = data[sid]
        del(data[sid])


template = env.get_template(args['template'])

allthedata = readrnadata(args['inputfile'])
fairfy(allthedata)

torender = {"settings":{"host":settings.host, "surl":"http://purl.org/fair/cgc/sample/"}, "rnadata":allthedata}

#print(template.render(torender))
with open("test_"+args['template'], "w") as f:
    f.write(template.render(torender))
