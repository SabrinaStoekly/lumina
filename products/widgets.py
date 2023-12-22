from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _

class CustomClearableFileInput(ClearableFileInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear_checkbox_label = _('Remove')
        self.initial_text = _('Current Image')
        self.input_text = _('')
        self.template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'