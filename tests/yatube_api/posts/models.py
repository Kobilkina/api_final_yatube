from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts', verbose_name='Автор',)
    group = models.ForeignKey(
                Group,
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name='posts',
                verbose_name='Группа',
                help_text='Группа, к которой будет относиться пост')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик',)
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='following',
        verbose_name='Автор',)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'following'],
            name='unique user-following')]
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return self.name



#from email.headerregistry import Group
#from django.db import models
#from django.contrib.auth import get_user_model

#from .validators import validate_not_empty

#User = get_user_model()


#class Group(models.Model):
#    title = models.CharField(max_length=200)
#    slug = models.SlugField(unique=True)
#    description = models.TextField()

#    def __str__(self):
#        return self.title


#class Post(models.Model):
#    text = models.TextField('Текст поста', help_text='Введите текст поста',
#                            validators=[validate_not_empty])
#    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
#    author = models.ForeignKey(
#        User,
#        on_delete=models.CASCADE,
#        related_name='posts',
#        verbose_name='Автор',
#    )
#    group = models.ForeignKey(
#        Group,
#        blank=True,
#        null=True,
#        on_delete=models.SET_NULL,
#        related_name='posts',
#        verbose_name='Группа',
#        help_text='Группа, к которой будет относиться пост'
#    )
#    image = models.ImageField(
#        'Картинка',
#        upload_to='posts/',
#        blank=True
#    )
    # Аргумент upload_to указывает директорию,
    # в которую будут загружаться пользовательские файлы.

    # посты отсортированы по полю pub_date по убыванию
#    class Meta:
#        ordering = ['-pub_date']
#        verbose_name = 'Пост'
#        verbose_name_plural = 'Посты'

#    def __str__(self):
#        return self.text[:15]


#class Comment(models.Model):
#    post = models.ForeignKey(
#        Post, on_delete=models.CASCADE, related_name='comments')
#    author = models.ForeignKey(
#        User,
#        on_delete=models.CASCADE,
#        related_name='comments',
#        verbose_name='Автор',)
#    text = models.TextField(
#        'Текст комментария', help_text='Введите текст комментария',
#        validators=[validate_not_empty])
#    created = models.DateTimeField('Дата публикации', auto_now_add=True)


#class Follow(models.Model):
#    user = models.ForeignKey(
#        User,
#        on_delete=models.CASCADE,
#        related_name='follower',
#        verbose_name='Подписчик',)
#    author = models.ForeignKey(
#        User,
#        on_delete=models.CASCADE,
#        related_name='following',
#        verbose_name='Автор',)

#    class Meta:
#        constraints = [models.UniqueConstraint(
#            fields=['user', 'author'],
#            name='unique user-author')]
#        verbose_name = 'Подписчик'
#        verbose_name_plural = 'Подписчики'