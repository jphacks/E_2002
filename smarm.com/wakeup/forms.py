from django import forms
from .models import Schedule, SoundFile


class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule
        fields = ('summary', 'start_time')
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return end_time


class SimpleScheduleForm(forms.ModelForm):
    """シンプルなスケジュール登録用フォーム"""

    class Meta:
        model = Schedule
        fields = ('summary', 'start_time', 'date',)
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'date': forms.HiddenInput,
        }

class SoundFileForm(forms.ModelForm):
    class Meta:
        model = SoundFile
        fields = '__all__'
