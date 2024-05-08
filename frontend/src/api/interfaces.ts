export interface TagModel {
    id: number;
    name: string;
}

export interface FrameworkModel {
    id: number;
    name: string;
    description: string;
    latest_version: string | null;
    latest_doc_file_url: string | null;
    tags: TagModel[];
}

export interface DocFileModel {
    file_name: string;
    file_url: string;
    token_count: number | null;
}

export interface VariantModel {
    variant_type: string;
    doc_files: DocFileModel[];
}

export interface VersionModel {
    version_number: string;
    release_date: string | null;
    variants: VariantModel[];
}

export interface ValidationError {
    loc: (string | number)[];
    msg: string;
    type: string;
}

export interface HTTPValidationError {
    detail: ValidationError[];
}