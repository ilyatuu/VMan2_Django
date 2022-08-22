# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actees(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    species = models.CharField(max_length=36, blank=True, null=True)
    parent = models.CharField(max_length=36, blank=True, null=True)
    purgedat = models.DateTimeField(db_column='purgedAt', blank=True, null=True)  # Field name made lowercase.
    purgedname = models.TextField(db_column='purgedName', blank=True, null=True)  # Field name made lowercase.
    details = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actees'


class Actors(models.Model):
    type = models.CharField(max_length=15, blank=True, null=True)
    acteeid = models.CharField(db_column='acteeId', max_length=36)  # Field name made lowercase.
    displayname = models.CharField(db_column='displayName', max_length=64)  # Field name made lowercase.
    meta = models.JSONField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    expiresat = models.DateTimeField(db_column='expiresAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'actors'


class Assignments(models.Model):
    actorid = models.OneToOneField(Actors, models.DO_NOTHING, db_column='actorId', primary_key=True)  # Field name made lowercase.
    roleid = models.ForeignKey('Roles', models.DO_NOTHING, db_column='roleId')  # Field name made lowercase.
    acteeid = models.CharField(db_column='acteeId', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'assignments'
        unique_together = (('actorid', 'roleid', 'acteeid'),)


class Audits(models.Model):
    actorid = models.ForeignKey(Actors, models.DO_NOTHING, db_column='actorId', blank=True, null=True)  # Field name made lowercase.
    action = models.TextField()
    acteeid = models.CharField(db_column='acteeId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    details = models.JSONField(blank=True, null=True)
    loggedat = models.DateTimeField(db_column='loggedAt', blank=True, null=True)  # Field name made lowercase.
    claimed = models.DateTimeField(blank=True, null=True)
    processed = models.DateTimeField(blank=True, null=True)
    lastfailure = models.DateTimeField(db_column='lastFailure', blank=True, null=True)  # Field name made lowercase.
    failures = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audits'


class Blobs(models.Model):
    sha = models.CharField(unique=True, max_length=40)
    content = models.BinaryField()
    contenttype = models.TextField(db_column='contentType', blank=True, null=True)  # Field name made lowercase.
    md5 = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'blobs'


class ClientAudits(models.Model):
    blobid = models.ForeignKey(Blobs, models.DO_NOTHING, db_column='blobId')  # Field name made lowercase.
    event = models.TextField(blank=True, null=True)
    node = models.TextField(blank=True, null=True)
    start = models.TextField(blank=True, null=True)
    end = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    accuracy = models.TextField(blank=True, null=True)
    old_value = models.TextField(db_column='old-value', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    new_value = models.TextField(db_column='new-value', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    remainder = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client_audits'


class Comments(models.Model):
    submissionid = models.ForeignKey('Submissions', models.DO_NOTHING, db_column='submissionId')  # Field name made lowercase.
    actorid = models.ForeignKey(Actors, models.DO_NOTHING, db_column='actorId')  # Field name made lowercase.
    body = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'comments'


class Config(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    value = models.JSONField(blank=True, null=True)
    setat = models.DateTimeField(db_column='setAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'config'


class FieldKeys(models.Model):
    actorid = models.OneToOneField(Actors, models.DO_NOTHING, db_column='actorId', related_name='actorid', primary_key=True)  # Field name made lowercase.
    createdby = models.ForeignKey(Actors, models.DO_NOTHING, db_column='createdBy', related_name='createdby',)  # Field name made lowercase.
    projectid = models.ForeignKey('Projects', models.DO_NOTHING, db_column='projectId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'field_keys'


class FormAttachments(models.Model):
    formid = models.ForeignKey('Forms', models.DO_NOTHING, db_column='formId')  # Field name made lowercase.
    blobid = models.ForeignKey(Blobs, models.DO_NOTHING, db_column='blobId', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField()
    type = models.TextField(blank=True, null=True)
    formdefid = models.OneToOneField('FormDefs', models.DO_NOTHING, db_column='formDefId', primary_key=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'form_attachments'
        unique_together = (('formdefid', 'name'),)


class FormDefs(models.Model):
    formid = models.ForeignKey('Forms', models.DO_NOTHING, db_column='formId', blank=True, null=True)  # Field name made lowercase.
    xml = models.TextField()
    hash = models.CharField(max_length=32)
    sha = models.CharField(max_length=40)
    sha256 = models.CharField(max_length=64)
    version = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    keyid = models.ForeignKey('Keys', models.DO_NOTHING, db_column='keyId', blank=True, null=True)  # Field name made lowercase.
    xlsblobid = models.ForeignKey(Blobs, models.DO_NOTHING, db_column='xlsBlobId', blank=True, null=True)  # Field name made lowercase.
    publishedat = models.DateTimeField(db_column='publishedAt', blank=True, null=True)  # Field name made lowercase.
    drafttoken = models.CharField(db_column='draftToken', max_length=64, blank=True, null=True)  # Field name made lowercase.
    enketoid = models.CharField(db_column='enketoId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_defs'


class FormFieldValues(models.Model):
    formid = models.ForeignKey('Forms', models.DO_NOTHING, db_column='formId')  # Field name made lowercase.
    submissiondefid = models.ForeignKey('SubmissionDefs', models.DO_NOTHING, db_column='submissionDefId')  # Field name made lowercase.
    path = models.TextField()
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_field_values'


class FormFields(models.Model):
    formid = models.ForeignKey('Forms', models.DO_NOTHING, db_column='formId')  # Field name made lowercase.
    formdefid = models.OneToOneField(FormDefs, models.DO_NOTHING, db_column='formDefId', primary_key=True)  # Field name made lowercase.
    path = models.TextField()
    name = models.TextField()
    type = models.CharField(max_length=32)
    binary = models.BooleanField(blank=True, null=True)
    order = models.IntegerField()
    selectmultiple = models.BooleanField(db_column='selectMultiple', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'form_fields'
        unique_together = (('formdefid', 'path'),)


class Forms(models.Model):
    xmlformid = models.CharField(db_column='xmlFormId', max_length=64)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    acteeid = models.CharField(db_column='acteeId', max_length=36)  # Field name made lowercase.
    state = models.TextField(blank=True, null=True)
    projectid = models.ForeignKey('Projects', models.DO_NOTHING, db_column='projectId')  # Field name made lowercase.
    currentdefid = models.ForeignKey(FormDefs, models.DO_NOTHING, db_column='currentDefId', related_name='currentdefid', blank=True, null=True)  # Field name made lowercase.
    draftdefid = models.ForeignKey(FormDefs, models.DO_NOTHING, db_column='draftDefId', related_name='draftdefid', blank=True, null=True)  # Field name made lowercase.
    enketoid = models.CharField(db_column='enketoId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enketoonceid = models.TextField(db_column='enketoOnceId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'forms'
        unique_together = (('projectid', 'xmlformid'),)


class Keys(models.Model):
    public = models.TextField(unique=True)
    private = models.JSONField(blank=True, null=True)
    managed = models.BooleanField(blank=True, null=True)
    hint = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'keys'


class KnexMigrations(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    batch = models.IntegerField(blank=True, null=True)
    migration_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'knex_migrations'


class KnexMigrationsLock(models.Model):
    index = models.AutoField(primary_key=True)
    is_locked = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'knex_migrations_lock'


class Projects(models.Model):
    name = models.TextField()
    acteeid = models.CharField(db_column='acteeId', unique=True, max_length=36)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    archived = models.BooleanField(blank=True, null=True)
    keyid = models.ForeignKey(Keys, models.DO_NOTHING, db_column='keyId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'projects'


class PublicLinks(models.Model):
    actorid = models.OneToOneField(Actors, models.DO_NOTHING, db_column='actorId', related_name='actorid', primary_key=True)  # Field name made lowercase.
    createdby = models.ForeignKey(Actors, models.DO_NOTHING, db_column='createdBy', related_name='createdby')  # Field name made lowercase.
    formid = models.ForeignKey(Forms, models.DO_NOTHING, db_column='formId')  # Field name made lowercase.
    once = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'public_links'


class Roles(models.Model):
    name = models.TextField()
    system = models.CharField(max_length=8, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    verbs = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Sessions(models.Model):
    actorid = models.ForeignKey(Actors, models.DO_NOTHING, db_column='actorId')  # Field name made lowercase.
    token = models.CharField(max_length=64)
    expiresat = models.DateTimeField(db_column='expiresAt')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    csrf = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions'


class SubmissionAttachments(models.Model):
    blobid = models.ForeignKey(Blobs, models.DO_NOTHING, db_column='blobId', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField()
    submissiondefid = models.OneToOneField('SubmissionDefs', models.DO_NOTHING, db_column='submissionDefId', primary_key=True)  # Field name made lowercase.
    index = models.IntegerField(blank=True, null=True)
    isclientaudit = models.BooleanField(db_column='isClientAudit', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'submission_attachments'
        unique_together = (('submissiondefid', 'name'),)


class SubmissionDefs(models.Model):
    submissionid = models.ForeignKey('Submissions', models.DO_NOTHING, db_column='submissionId')  # Field name made lowercase.
    xml = models.TextField()
    formdefid = models.ForeignKey(FormDefs, models.DO_NOTHING, db_column='formDefId')  # Field name made lowercase.
    submitterid = models.ForeignKey(Actors, models.DO_NOTHING, db_column='submitterId', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    encdataattachmentname = models.CharField(db_column='encDataAttachmentName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    localkey = models.TextField(db_column='localKey', blank=True, null=True)  # Field name made lowercase.
    signature = models.TextField(blank=True, null=True)
    current = models.BooleanField(blank=True, null=True)
    instancename = models.TextField(db_column='instanceName', blank=True, null=True)  # Field name made lowercase.
    instanceid = models.CharField(db_column='instanceId', max_length=64)  # Field name made lowercase.
    useragent = models.CharField(db_column='userAgent', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deviceid = models.CharField(db_column='deviceId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    root = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'submission_defs'


class Submissions(models.Model):
    formid = models.ForeignKey(Forms, models.DO_NOTHING, db_column='formId')  # Field name made lowercase.
    instanceid = models.CharField(db_column='instanceId', max_length=64)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    submitterid = models.ForeignKey(Actors, models.DO_NOTHING, db_column='submitterId', blank=True, null=True)  # Field name made lowercase.
    deviceid = models.CharField(db_column='deviceId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    draft = models.BooleanField()
    reviewstate = models.TextField(db_column='reviewState', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'submissions'
        unique_together = (('formid', 'instanceid', 'draft'),)
