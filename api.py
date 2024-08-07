import os
import django

from core.embed import get_embedding
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contextdb.settings')
django.setup()
from fastapi import APIRouter, FastAPI, HTTPException, Query
from django.conf import settings
from django.db.models import Q
from pydantic import BaseModel, HttpUrl
from packaging import version
from datetime import date
from core.models import Tag, Framework, Version, DocFile, Variant
from typing import List, Optional
from packaging.version import parse as parse_version


app = FastAPI(
    title="ContextDB API",
    description="API for ContextDB",
    version="0.1",
    servers=[{"url": "https://context-db.com/", "description": "Production"},
             {"url": "http://localhost:8001/", "description": "Local"}]
)
api_router = APIRouter(prefix="/api/v1")

class TagModel(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class FrameworkModel(BaseModel):
    id: int
    name: str
    description: str
    tags: List[TagModel]
    latest_version: Optional[str] = None
    latest_doc_file_url: Optional[HttpUrl] = None

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


class FrameworkDetailModel(BaseModel):
    name: str
    description: str
    versions: List[VersionModel]


@api_router.get("/tags/", response_model=List[TagModel])
def list_tags():
    tags = Tag.objects.all()
    return list(tags)


@api_router.get("/frameworks/", response_model=List[FrameworkModel])
def search_frameworks(name: str = None, tag_ids: List[int] = Query(None)):
    query = Q()

    if name:
        query &= Q(name__icontains=name)
    
    if tag_ids:
        query &= Q(tags__id__in=tag_ids)
    
    frameworks = Framework.objects.filter(query).prefetch_related(
        'tags', 
        'version_set__variant_set__docfile_set'
    )
    
    framework_models = []
    for framework in frameworks:
        versions = []
        for version in framework.version_set.order_by('-id').all():
            variants = []
            for variant in version.variant_set.all():
                doc_files = [
                    DocFileModel(
                        file_name=docfile.file_name,
                        file_url=docfile.get_file_url(),
                        token_count=docfile.token_count
                    ) for docfile in variant.docfile_set.all()
                ]
                variants.append(VariantModel(
                    variant_type=variant.get_variant_type_display(),
                    doc_files=doc_files
                ))
            versions.append(VersionModel(
                version_number=version.version_number,
                release_date=version.release_date,
                variants=variants
            ))
        
        # Sort versions by version number in descending order
        versions.sort(key=lambda x: parse_version(x.version_number), reverse=True)
        
        tag_models = [TagModel(id=tag.id, name=tag.name) for tag in framework.tags.all()]
        
        framework_model = FrameworkModel(
            id=framework.id,
            name=framework.name,
            description=framework.description,
            tags=tag_models,
            latest_version=versions[0].version_number if versions else None,
            latest_doc_file_url=versions[0].variants[0].doc_files[0].file_url if versions and versions[0].variants and versions[0].variants[0].doc_files else None
        )
        framework_models.append(framework_model)
    
    return framework_models

@api_router.get("/versions/{tool_id}/", response_model=FrameworkDetailModel)
def get_versions_with_variants_and_docs(tool_id: int):
    try:
        framework = Framework.objects.get(id=tool_id)
    except Framework.DoesNotExist:
        raise HTTPException(status_code=404, detail="Framework not found")

    versions = Version.objects.filter(framework=framework).prefetch_related('variant_set__docfile_set')

    version_models = []
    for version_obj in versions:
        variant_models = []
        for variant in version_obj.variant_set.all():
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
            version_number=version_obj.version_number,
            release_date=version_obj.release_date,
            variants=variant_models
        )
        version_models.append(version_model)

    # Sort versions by version number in descending order
    version_models.sort(key=lambda x: version.parse(x.version_number), reverse=True)

    if not version_models:
        raise HTTPException(status_code=404, detail="No versions found for the given framework")

    return FrameworkDetailModel(
        name=framework.name,
        description=framework.description,
        versions=version_models
    )


@api_router.get('/embeddings/')
def get_embeddings(url: str, query: str, num_of_results: int = 10) -> list[str]:
    res = get_embedding(url, query, num_of_results)
    return res


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)