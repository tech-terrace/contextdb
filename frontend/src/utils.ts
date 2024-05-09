export const copyToClipboard = async (url: string | null) => {
    try {
        await navigator.clipboard.writeText(url || '');
        alert('Link copied to clipboard!');
    } catch (error) {
        console.error('Failed to copy:', error);
    }
};

export const copyUrlContentToClipboard = async (url: string | null) => {
    try {
        const response = await fetch(url || '');
        const text = await response.text();
        await navigator.clipboard.writeText(text);
        alert('Content copied to clipboard!');
    } catch (error) {
        console.error('Failed to copy:', error);
    }
};

export const openInNewTab = (url: string | null) => {
    window.open(url || '', '_blank');
};

export const downloadFile = async (url: string | null) => {
    try {
        const response = await fetch(url || '');
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.setAttribute('download', url?.split('/').pop() || '');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
        console.error('Failed to download file:', error);
    }
};