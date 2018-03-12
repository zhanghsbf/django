from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

# 创建一个模型管理对象
class QuestionAdmin(admin.ModelAdmin):
	#fields = ['pub_date','question']
	fieldsets = [
		('I will ask', {'fields':['question']}),
		('Date information', {'fields':['pub_date'],
		'classes':['collapse']}),
	]
	inlines = [ChoiceInline]
	list_display = ('question','pub_date','was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question']

admin.site.register(Question,QuestionAdmin)


