from flask import render_template, abort, flash, url_for, redirect, request
from flask.ext.login import login_required
from editor.app import app
from editor import models as m
from editor.models import db
from editor.models.document import Document
import datetime

# Forms

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, HiddenField


class DocumentForm(Form):
    # username = TextField('Username', [validators.Length(min=4, max=25)])
    name = TextField('Name')
    value = TextAreaField('Content')
    id = HiddenField('id')


# Views

@app.route('/')
@app.route('/document/list')
@login_required
def document_list():
    documents = m.get_document()
    return render_template('document/list.html', documents=documents)


@app.route('/document/edit/<id>')
@login_required
def document_edit(id):
    if id == 'new':
        document = Document()
    else:
        document = m.get_document_by_id(id)
    if not document:
        abort(404)
    document_form = DocumentForm(obj=document)

    return render_template('document/edit.html', document=document,
                           document_form=document_form)


@app.route('/document/store', methods=['POST'])
@login_required
def document_store():
    name = request.form['name']
    value = request.form['value']
    document_id = request.form['document_id']
    document = Document()
    if document_id:
        document = m.get_document_by_id(document_id)
    # maybe use lambda to assign key->values to object?
    document.name = name
    document.value = value
    document.save_date = datetime.datetime.now()
    # db stuff
    db.session.add(document)
    db.session.commit()
    flash('Document {0} stored, yo'.format(document_id))
    return redirect(url_for('document_list'))


@app.route('/document/delete/<id>', methods=['GET'])
@login_required
def document_delete(id):
    document = m.get_document_by_id(id)
    db.session.delete(document)
    db.session.commit()
    flash('Document {0} deleted!'.format(id))
    return redirect(url_for('document_list'))
