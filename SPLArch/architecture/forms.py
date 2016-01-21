from SPLArch.architecture.models import *
from django import forms


class ApiForm(forms.ModelForm):
    class Meta:
        model = API

    def clean(self):
        for field in self.cleaned_data:
            if isinstance(self.cleaned_data[field], basestring):
                self.cleaned_data[field] = self.cleaned_data[field].strip()
        return self.cleaned_data


class ReferencesForm(forms.ModelForm):
    class Meta:
        model = References

    def clean(self):
        for field in self.cleaned_data:
            if isinstance(self.cleaned_data[field], basestring):
                self.cleaned_data[field] = self.cleaned_data[field].strip()
        return self.cleaned_data


class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology

    def clean(self):
        for field in self.cleaned_data:
            if isinstance(self.cleaned_data[field], basestring):
                self.cleaned_data[field] = self.cleaned_data[field].strip()
        return self.cleaned_data


class UseCaseForm(forms.ModelForm):
    class Meta:
        model = UseCase

    def __init__(self, *args, **kwargs):
        super(UseCaseForm, self).__init__(*args, **kwargs)
        wtf = Requirement.objects.filter(
            requirement_type=RequirementType.objects.filter(name='Functional Requirements'));

        w = self.fields['f_requirements'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice.name))
        w.choices = choices

    def clean(self):
        for field in self.cleaned_data:
            if isinstance(self.cleaned_data[field], basestring):
                self.cleaned_data[field] = self.cleaned_data[field].strip()
        return self.cleaned_data


class ArchitectureForm(forms.ModelForm):
    class Meta:
        model = Architecture

    def clean(self):
        for field in self.cleaned_data:
            if isinstance(self.cleaned_data[field], basestring):
                self.cleaned_data[field] = self.cleaned_data[field].strip()
        return self.cleaned_data


class ScenariosForm(forms.ModelForm):
    class Meta:
        model = Scenarios

    def clean(self):
        for field in self.cleaned_data:
            if isinstance(self.cleaned_data[field], basestring):
                self.cleaned_data[field] = self.cleaned_data[field].strip()
        return self.cleaned_data


class DSSAForm(forms.ModelForm):
    class Meta:
        model = DDSA

    def clean(self):
        for field in self.cleaned_data:
            if isinstance(self.cleaned_data[field], basestring):
                self.cleaned_data[field] = self.cleaned_data[field].strip()
        return self.cleaned_data


class AddScenariosForm(forms.ModelForm):
    class Meta:
        model = AddScenarios

    def __init__(self, *args, **kwargs):
        super(AddScenariosForm, self).__init__(*args, **kwargs)
        wtf = Requirement.objects.filter(
            requirement_type=RequirementType.objects.filter(name='Non-functional requirement'));

        w = self.fields['nf_requirement'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice.name))
        w.choices = choices

    def clean(self):
        for field in self.cleaned_data:
            if isinstance(self.cleaned_data[field], basestring):
                self.cleaned_data[field] = self.cleaned_data[field].strip()
        return self.cleaned_data