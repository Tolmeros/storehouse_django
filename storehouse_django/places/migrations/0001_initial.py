# Generated by Django 2.2.2 on 2019-06-16 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Formfactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, default='', max_length=255)),
                ('humanid', models.IntegerField(unique=True)),
                ('outside_height', models.IntegerField(blank=True, null=True)),
                ('outside_width', models.IntegerField(blank=True, null=True)),
                ('outside_depth', models.IntegerField(blank=True, null=True)),
                ('inside_height', models.IntegerField(blank=True, null=True)),
                ('inside_width', models.IntegerField(blank=True, null=True)),
                ('inside_depth', models.IntegerField(blank=True, null=True)),
                ('empty_weight', models.IntegerField(blank=True, null=True)),
                ('contents_weight_max', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OpeningType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, default='', max_length=255)),
                ('humanid', models.CharField(max_length=1, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoragePlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, default='', max_length=255)),
                ('humanid', models.CharField(max_length=5)),
                ('formfactor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storage_places', to='places.Formfactor')),
                ('opening_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storage_places', to='places.OpeningType')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inside_places', to='places.StoragePlace')),
            ],
        ),
        migrations.AddConstraint(
            model_name='storageplace',
            constraint=models.UniqueConstraint(fields=('humanid', 'opening_type', 'formfactor'), name='full_humanid'),
        ),
    ]
