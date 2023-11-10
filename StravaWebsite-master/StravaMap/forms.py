from django import forms

from StravaMap.models import Col

class ColForm(forms.ModelForm):
    class Meta:
        model = Col
        fields = ["col_name", "col_code", "col_alt", "col_lat", "col_lon", "col_type" ]	