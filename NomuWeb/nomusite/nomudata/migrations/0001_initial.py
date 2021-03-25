# Generated by Django 3.1.7 on 2021-03-19 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientName', models.CharField(max_length=500)),
                ('revenueGrowth', models.FloatField(default=0.0)),
                ('profitGrowth', models.FloatField(default=0.0)),
                ('pbr', models.FloatField(default=0.0)),
                ('per', models.FloatField(default=0.0)),
                ('evtoEBITDA', models.FloatField(default=0.0)),
                ('dividenYield', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='NomuData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=500)),
                ('sym', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RecommendedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientName', models.CharField(max_length=500)),
                ('sector', models.CharField(max_length=200)),
                ('ticker', models.CharField(max_length=20)),
                ('report', models.CharField(max_length=900)),
                ('rating', models.CharField(max_length=10)),
                ('ticks', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='SimilarClientItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientName', models.CharField(max_length=500)),
                ('sector', models.CharField(max_length=500)),
                ('ticker', models.CharField(max_length=20)),
                ('report', models.CharField(max_length=900)),
                ('rating', models.CharField(max_length=10)),
                ('ticks', models.FloatField(default=0.0)),
            ],
        ),
    ]
