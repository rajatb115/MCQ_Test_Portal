from django.db import models

class question(models.Model):
	q_test_id=models.CharField(max_length = 20)
	q_number=models.IntegerField()
	q_question=models.CharField(max_length=10000)
	q_op1=models.CharField(max_length=1000)
	q_op2=models.CharField(max_length=1000)
	q_op3=models.CharField(max_length=1000)
	q_op4=models.CharField(max_length=1000)
	q_ans=models.IntegerField()

	def __unicode__(self):
		return(self.q_test_id+" ques="+str(self.q_number))

class student(models.Model):
	stu_name = models.CharField(max_length = 50)
	stu_roll_no = models.IntegerField()
	stu_contact = models.IntegerField()
	stu_email = models.CharField(max_length = 50)
	stu_q_test_id = models.CharField(max_length = 20)

	def __unicode__(self):
		#return meta data to browser ...
		#return(str(self.stu_roll_no)+" "+str(self.stu_q_test_id))
		return(str(self.stu_roll_no))

class stu_solution(models.Model):
	stu_sol_roll_no = models.IntegerField()
	stu_sol_q_test_id = models.CharField(max_length = 20)
	stu_sol_q_number=models.IntegerField()
	stu_sol_q_ans=models.IntegerField(null=True)
	
	def __unicode__(self):
		return(str(self.stu_sol_roll_no)+" "+str(self.stu_sol_q_test_id)+" "+str(self.stu_sol_q_number)+" "+str(self.stu_sol_q_ans))

class teacher(models.Model):
	tech_name = models.CharField(max_length= 50)
	tech_id = models.CharField(max_length = 10,primary_key=True)
	tech_password = models.CharField(max_length =30)

	def __unicode__(self):
		return(self.tech_name)

class paper_list(models.Model):
	pap_tech_id = models.CharField(max_length = 10)
	test_id = models.CharField(max_length = 20,primary_key=True)
	max_ques = models.IntegerField()
	ques_attempt = models.IntegerField()
	maxtime=models.IntegerField()
	ques_made = models.IntegerField(default=0)
	visible = models.IntegerField(default=0)

	def __unicode__(self):
		return(self.pap_tech_id+" "+self.test_id)

class desc(models.Model):
	de_test_id=models.CharField(max_length = 20,primary_key=True)
	desc=models.CharField(max_length = 600)

	def __unicode__(self):
		return(self.de_test_id)