from django import forms


class CreateThreadForm(forms.Form):
    title = forms.CharField(max_length=256)
    body = forms.CharField(widget=forms.Textarea)
    attachment = forms.FileField(required=False)


class CreateCommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)
    attachment = forms.FileField(required=False)
