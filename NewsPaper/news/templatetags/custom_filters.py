from django import template


register = template.Library()

censor_list = ['пиво', 'водк']


@register.filter()
def censor(value):
   """
   value: значение, к которому нужно применить фильтр
   """
   text = value.split()
   for i, word in enumerate(text):
      for w in censor_list:
         if w in word:
            if '.' in word or ',' in word:
               text[i] = word[0] + '*' * (len(word) - 2) + word[-1]
            else:
               text[i] = word[0] + '*' * (len(word) - 1)

   # Возвращаемое функцией значение подставится в шаблон.
   return ' '.join(text)