from django import forms


class APIForm(forms.Form):
    def api_method(self, *args, **kwargs):
        raise NotImplementedError()

    def save(self, *args, **kwargs):
        if not self.is_valid():
            return {
                'status': 'error',
                'data': self.errors
            }

        return {
            'status': 'success',
            'data': self.api_method(*args, **kwargs)
        }
