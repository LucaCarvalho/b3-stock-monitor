from django import forms
from .models import Tunnel
from .utils.ticker import get_ticker_data

class TunnelForm(forms.ModelForm):
    
    def validate_ticker(ticker: str) -> None:
        ticker_data = get_ticker_data(ticker)
        if ticker_data["bestMatches"] == [] or float(ticker_data["bestMatches"][0]['9. matchScore']) != 1.0:
            raise forms.ValidationError("Invalid ticker")

    def clean(self) -> dict:
        data = super().clean()
        lower = data.get("lower_bound")
        upper = data.get("upper_bound")
        
        if lower >= upper:
            raise forms.ValidationError("Upper bound must be greater than lower bound")

        return data

    ticker = forms.CharField(
        max_length=7,
        min_length=5,
        validators=[validate_ticker]
    )

    class Meta:
        model = Tunnel
        fields = ["ticker", "upper_bound", "lower_bound", "interval"]