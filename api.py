import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contextdb.settings')
django.setup()
from fastapi import FastAPI, HTTPException, Query
from django.conf import settings
from pydantic import BaseModel, HttpUrl
from datetime import date
from core.models import Tag, Framework, Version, DocFile
from typing import List, Optional
from django.db.models import Prefetch


app = FastAPI()

class TagModel(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class FrameworkModel(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class DocFileModel(BaseModel):
    file_name: str
    file_url: HttpUrl
    token_count: Optional[int]

    class Config:
        from_attributes = True

class VariantModel(BaseModel):
    variant_type: str
    doc_files: List[DocFileModel]

    class Config:
        from_attributes = True

class VersionModel(BaseModel):
    version_number: str
    release_date: Optional[date]
    variants: List[VariantModel]

    class Config:
        from_attributes = True


@app.get("/tags/", response_model=List[TagModel])
def list_tags():
    tags = Tag.objects.all()
    return list(tags)


@app.get("/frameworks/", response_model=List[FrameworkModel])
def search_frameworks(name: str = None, tag_ids: List[int] = Query(None)):
    frameworks = Framework.objects.all()
    
    if name:
        frameworks = frameworks.filter(name__icontains=name)
    
    if tag_ids:
        frameworks = frameworks.filter(tags__id__in=tag_ids).distinct()
    
    return list(frameworks)


@app.get("/versions/{tool_id}/", response_model=List[VersionModel])
def get_versions_with_variants_and_docs(tool_id: int):
    try:
        framework = Framework.objects.get(id=tool_id)
    except Framework.DoesNotExist:
        raise HTTPException(status_code=404, detail="Framework not found")

    versions = Version.objects.filter(framework=framework).prefetch_related('variant_set__docfile_set').all()

    version_models = []
    for version in versions:
        variant_models = []
        for variant in version.variant_set.all():
            docfile_models = []
            for docfile in variant.docfile_set.all():
                docfile_model = DocFileModel(
                    file_name=docfile.file_name,
                    file_url=docfile.get_file_url(),
                    token_count=docfile.token_count
                )
                docfile_models.append(docfile_model)
            variant_model = VariantModel(
                variant_type=variant.get_variant_type_display(),
                doc_files=docfile_models
            )
            variant_models.append(variant_model)
        version_model = VersionModel(
            version_number=version.version_number,
            release_date=version.release_date,
            variants=variant_models
        )
        version_models.append(version_model)

    if not version_models:
        raise HTTPException(status_code=404, detail="No versions found for the given framework")

    return version_models

