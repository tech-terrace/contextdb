from django.db import models
from django.core.files import File
import tiktoken
from storages.backends.gcloud import GoogleCloudStorage

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Framework(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Version(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    version_number = models.CharField(max_length=20)
    release_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('framework', 'version_number')

    def __str__(self):
        return f"{self.framework.name} - {self.version_number}"


class Variant(models.Model):
    VARIANT_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    variant_type = models.CharField(max_length=1, choices=VARIANT_CHOICES)

    class Meta:
        unique_together = ('version', 'variant_type')

    def __str__(self):
        return f"{self.version} - {self.get_variant_type_display()}"


class DocFile(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=250)
    file = models.FileField(storage=GoogleCloudStorage(), upload_to='docfiles/')
    token_count = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name
    
    def delete(self, *args, **kwargs):
        # Delete the file from Google Cloud Storage
        self.file.delete(save=False)
        # Call the superclass method to delete the instance from the database
        super(DocFile, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Check if the object already exists and has a file
        if self.pk:
            old_file = DocFile.objects.get(pk=self.pk).file
            # If the file has changed and the old file exists
            if old_file and self.file != old_file:
                old_file.delete(save=False)
        if self.file:
            file_content = self.file.read()
            file_content = file_content.decode('utf-8')
            # Get encoding for a model, e.g., 'gpt-4'
            encoding = tiktoken.encoding_for_model('gpt-4')
            # Count tokens
            self.token_count = len(encoding.encode(file_content))
            # Reset the file's pointer to the beginning
            self.file.seek(0)
        super(DocFile, self).save(*args, **kwargs)

    def get_file_url(self):
        if self.file:
            return self.file.url.split('?')[0]
        return None


def add_docfile(framework_name, version_number, variant_type, file_name, file):
    framework = Framework.objects.get(name=framework_name)
    version, created = Version.objects.get_or_create(framework=framework, version_number=version_number)
    variant, created = Variant.objects.get_or_create(version=version, variant_type=variant_type)
    try:
        existing_file = DocFile.objects.get(file_name=file_name, variant=variant)
        existing_file.file.delete(save=False)
        existing_file.delete()
    except DocFile.DoesNotExist:
        pass
    # Wrap the standard file object with Django's File class
    django_file = File(file, name=file_name)
    DocFile.objects.create(variant=variant, file_name=file_name, file=django_file)


def version_exists(framework_name, version_number):
    """
    Checks if the version of a given framework already exists.

    Args:
        framework_name: The name of the framework.
        version_number: The version number to check for.

    Returns:
        True if the version exists, False otherwise.
    """
    framework = Framework.objects.get(name=framework_name)
    try:
        Version.objects.get(framework=framework, version_number=version_number)
        return True
    except Version.DoesNotExist:
        return False