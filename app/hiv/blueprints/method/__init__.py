# vim: fdm=indent
'''
author:     Fabio Zanini
date:       11/06/15
content:    Blueprint for the methods page.
'''
from re import split as resplit
from flask import Blueprint, render_template
from flask import (render_template, flash, redirect, request, jsonify,
                   make_response, abort)
from .forms import (LocalHaplotypeForm, TreeForm, ConsensiForm, RegionFragForm,
                    PatSingleForm, PatFragSingleForm, PrecompiledHaplotypeForm)
from .config import sections
from ... import hiv



method = Blueprint('method', __name__,
                    url_prefix='/method',
                    static_folder='static',
                    template_folder='templates')
hiv.config['BLUEPRINTS']['METHOD'] = {'SECTIONS': sections}


@method.route('/')
def index():
    return render_template('index.html',
                           title='Methods',
                           section_name='Method')


@method.route('/singleNucleotidePolymorphisms/', methods=['GET', 'POST'])
def allele_frequencies():
    if request.json:
        from ...models import AlleleFrequencyTrajectoryModel
        pname = request.json['patient']
        data = {'data': AlleleFrequencyTrajectoryModel(pname).get_data()}
        return jsonify(**data)


    form = PatSingleForm()
    if request.method == 'GET':
        show_intro = True
        pname = 'p1'
    else:
        show_intro = False
        pname = form.patient.data
        if not form.validate_on_submit():
            flash('Select at least one patient!')

    data = {'pname': pname,
            'name': pname,
            'id': pname}

    return render_template('allele_frequencies.html',
                           title='Single nucleotide polymorphisms',
                           section_name='Single nucleotide polymorphisms',
                           data=data,
                           form=form,
                           show_intro=show_intro,
                          )


@method.route('/coverage/', methods=['GET', 'POST'])
def coverage():
    if request.json:
        from ...models import CoverageTrajectoryModel
        pname = request.json['patient']
        data = {'data': CoverageTrajectoryModel(pname).get_data()}
        return jsonify(**data)

    form = PatSingleForm()
    if request.method == 'GET':
        show_intro = True
        pname = 'p1'
    else:
        show_intro = False
        pname = form.patient.data
        if not form.validate_on_submit():
            flash('Select at least one patient!')

    data = {'pname': pname,
            'name': pname,
            'id': pname}

    return render_template('coverage.html',
                           title='Coverage',
                           section_name='Coverage',
                           data=data,
                           form=form,
                           show_intro=show_intro,
                          )


@method.route('/physiological/', methods=['GET'])
def physio():
    return render_template('physio.html',
                           title='Viral load and CD4+ counts',
                           section_name='Viral load and CD4+ counts',
                          )



@method.route('/trees/', methods=['GET'])
def trees():
    return render_template('trees.html',
                           title='Phylogenetic trees',
                           section_name='Phylogenetic trees',
                          )


@method.route('/divdiv/', methods=['GET', 'POST'])
def divdiv():
    if request.json:
        from ...models import DivdivModel
        req = request.json
        pname = request.json['patient']
        region = request.json['region']
        data = {'data': DivdivModel(pname, region).get_data()}
        return jsonify(**data)

    form = RegionFragForm()
    if request.method == 'GET':
        show_intro = True
        pname = 'p1'
        region = 'F1'
    else:
        show_intro = False
        pname = form.patient.data
        region = form.region.data
        if not form.validate_on_submit():
            flash('Select a region and a patient!')

    data = {'pname': pname,
            'region': region,
            'name': pname+', '+region,
            'id': pname+'_'+region}

    return render_template('divdiv.html',
                           title='Divergence and diversity',
                           section_name='Divergence and diversity',
                           data=data,
                           form=form,
                           show_intro=show_intro,
                          )


@method.route('/genomes/', methods=['GET', 'POST'])
def genomes():
    if request.json:
        from ...models import GenomeModel
        pname = request.json['patient']
        data = {'data': GenomeModel(pname).get_data()}
        return jsonify(**data)

    form = PatSingleForm()
    if request.method == 'GET':
        show_intro = True
        pname = 'p1'
    else:
        show_intro = False
        pname = form.patient.data
        if not form.validate_on_submit():
            flash('Select a patient!')

    data = {'pname': pname,
            'name': pname,
            'id': pname}

    return render_template('genome.html',
                           title='Genome sequences',
                           section_name='Genome sequences',
                           data=data,
                           form=form,
                           show_intro=show_intro,
                          )


