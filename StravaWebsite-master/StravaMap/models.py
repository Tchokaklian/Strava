from django.db import models
from numpy import generic

# Create your models here.

class Col(models.Model):		
	col_id = models.IntegerField(auto_created=True,  primary_key=True)
	col_name = models.CharField(max_length=200)
	col_code = models.CharField(max_length=20, null=True, unique=True)
	col_alt = models.IntegerField(null=True)
	col_lon = models.FloatField(null=True)
	col_lat = models.FloatField(null=True)
	col_type = models.CharField(max_length=10, null= True)	

	def get_activities_passed(self):
		sc = self.col_code		
		q1 = Col_perform.objects.filter(col_code=sc)		
		return q1

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

	def get_act_dist_km(self):
		return self.act_dist/1000
	
	def get_col_passed(self):
		sc = self.strava_id		
		q1 = Col_perform.objects.filter(strava_id=sc)		
		return q1
						
class Col_perform(models.Model):
	col_perf_id = models.IntegerField(auto_created=True,  primary_key=True)
	col_code = models.CharField(max_length=20, null=False, default="-" )
	strava_id = models.IntegerField(null=False)	

	class Meta:
		ordering = ['-strava_id']

	def get_col_name(self):		
		sc = self.col_code
		q1 = Col.objects.filter(col_code=sc)		
		return q1[0].col_name
	
	def get_col_id(self):		
		sc = self.col_code
		q1 = Col.objects.filter(col_code=sc)		
		return q1[0].col_id
		
	def get_activity_name(self):		
		sc = self.strava_id
		q1 = Activity.objects.filter(strava_id=sc)			
		return q1[0].act_name
	
	def get_activity_id(self):		
		sc = self.strava_id
		q1 = Activity.objects.filter(strava_id=sc)			
		return q1[0].act_id
	
	def get_activity_date(self):		
		sc = self.strava_id
		q1 = Activity.objects.filter(strava_id=sc)			
		return q1[0].act_start_date

class Col_counter(models.Model):
	col_count_id = models.IntegerField(auto_created=True,  primary_key=True)
	col_code = models.CharField(max_length=20, default="-")
	user_id	= models.IntegerField(null=False)
	col_count = models.IntegerField(null=False)	

	def get_col_name(self):		
		sc = self.col_code
		q1 = Col.objects.filter(col_code=sc)		
		return q1[0].col_name
	
	def get_col_id(self):		
		sc = self.col_code
		q1 = Col.objects.filter(col_code=sc)				
		return q1[0].col_id
	
class Strava_user(models.Model):	
	strava_user_id = models.IntegerField(auto_created=True,  primary_key=True)
	strava_user = models.CharField(max_length=100, default="-") 
	first_name = models.CharField(max_length=100, default="-")
	last_name = models.CharField(max_length=100, default="-")
	token_type = models.CharField(max_length=100, default="-")
	access_token = models.CharField(max_length=100, default="-")
	refresh_token = models.CharField(max_length=100, default="-")
	expire_at = models.IntegerField(null=True)
	athlete_id = models.IntegerField(null=True)
	city = models.CharField(max_length=50, null=True)
	country = models.CharField(max_length=50, null=True)
	sex = models.CharField(max_length=100, null=True)