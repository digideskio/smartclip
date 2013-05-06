from haystack import indexes

from .models import Clipping


class ClippingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    html = indexes.CharField(model_attr='html')
    title = indexes.CharField(model_attr='title')
    source_url = indexes.CharField(model_attr='source_url')
    created = indexes.DateTimeField(model_attr='date_created')
    user_id = indexes.CharField(model_attr='user_id')

    def get_model(self):
        return Clipping

