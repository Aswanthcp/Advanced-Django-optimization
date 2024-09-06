# Generated by Django 5.1.1 on 2024-09-06 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('publication_date', models.DateField()),
            ],
            options={
                'indexes': [models.Index(fields=['author', 'publication_date'], name='app_book_author_9ea7c4_idx')],
            },
        ),
    ]
