from django.db import models
from django.utils import timezone


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-updated_at",)

class Document(TrackingModel):
    """
    -- Table: documents
    CREATE TABLE documents (
        id bigserial  NOT NULL,
        document_id varchar(200)  NOT NULL,
        document_name varchar(200)  NOT NULL,
        content text  NULL,
        creation_date timestamp  NULL,
        source smallint  NULL,
        document_type varchar(200)  NULL,
        created_at timestamp  NULL DEFAULT NOW(),
        updated_at timestamp  NULL DEFAULT NOW(),
        CONSTRAINT documents_ak_1 UNIQUE (document_id) NOT DEFERRABLE  INITIALLY IMMEDIATE,
        CONSTRAINT documents_id PRIMARY KEY (id)
    );
    """

    document_id = models.CharField(unique=True, max_length=200, blank=False)
    document_name = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=True)
    creation_date = models.DateTimeField(blank=True)
    source = models.IntegerField(blank=True)
    document_type = models.CharField(max_length=200, blank=True)
    updated_at_system = models.DateTimeField(default=timezone.now)

    class Meta:
        # set name cho table trong database
        db_table = "documents"


class DocumentFile(TrackingModel):
    """
    -- Table: document_files
    CREATE TABLE document_files (
        id bigserial  NOT NULL,
        file_url varchar(200)  NOT NULL,
        document_id varchar(200)  NOT NULL,
        created_at timestamp  NULL DEFAULT NOW(),
        updated_at timestamp  NULL DEFAULT NOW(),
        updated_at_system timestamptz  NOT NULL,
        CONSTRAINT document_files_id PRIMARY KEY (id)
    );
    """

    file_url = models.CharField(max_length=200, blank=False)
    document_id = models.ForeignKey(
        Document,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name="document_files",
        db_column="document_id",
        to_field="document_id",
    )
    updated_at_system = models.DateTimeField(default=timezone.now)

    class Meta:
        # set name cho table trong database
        db_table = "document_files"

