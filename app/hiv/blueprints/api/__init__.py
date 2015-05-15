from flask import Blueprint
from flask_restful import Api, Resource


api_bp = Blueprint('api', __name__,
                   url_prefix='/api',
                   template_folder='templates')

api = Api(api_bp)


# Resources
from .resources import *

# Data
api.add_resource(Tree, '/data/tree/<pname>/<region>')
api.add_resource(Physiological, '/data/physiological/<pname>')
api.add_resource(NTemplates, '/data/numberTemplates/<pname>')
api.add_resource(ReferenceSequence, '/data/referenceSequence/<pname>/<region>')
api.add_resource(Coverage, '/data/coverage/<pname>')
# FIXME: this should be way more flexible (only polymorphic sites are returned now)
api.add_resource(AlleleFrequency, '/data/singleNucleotideVariants/<pname>')
api.add_resource(Haplotypes, '/data/haplotypes/<pname>/<region>')

# JS for plots
# FIXME: this becomes a CDN for embedding plots into other people's websites. Do we want this?