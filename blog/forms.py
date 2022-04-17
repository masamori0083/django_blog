from django import forms


class DiarySearchForm(forms.Form):
    """
    検索フォーム
    """
    key_word = forms.CharField(
        label="検索キーワード",
        required=False
    )
