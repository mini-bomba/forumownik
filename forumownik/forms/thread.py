from django import forms

from ..utils import RestrictedFileField


class CreateThreadForm(forms.Form):
    title = forms.CharField(max_length=256)
    body = forms.CharField(widget=forms.Textarea)
    attachment = RestrictedFileField(
        required=False,
        max_upload_size=5_000_000,
        content_types=["image/gif", "image/jpeg", "image/png", "image/svg+xml", "image/tiff", "image/webp"],
    )


class CreateCommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)
    attachment = RestrictedFileField(
        required=False,
        max_upload_size=5_000_000,
        content_types=["image/gif", "image/jpeg", "image/png", "image/svg+xml", "image/tiff", "image/webp"],
    )
