# Generated by Django 2.2.6 on 2019-10-19 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalLectureContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernum', models.PositiveIntegerField(default=0)),
                ('at_beginning', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('text', models.TextField(max_length=2000)),
                ('format', models.CharField(choices=[('md', 'md'), ('html', 'html')], default='md', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('version', models.CharField(max_length=15)),
                ('additional_lecture_content', models.ManyToManyField(to='teach.AdditionalLectureContent')),
                ('content_types_selected', models.ManyToManyField(blank=True, to='teach.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('titleslide', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('layout', models.TextField(default='[\n  {}\n]')),
                ('hastitle', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('text', models.TextField()),
                ('restriction_kind', models.CharField(choices=[('none', 'none'), ('choice', 'choice'), ('number_of_choices', 'number_of_choices'), ('number', 'number')], default='none', max_length=25)),
                ('restriction_detail', models.TextField(blank=True, null=True)),
                ('eval_kind', models.CharField(choices=[('manual', 'manual'), ('accuracy', 'accuracy'), ('pct_off', 'pct_off')], default='manual', max_length=25)),
                ('eval_detail', models.TextField(blank=True, null=True)),
                ('eval_transform', models.TextField(blank=True, null=True)),
                ('explanation', models.TextField(blank=True, null=True)),
                ('imagelink', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('num_sample', models.PositiveIntegerField(default=0)),
                ('instant_answer', models.BooleanField(default=False)),
                ('tasks', models.ManyToManyField(blank=True, to='teach.Task')),
            ],
        ),
        migrations.CreateModel(
            name='UserSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starttime', models.BigIntegerField()),
                ('endtime', models.BigIntegerField(blank=True, null=True)),
                ('submitted', models.BooleanField(blank=True, default=False)),
                ('tasklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach.TaskList')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('related_contents', models.ManyToManyField(blank=True, to='teach.Content')),
            ],
        ),
        migrations.CreateModel(
            name='TaskAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('needs_human', models.BooleanField(blank=True, default=False)),
                ('answertext', models.TextField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach.UserSubmission')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='answer',
            field=models.ManyToManyField(through='teach.TaskAnswer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SlideStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernum', models.PositiveIntegerField()),
                ('css_style', models.CharField(blank=True, default='', max_length=100)),
                ('animate', models.BooleanField(default=True)),
                ('print_title', models.BooleanField(default=False)),
                ('fragment_no', models.SmallIntegerField(default=0)),
                ('upto_level', models.SmallIntegerField(default=0)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach.Content')),
                ('slide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach.Slide')),
            ],
        ),
        migrations.AddField(
            model_name='slide',
            name='contents',
            field=models.ManyToManyField(through='teach.SlideStructure', to='teach.Content'),
        ),
        migrations.CreateModel(
            name='LectureStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernum', models.FloatField()),
                ('multislide', models.BooleanField(default=False)),
                ('subordernum', models.PositiveIntegerField(default=0)),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach.Lecture')),
                ('slide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach.Slide')),
            ],
        ),
        migrations.AddField(
            model_name='lecture',
            name='slides',
            field=models.ManyToManyField(through='teach.LectureStructure', to='teach.Slide'),
        ),
        migrations.CreateModel(
            name='CourseStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernum', models.PositiveIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach.Course')),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach.Lecture')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='lectures',
            field=models.ManyToManyField(through='teach.CourseStructure', to='teach.Lecture'),
        ),
        migrations.AddField(
            model_name='course',
            name='tasklists',
            field=models.ManyToManyField(blank=True, to='teach.TaskList'),
        ),
        migrations.AddField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teach.ContentType'),
        ),
        migrations.AddField(
            model_name='additionallecturecontent',
            name='content',
            field=models.ManyToManyField(to='teach.Content'),
        ),
        migrations.AddField(
            model_name='additionallecturecontent',
            name='course',
            field=models.ManyToManyField(to='teach.Course'),
        ),
        migrations.AddField(
            model_name='additionallecturecontent',
            name='lecture',
            field=models.ManyToManyField(to='teach.Lecture'),
        ),
    ]