@method.route('/consensi/', methods=['GET', 'POST'])
def consensi():
    form = ConsensiForm()

    if request.method == 'GET':
        show_intro = True
        return render_template('consensi.html',
                       title='Consensus sequences',
                       section_name='Consensus sequences',
                       form=form,
                       show_intro=show_intro,
                      )


    if not form.validate_on_submit():
        show_intro = False
        flash('Select one region and one patient!')
        return render_template('consensi.html',
                       title='Consensus sequences',
                       section_name='Consensus sequences',
                       form=form,
                       show_intro=show_intro,
                      )

    pname = form.patient.data
    region = form.region.data
    return redirect('/download/consensi/'+pname+'_'+region+'.fasta')


@method.route('/divdivLocal/', methods=['GET', 'POST'])
def divdiv_local():
    if request.json:
        from ...models import DivdivLocalModel

        req = request.json
        pname = req['patient']
        kwargs = {}
        for key in ('observables', 'itimes', 'roi'):
            if key in req:
                kwargs[key] = req[key]

        data = {'data': DivdivLocalModel(pname, **kwargs).get_data()}
        return jsonify(**data)

    form = PatSingleForm()
    if request.method == 'GET':
        show_intro = True
        pname = 'p1'
    else:
        show_intro = False
        pname = form.patient.data
        if not form.validate_on_submit():
            flash('Select at least one patient!')

    data = {'pname': pname,
            'name': pname,
            'id': pname}

    return render_template('divdiv_local.html',
                           title='Local divergence and diversity',
                           section_name='Local divergence and diversity',
                           data=data,
                           form=form,
                           show_intro=show_intro,
                          )


@method.route('/haplotypes/', methods=['GET', 'POST'])
def haplotypes():

    form = LocalHaplotypeForm()
    formpc = PrecompiledHaplotypeForm()

    if request.method == 'GET':
        show_intro = True
        return render_template('haplotypes.html',
                               title='Haplotypes',
                               section_name='Haplotypes',
                               show_intro=show_intro,
                               form=form,
                               formpc=formpc,
                              )

    show_intro = False
    if (not formpc.validate_on_submit()) and (not form.validate_on_submit()):
        flash('Form incorrectly filled!')

        return render_template('haplotypes.html',
                               title='Haplotypes',
                               section_name='Haplotypes',
                               show_intro=show_intro,
                               form=form,
                               formpc=formpc,
                              )

    if formpc.validate_on_submit():
        pname = formpc.patient.data
        region = formpc.region.data
        return redirect('/download/haplotypes/'+pname+'/'+region+'.fasta')

    elif form.validate_on_submit():
        from ...models import LocalHaplotypeModel

        # NOTE: we offer only genomewide HXB2 coordinates
        region = 'genomewide'
        pname = form.patient.data
        start = form.roi.start.data - 1 #Inclusive coordinates
        end = form.roi.end.data
        roi = (region, start, end)

        hm = LocalHaplotypeModel(pname, roi)
        try:
            hm.translate_coordinates()
        except ValueError:
            flash('No PCR fragment covers such region, please select a narrower region')

            return render_template('haplotypes.html',
                                   title='Haplotypes',
                                   section_name='Haplotypes',
                                   show_intro=show_intro,
                                   form=form,
                                   formpc=formpc,
                                  )


        # Get the data from a temporary folder + file
        # NOTE: the temp folders are cleaned regularly at a timeout specified
        # in the config file, so no need to to that here.
        fn = hm.get_data()

        # TODO: refine this to show a success page with a download link etc. (that
        # changes the policies on temporary files, storage use, etc., so watch out)
        with open(fn, 'r') as f:
            fstr = f.read()
        response = make_response(fstr)
        response.headers["Content-Disposition"] = ("attachment; filename="+
                                                   "haplotypes_"+pname+
                                                   "_"+str(start+1)+
                                                   "_"+str(end)+
                                                   ".zip")
        return response


@method.route('/nTemplates/', methods=['POST'])
def n_templates():
    if request.json:
        from ...models import NTemplatesModel
        pname = request.json['patient']
        data = {'data': NTemplatesModel(pname).get_data()}
        return jsonify(**data)

    else:
        abort(403)
