# Generated by Django 3.2 on 2021-06-05 14:20

from django.db import migrations, models
import django.db.models.deletion
import hotel.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buffet_round',
            fields=[
                ('buffet_round', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('charge', models.FloatField(null=True)),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.CharField(default=hotel.models.Customer.genID, max_length=11, primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=64)),
                ('lname', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('tel', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer_booking',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('booking_no', models.CharField(max_length=11, null=True)),
                ('resb_no', models.CharField(max_length=11, null=True, unique=True)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='hotel.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion_type',
            fields=[
                ('promotion_code', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('promotion_name', models.CharField(max_length=32)),
                ('promotion_detail', models.CharField(max_length=500)),
                ('start_date', models.DateField()),
                ('expire_date', models.DateField()),
                ('discount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('roomtype', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('capacity', models.IntegerField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('service_name', models.CharField(max_length=10, unique=True)),
                ('charge', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.CharField(default=hotel.models.Staff.genID, max_length=12, primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=64)),
                ('lname', models.CharField(max_length=64)),
                ('dob', models.DateField()),
                ('job_title', models.CharField(choices=[('S', 'Staff'), ('A', 'Admin'), ('M', 'Manager'), ('R', 'Receptionist'), ('HS', 'Hotel Staff'), ('RS', 'Restaurant Staff')], default='S', max_length=5)),
                ('salary', models.FloatField(null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Room_detail',
            fields=[
                ('detail_no', models.AutoField(primary_key=True, serialize=False)),
                ('room_count', models.IntegerField()),
                ('roomtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room')),
                ('service_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.service')),
            ],
        ),
        migrations.CreateModel(
            name='Room_booking',
            fields=[
                ('bhsurrogate', models.AutoField(primary_key=True, serialize=False)),
                ('date_check_in', models.DateTimeField()),
                ('date_check_out', models.DateTimeField()),
                ('number_guest', models.IntegerField()),
                ('total_charge', models.FloatField()),
                ('payment_method', models.CharField(max_length=32, null=True)),
                ('booking_no', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='hotel.customer_booking')),
                ('detail_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room_detail')),
                ('promotion_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel.promotion_type')),
            ],
        ),
        migrations.CreateModel(
            name='Resbooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_guest', models.IntegerField()),
                ('eatdate', models.DateTimeField()),
                ('total_charge', models.FloatField()),
                ('paymentmethod', models.CharField(max_length=32)),
                ('buffet_round', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel.buffet_round')),
                ('promotion_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel.promotion_type')),
                ('resb_no', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='hotel.customer_booking')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_no', models.CharField(max_length=12, primary_key=True, serialize=False, unique=True)),
                ('tax', models.FloatField()),
                ('date', models.DateField()),
                ('booking_no', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='hotel.room_booking')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='hotel.customer')),
                ('resb_no', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='hotel.resbooking')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.staff')),
            ],
        ),
    ]

