# courses/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CourseReview

class CourseReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        label=_('امتیاز'),
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'rating-input'})
    )
    
    comment = forms.CharField(
        label=_('نظر شما'),
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': _('نظر خود را درباره این دوره بنویسید...')
        })
    )
    
    class Meta:
        model = CourseReview
        fields = ['rating', 'comment']