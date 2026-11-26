from django import forms
from django.template.defaultfilters import filesizeformat


# https://stackoverflow.com/a/9016664
class RestrictedFileField(forms.FileField):
    def __init__(self, *args, content_types=None, max_upload_size=0, **kwargs):
        self.content_types = content_types or []
        self.max_upload_size = max_upload_size

        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        file = super().clean(*args, **kwargs)

        try:
            content_type = file.content_type
            print(content_type)
            if content_type in self.content_types:
                if file.size > self.max_upload_size:
                    raise forms.ValidationError(
                        f"File exceeds size limit. Max size: {filesizeformat(self.max_upload_size)}, file size: {filesizeformat(file.size)}."
                    )
            else:
                raise forms.ValidationError("Filetype not supported.")
        except AttributeError as e:
            print(e)
            pass

        return file
