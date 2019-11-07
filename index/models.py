from django.db import models

# Create your models here.
class Topic(models.Model):
    topic_name = models.CharField(max_length=50, null=True, blank=True)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return str(self.topic_name)

class Article(models.Model):
    article_name = models.ForeignKey(Topic, null=True, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.article_name)


"""
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
"""