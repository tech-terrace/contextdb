import type { TagModel, FrameworkModel, VersionModel } from './interfaces';


const baseUrl = '/api/v1';

export const listTags = async (): Promise<TagModel[]> => {
    const response = await fetch(`${baseUrl}/tags/`);
    if (!response.ok) {
        throw new Error('Failed to fetch tags');
    }
    return response.json();
};

export const searchFrameworks = async (name?: string, tagIds?: number[]): Promise<FrameworkModel[]> => {
    const params = new URLSearchParams();
    if (name) params.append('name', name);
    if (tagIds) params.append('tag_ids', JSON.stringify(tagIds));

    const response = await fetch(`${baseUrl}/frameworks/?${params.toString()}`);
    if (!response.ok) {
        throw new Error('Failed to fetch frameworks');
    }
    return response.json();
};

export const getVersionsWithVariantsAndDocs = async (toolId: number): Promise<VersionModel[]> => {
    const response = await fetch(`${baseUrl}/versions/${toolId}/`);
    if (!response.ok) {
        throw new Error('Failed to fetch versions');
    }
    return response.json();
};