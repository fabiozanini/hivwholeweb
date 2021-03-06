# vim: fdm=indent
'''
author:     Fabio Zanini
date:       11/06/15
content:    Blueprint for the data page.
'''
# Modules
from flask import (Blueprint, render_template, abort, flash,
                   redirect, request, jsonify, make_response)



# Blueprint
data = Blueprint('data', __name__,
                 url_prefix='/data',
                 static_folder='static',
                 template_folder='templates')



# Views
@data.route('/', methods=['GET', 'POST'])
def index():
    # Haplotype forms
    from ..method.forms import LocalHaplotypeForm, PrecompiledHaplotypeForm
    from ...models import LocalHaplotypeModel
    form = LocalHaplotypeForm()
    formpc = PrecompiledHaplotypeForm()

    if request.method == 'POST':
        if ((not formpc.validate_on_submit()) and
            (not form.validate_on_submit())):
            flash('Haplotype form incorrectly filled!')

        elif formpc.validate_on_submit():
            pname = formpc.patient.data
            region = formpc.region.data
            return redirect('/download/haplotypes_'+pname+'_'+region+'.fasta')

        elif form.validate_on_submit():
            # NOTE: we offer only genomewide HXB2 coordinates
            region = 'genomewide'
            pname = form.patient.data
            start = form.roi.start.data - 1 #Inclusive coordinates
            end = form.roi.end.data
            roi = (region, start, end)

            hm = LocalHaplotypeModel(pname, roi)
            try:
                hm.translate_coordinates()
                cont = True
            except ValueError:
                flash('No PCR fragment covers such region, please select another region')
                cont = False

            if cont:
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
                                                           ".fasta")
                return response


    # SEQUENCING READS
    # NOTE: we are using the proxy view for static downloads as a screen
    # to the real locations on the server. A nice side effect is that we need
    # not instantiate data models within this view.
    # That factory is quite poorly written though, and would need some love.
    from ...models import PatientTableModel, ReadsTableModel
    data = []
    table = PatientTableModel().get_table()
    d = lambda x: '/download/'+x
    for row in table:
        pname = row['Patient']
        n_samples = row['# samples']

        reads = ReadsTableModel(pname)
        reads_table = reads.get_table()

        data.append({'pname': pname,
                     'nsamples': n_samples,
                     'vl': d('viralLoad_'+pname+'.tsv'),
                     'cd4': d('cellCount_'+pname+'.tsv'),
                     'hla': d('HLA_'+pname+'.tsv'),
                     'refgb': d('genome_'+pname+'.gb'),
                     'reffa': d('genome_'+pname+'.fasta'),
                     'act': d('act_'+pname+'.zip'),
                     'depth': d('depth_'+pname+'.tsv'),
                     'reads': reads_table,
                    })

    return render_template('data.html',
                           data=data,
                           form=form,
                           formpc=formpc,
                           fragments=['F'+str(i) for i in xrange(1, 7)],
                           title='Downloads',
                          )
