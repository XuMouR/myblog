from faker import Faker
from blog.models import Article
fake = Faker('zh_CN')
# fake.name()




def add_fake_datas(request):
    print(fake.name())
    for i in range(1,1000000):
        Article.objects.create(title=fake.word(), desc=fake.sentence(), content=fake.texts(), user=request.user



print(123)


