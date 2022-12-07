# Generated by Django 4.1.4 on 2022-12-06 22:38

import appManageWSSP.datavalidation
import appManageWSSP.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appManageWSSP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_es', models.CharField(max_length=100, unique=True)),
                ('name_en', models.CharField(max_length=100, unique=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_countries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'db_table': 'Country',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_es', models.CharField(max_length=250, unique=True)),
                ('title_en', models.CharField(max_length=250, unique=True)),
                ('show_title', models.BooleanField(default=True)),
                ('display_order', models.PositiveSmallIntegerField(default=1)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Element',
                'verbose_name_plural': 'Elements',
                'db_table': 'Element',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='MediaResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mediaType', models.CharField(choices=[('images', 'Image'), ('videos', 'Video')], default='images', max_length=6)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_mediaResources', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'MediaResource',
                'verbose_name_plural': 'MediaResources',
                'db_table': 'MediaResource',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_es', models.CharField(max_length=50, unique=True)),
                ('title_en', models.CharField(max_length=50, unique=True)),
                ('styleSheetName', models.CharField(max_length=50, unique=True)),
                ('url_title_es', models.CharField(max_length=50, unique=True)),
                ('url_title_en', models.CharField(max_length=50, unique=True)),
                ('display_order', models.PositiveSmallIntegerField(default=1)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_pages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'db_table': 'Page',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DescriptiveArticle',
            fields=[
                ('element_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appManageWSSP.element')),
                ('description_es', models.TextField(blank=True)),
                ('description_en', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'DescriptiveArticle',
                'verbose_name_plural': 'DescriptiveArticles',
                'db_table': 'DescriptiveArticle',
                'ordering': ['id'],
            },
            bases=('appManageWSSP.element',),
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('mediaresource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appManageWSSP.mediaresource')),
                ('file_image', models.FileField(unique=True, upload_to=appManageWSSP.models.custom_media_path, validators=[appManageWSSP.datavalidation.valid_image_extension, appManageWSSP.datavalidation.valid_image_file_size, appManageWSSP.datavalidation.valid_file_name])),
            ],
            options={
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imagenes',
                'db_table': 'Imagen',
                'ordering': ['id'],
            },
            bases=('appManageWSSP.mediaresource',),
        ),
        migrations.CreateModel(
            name='Outstanding',
            fields=[
                ('element_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appManageWSSP.element')),
            ],
            options={
                'verbose_name': 'Outstanding',
                'verbose_name_plural': 'Outstandings',
                'db_table': 'Outstanding',
                'ordering': ['id'],
            },
            bases=('appManageWSSP.element',),
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('element_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appManageWSSP.element')),
                ('size', models.CharField(choices=[('fullscreen', 'Full Screen'), ('dinamic', 'Dinamic')], default='fullscreen', max_length=20)),
                ('transitionType', models.CharField(choices=[('interactive', 'Interactive'), ('automatic', 'Automatic')], default='interactive', max_length=20)),
                ('display_sliderList', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Slider',
                'verbose_name_plural': 'Sliders',
                'db_table': 'Slider',
                'ordering': ['id'],
            },
            bases=('appManageWSSP.element',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('mediaresource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appManageWSSP.mediaresource')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('source', models.CharField(choices=[('server', 'Server'), ('web', 'Web')], default='server', max_length=10)),
                ('web_url', models.URLField(blank=True, null=True)),
                ('file_video', models.FileField(blank=True, null=True, upload_to=appManageWSSP.models.custom_media_path, validators=[appManageWSSP.datavalidation.valid_video_extension, appManageWSSP.datavalidation.valid_video_file_size, appManageWSSP.datavalidation.valid_file_name])),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
                'db_table': 'Video',
                'ordering': ['id'],
            },
            bases=('appManageWSSP.mediaresource',),
        ),
        migrations.CreateModel(
            name='StyleSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('content', models.TextField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_styleSheets', to='appManageWSSP.page')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_styleSheets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'StyleSheet',
                'verbose_name_plural': 'StyleSheets',
                'db_table': 'StyleSheet',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_es', models.CharField(max_length=250, unique=True)),
                ('title_en', models.CharField(max_length=250, unique=True)),
                ('show_title', models.BooleanField(default=True)),
                ('display_order', models.PositiveSmallIntegerField(default=1)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('media', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mediaResource_sections', to='appManageWSSP.mediaresource')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_sections', to='appManageWSSP.page')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
                'db_table': 'Section',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('scope', models.PositiveIntegerField(default=0)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country_regions', to='appManageWSSP.country')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_regions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
                'db_table': 'Region',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_provinces', to='appManageWSSP.region')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_provinces', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Province',
                'verbose_name_plural': 'Provinces',
                'db_table': 'Province',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='HtmlDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_html', models.FileField(unique=True, upload_to='html', validators=[appManageWSSP.datavalidation.valid_html_extension, appManageWSSP.datavalidation.valid_html_file_size, appManageWSSP.datavalidation.valid_file_name])),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_htmlDesigns', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'HtmlDesign',
                'verbose_name_plural': 'HtmlDesign',
                'db_table': 'HtmlDesign',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ElementType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('htmlName', models.CharField(max_length=100, unique=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_elementTypes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ElementType',
                'verbose_name_plural': 'ElementTypes',
                'db_table': 'ElementType',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='element',
            name='elementType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elemenType_elements', to='appManageWSSP.elementtype'),
        ),
        migrations.AddField(
            model_name='element',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_elements', to='appManageWSSP.section'),
        ),
        migrations.AddField(
            model_name='element',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_elements', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('altitude', models.IntegerField(default=0)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='province_districts', to='appManageWSSP.province')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_districts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
                'db_table': 'District',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(blank=True, max_length=15)),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country_contacts', to='appManageWSSP.country')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
                'db_table': 'Contact',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('profession_es', models.CharField(max_length=250)),
                ('profession_en', models.CharField(max_length=250)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country_authors', to='appManageWSSP.country')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mediaResource_authors', to='appManageWSSP.mediaresource')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_authors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
                'db_table': 'Author',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SliderElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_es', models.CharField(max_length=250, unique=True)),
                ('title_en', models.CharField(max_length=250, unique=True)),
                ('show_title', models.BooleanField(default=True)),
                ('description_es', models.TextField(blank=True)),
                ('description_en', models.TextField(blank=True)),
                ('media_display_type', models.CharField(choices=[('none', 'None'), ('simple', 'Simple'), ('multiple', 'Multiple')], default='simple', max_length=20)),
                ('display_order', models.PositiveSmallIntegerField(default=1)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('list_icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listIcon_slideElements', to='appManageWSSP.mediaresource')),
                ('medias', models.ManyToManyField(blank=True, null=True, related_name='mediaResource_sliderElements', to='appManageWSSP.mediaresource')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sliderElements', to=settings.AUTH_USER_MODEL)),
                ('slider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slider_sliderElements', to='appManageWSSP.slider')),
            ],
            options={
                'verbose_name': 'SliderElement',
                'verbose_name_plural': 'SliderElements',
                'db_table': 'SliderElement',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='OutstandingArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_es', models.CharField(max_length=100, unique=True)),
                ('title_en', models.CharField(max_length=100, unique=True)),
                ('article_origin', models.CharField(choices=[('web', 'Web'), ('local', 'Local')], default='web', max_length=10)),
                ('source_web', models.URLField(max_length=250)),
                ('description_es', models.TextField(blank=True)),
                ('description_en', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_outstandingArticles', to='appManageWSSP.author')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mediaResource_outstandingArticles', to='appManageWSSP.mediaresource')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_outstandingArticles', to=settings.AUTH_USER_MODEL)),
                ('outstanding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outstanding_outstandingArticles', to='appManageWSSP.outstanding')),
            ],
            options={
                'verbose_name': 'OutstandingArticle',
                'verbose_name_plural': 'OutstandingArticles',
                'db_table': 'OutstandingArticle',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='HtmlArticle',
            fields=[
                ('element_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appManageWSSP.element')),
                ('htmlDesign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='htmlDesign_htmlArticles', to='appManageWSSP.htmldesign')),
            ],
            options={
                'verbose_name': 'htmlArticle',
                'verbose_name_plural': 'htmlArticles',
                'db_table': 'htmlArticle',
                'ordering': ['id'],
            },
            bases=('appManageWSSP.element',),
        ),
        migrations.CreateModel(
            name='GraphicArticle',
            fields=[
                ('element_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appManageWSSP.element')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mediaResource_graphicArticles', to='appManageWSSP.mediaresource')),
            ],
            options={
                'verbose_name': 'GraphicArticle',
                'verbose_name_plural': 'GraphicArticles',
                'db_table': 'GraphicArticle',
                'ordering': ['id'],
            },
            bases=('appManageWSSP.element',),
        ),
    ]
