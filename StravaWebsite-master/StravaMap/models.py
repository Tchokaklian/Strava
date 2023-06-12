from django.db import models

# Create your models here.

class Col(models.Model):		
	col_id = models.IntegerField(auto_created=True,  primary_key=True)
	col_name = models.CharField(max_length=200)
	col_code = models.CharField(max_length=20, null=True, unique=True)
	col_alt = models.IntegerField(null=True)
	col_lon = models.FloatField(null=True)
	col_lat = models.FloatField(null=True)
	col_type = models.CharField(max_length=10, null= True)	

class Activity(models.Model):
	act_id = models.IntegerField(null=False, primary_key=True)	
	strava_id = models.IntegerField(null=False, default=0)	
	user_id	= models.IntegerField(null=False)	
	act_name = models.CharField(max_length=200, null=True, default="")
	act_start_date = models.DateTimeField(null=False)
	act_dist = models.FloatField(null=True)
	act_den =  models.IntegerField(null=True)
	act_type = models.CharField(max_length=10, null= True)
	act_time = models.IntegerField(null=True)	
	act_power = models.IntegerField(null=True)
	act_status = models.IntegerField(null=True)
	def act_dist_km(self):
		return self.act_dist/1000

class Col_perform(models.Model):
	col_perf_id = models.IntegerField(auto_created=True,  primary_key=True)
	col_code = models.CharField(max_length=20, null=False, default="-" )
	strava_id = models.IntegerField(null=False)	

class Col_counter(models.Model):
	col_count_id = models.IntegerField(auto_created=True,  primary_key=True)
	col_code = models.CharField(max_length=20, default="-")
	user_id	= models.IntegerField(null=False)
	col_count = models.IntegerField(null=False)	
	def nom_col(self):		
		sc = self.col_code
		q1 = Col.objects.filter(col_code=sc)		
		return q1[0].col_name