
# views for the project ...

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

# importing models from the project file 
from .models import question,student,stu_solution,teacher,paper_list,desc
import random
import csv



def index(request):
	return render(request, 'personal/home.html') 

def generatetest(request):
	return render(request,'personal/generatetest.html')

def erro(request):
	return HttpResponse('<h1>ERROR 404</h1>')

############################
## Test given by students ##
############################

def starttest(request):
	
	try:
		query1=request.POST.get('name','')
		query2=request.POST.get('rollno','')
		query3=request.POST.get('contact','')
		query4=request.POST.get('email','')
		query5=request.POST.get('Test_Name','')
		counter1=1
		request.session['counter1']=counter1
	
		try:
			preval=student.objects.get(stu_roll_no=query2,stu_q_test_id=query5)
			return HttpResponse('<h1>There is a previous entry with this roll number and test id..<br>Please contact your teacher...</h1>')
		except:
			query6=paper_list.objects.get(test_id=query5)
			if int(query6.visible)==1:
				request.session['name'] = query1
				request.session['rollno'] = query2
				request.session['Test_Name']=query5
				
				p=student(stu_name=query1,stu_roll_no=query2,stu_contact=query3,stu_email=query4,stu_q_test_id=query5)
				p.save()
				timet=paper_list.objects.get(test_id=query5)
				return render(request,'personal/paper.html',{"name":query1,"roll_no":query2,"contact":query3,"timet":timet.maxtime,"testcode":query5})
			else:
				return render(request, 'personal/home.html',{"mess":"1"}) 
	except:
		return render(request, 'personal/home.html',{"mess":"2"})

def testc(request):
	
	try:
		query1=request.session['name']
		query2=request.session['rollno']
		query5=request.session['Test_Name']
		query3=paper_list.objects.get(test_id=query5)
		counter1=int(request.session['counter1'])
		temp1=1

		if counter1==1:
			# random question number generator...
			request.session['counter1']=2
			ptime=int(query3.maxtime)
			ptime=ptime*60*1000
			arr=[]
			for i in range(1,int(query3.max_ques)+1):
				arr.append(i)  # array list genetrating...
			random_list=random.sample(arr,int(query3.ques_attempt))  # random question number generated...

			request.session['random_list']=random_list

			arrq=[]
			for i in range(int(query3.ques_attempt)):
				a=question.objects.get(q_test_id=query5,q_number=random_list[i])
				arrq.append((a.q_number,a.q_question,a.q_op1,a.q_op2,a.q_op3,a.q_op4))

			request.session['arrq']=arrq

			quesn=[]
			qno=[]
			for i in range(query3.ques_attempt):
				quesn.append(i)
				qno.append(i+1)

			request.session['quesn']=quesn
			request.session['qno']=qno

			if temp1<=int(query3.ques_attempt):
				return render(request,'personal/paperc.html',{"name":query1,"roll_no":query2,"testcode":query5,"ques":arrq,"quesn":quesn,"qno":qno,"tm":ptime})
			else:
				del request.session['name']
				del request.session['rollno']
				del request.session['Test_Name']
				del request.session['counter1']
				del request.session['random_list']
				del request.session['arrq']
				del request.session['quesn']
				del request.session['qno']
				return render(request,'personal/thankyou.html')


		elif counter1==2:
			arrq=request.session['arrq']
			quesn=request.session['quesn']
			qno=request.session['qno']
			if temp1<=int(query3.ques_attempt):
				return render(request,'personal/paperc.html',{"name":query1,"roll_no":query2,"testcode":query5,"ques":arrq,"quesn":quesn,"qno":qno})
			else:
				del request.session['name']
				del request.session['rollno']
				del request.session['Test_Name']
				del request.session['counter1']
				del request.session['random_list']
				del request.session['arrq']
				del request.session['quesn']
				del request.session['qno']
				return render(request,'personal/thankyou.html')
	except:
		return HttpResponse('<h1>OOPS!!! </h1><h2>Something went wrong.</h2><br><h3>please contact your teacher.</h3>')


def submit(request):
	try:
		query1=request.session['name']
		query2=int(request.session['rollno'])
		query5=request.session['Test_Name']
		query3=paper_list.objects.get(test_id=query5)
		query4=int(query3.ques_attempt)
		arrq=request.session['arrq']
		vall=0
		soln="anything"
		for i in range(query4):
			soln=request.POST.get(str(arrq[i][0]),'')
			if soln==arrq[i][2]:
				vall=1
			elif soln==arrq[i][3]:
				vall=2
			elif soln==arrq[i][4]:
				vall=3
			elif soln==arrq[i][5]:
				vall=4
			else:
				vall=0

			p=stu_solution(stu_sol_roll_no=query2,stu_sol_q_test_id=query5,stu_sol_q_number=int(arrq[i][0]),stu_sol_q_ans=vall)
			p.save()

		del request.session['name']
		del request.session['rollno']
		del request.session['Test_Name']
		del request.session['counter1']
		del request.session['random_list']
		del request.session['arrq']
		del request.session['quesn']
		del request.session['qno']
		return render(request,'personal/submit.html')

	except:
		return HttpResponse('<h1>OOPS!!! </h1><h2>Something went wrong.</h2><br><h3>please contact your teacher.</h3>')


################################################################
#  teacher login details and computation below this comment....#
################################################################

def teacherlogin(request):
	try:
		query1=request.POST.get('userid','')
		query2=request.POST.get('password','')
		request.session['techid'] = query1
		try:
			p = teacher.objects.get(tech_id =query1)
			request.session['techname'] = p.tech_name
			if p.tech_password == query2:
				return render(request,'personal/teacherlogin.html',{"techid":request.session['techid'],"techname":request.session['techname'],"temporary":"1"})
			else:
				del request.session['techname']
				del request.session['techid']
				return HttpResponse('<h1>ERROR : wrong id or password please <a href="login">try again</a></h1>')
		except Exception as e:
			del request.session['techname']
			del request.session['techid']
			return HttpResponse('<h1>ERROR : wrong id or password please <a href="login">try again</a></h1>')
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def logout(request):
	try:
		del request.session['techname']
		del request.session['techid']
		return HttpResponse('<h1>You are logged out please click <a href="login">here</a> to login again</h1>')
	except Exception as e:
		return HttpResponse('<h1>ERROR :Please <a href="login">try again</a></h1>')


def profile(request):
	try:
		return render(request,'personal/profile.html',{"techid":request.session['techid'],"techname":request.session['techname'],"mess":'1'})
	except:
		return HttpResponse('<h1>OOPS!!! </h1><h2>Something went wrong...</h2><br><h2>please <a href="login">try again</a></h1>')

def updateiddetail(request):
	try:
		query1=request.POST.get('ptechid','')
		query2=request.POST.get('ntechid','')
		query3=request.POST.get('ctechid','')
		p = teacher.objects.get(tech_id =query1)
		if query1==request.session['techid']:
			if query2==query3:
				p.tech_id=query2
				del request.session['techid']
				request.session['techid'] = query2
				teacher.objects.filter(tech_id=query1).update(tech_id=query2)
				paper_list.objects.filter(pap_tech_id=query1).update(pap_tech_id=query2)
				return render(request,'personal/profile.html',{"techid":request.session['techid'],"techname":request.session['techname'],"mess":'2'})
			else:
				del request.session['techname']
				del request.session['techid']
				return HttpResponse('<h1>ERROR : Teacher id did not match please <a href="login">try again</a></h1>')
		else:
			del request.session['techname']
			del request.session['techid']
			return HttpResponse('<h1>ERROR : Wrong teacher id please <a href="login">try again</a></h1>')
	except:
		del request.session['techname']
		del request.session['techid']
		return HttpResponse('<h1>ERROR : Wrong teacher id please <a href="login">try again</a></h1>')

def updatepassdetail(request):
	try:
		query1=request.POST.get('ptechpass','')
		query2=request.POST.get('ntechpass','')
		query3=request.POST.get('ctechpass','')
		p=teacher.objects.get(tech_id=request.session['techid'])
		if p.tech_password==query1:
			if query2==query3:
				teacher.objects.filter(tech_password=query1).update(tech_password=query2)
				return render(request,'personal/profile.html',{"techid":request.session['techid'],"techname":request.session['techname'],"mess":'3'})
			else:
				del request.session['techname']
				del request.session['techid']
				return HttpResponse('<h1>ERROR : Password did not match please <a href="login">try again</a></h1>')
		else:
			del request.session['techname']
			del request.session['techid']
			return HttpResponse('<h1>ERROR : Wrong password please <a href="login">try again</a></h1>')
	except:
		del request.session['techname']
		del request.session['techid']
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def creteststart(request):
	try:
		return render(request,'personal/creteststart.html',{"techid":request.session['techid'],"techname":request.session['techname'],"coun":"1"})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')


def cretest(request):
	try:
		query1=request.POST.get('pcode','')
		query2=int(request.POST.get('maxque',''))
		query3=request.POST.get('attque','')
		query4=request.POST.get('mtime','')
		query6=request.POST.get('descr','')
		if int(query3)<=int(query2) and query2>0:
			query5=1
			request.session['pcode']=query1
			request.session['quesno']= query5
			request.session['maxque']=query2
			try:
				t=paper_list.objects.get(test_id=query1)
				return render(request,'personal/creteststart.html',{"techid":request.session['techid'],"techname":request.session['techname'],"coun":"2","query66":query6})
			except:
				p=desc(de_test_id=query1,desc=query6)
				p.save()
				p=paper_list(pap_tech_id=request.session['techid'],test_id=query1,max_ques=query2,ques_attempt=query3,maxtime=query4)
				p.save()
				return render(request,'personal/cretestf.html',{"techid":request.session['techid'],"techname":request.session['techname'],"quesno":query5,"maxq":query2})
		else:
			if query2<=0:
				return render(request,'personal/creteststart.html',{"techid":request.session['techid'],"techname":request.session['techname'],"coun":"5","query66":query6})
			else:
				return render(request,'personal/creteststart.html',{"techid":request.session['techid'],"techname":request.session['techname'],"coun":"4","query66":query6})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')


def cretestf(request):
	try:
		query1=request.POST.get('question','')
		query2=request.POST.get('op1','')
		query3=request.POST.get('op2','')
		query4=request.POST.get('op3','')
		query5=request.POST.get('op4','')
		query6=request.POST.get('ans','')
		query7=int(request.session['quesno'])
		query8=request.session['pcode']
		query9=int(request.session['maxque'])
		
		if int(request.session['maxque'])+1 > int(request.session['quesno']):
			del request.session['quesno']
			request.session['quesno']= query7+1
			p=question(q_test_id=query8,q_number=query7,q_question=query1,q_op1=query2,q_op2=query3,q_op3=query4,q_op4=query5,q_ans=query6)
			p.save()
			paper_list.objects.filter(test_id=request.session['pcode']).update(ques_made=query7)
		
		if int(request.session['quesno']) < int(request.session['maxque'])+1:
			return render(request,'personal/cretestf.html',{"techid":request.session['techid'],"techname":request.session['techname'],"quesno":int(request.session['quesno']),"maxq":query9})
		else:
			del request.session['quesno']
			del request.session['pcode']
			del request.session['maxque']
			return render(request,'personal/teacherlogin.html',{"techid":request.session['techid'],"techname":request.session['techname'],"temporary":"2"})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')


def underconstruction(request):
	try:
		return render(request,'personal/underconstruction.html',{"techid":request.session['techid'],"techname":request.session['techname']})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def edittest(request):
	try:
		p=paper_list.objects.filter(pap_tech_id=request.session['techid'])
		return render(request,'personal/edittest.html',{"techid":request.session['techid'],"techname":request.session['techname'],"pclist":p})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def edittestoption(request):
	try:
		query1=request.POST.get('sel1','')
		request.session['testid']=query1
		return render(request,'personal/edittestop.html',{"techid":request.session['techid'],"techname":request.session['techname'],"tid":query1})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')
	
def prevedittest(request):
	try:
		p=paper_list.objects.get(test_id=request.session['testid'])
		request.session['pcode']=request.session['testid']
		del request.session['testid']
		request.session['quesno']= p.ques_made+1
		request.session['maxque']=p.max_ques
		if int(request.session['quesno'])<int(request.session['maxque']):
			return render(request,'personal/cretestf.html',{"techid":request.session['techid'],"techname":request.session['techname'],"quesno":request.session['quesno'],"maxq":request.session['maxque']})
		else:
			del request.session['pcode']
			del request.session['quesno']
			del request.session['maxque']
			return render(request,'personal/nomoreques.html',{"techid":request.session['techid'],"techname":request.session['techname']})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def perticularedittest(request):
	try:
		return render(request,'personal/gotequesno.html',{"techid":request.session['techid'],"techname":request.session['techname'],"tid":request.session['testid'],"e":"1"})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def equestion(request):
	try:
		query1=int(request.POST.get('qono',0))
		q=paper_list.objects.get(test_id=request.session['testid'])
		if int(q.ques_made)==0:
			return render(request,'personal/gotequesno.html',{"techid":request.session['techid'],"techname":request.session['techname'],"tid":request.session['testid'],"e":"4"})
		elif query1>0 and query1<=q.ques_made:
			request.session['q_numberd']=query1
			p=question.objects.get(q_test_id=request.session['testid'],q_number=query1)
			return render(request,'personal/updgotequesno.html',{"techid":request.session['techid'],"techname":request.session['techname'],"tid":request.session['testid'],"p":p})
		else:
			return render(request,'personal/gotequesno.html',{"techid":request.session['techid'],"techname":request.session['techname'],"tid":request.session['testid'],"e":"2","rang":q.ques_made})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def updatesave(request):
	try:
		query1=request.POST.get('question','')
		query2=request.POST.get('op1','')
		query3=request.POST.get('op2','')
		query4=request.POST.get('op3','')
		query5=request.POST.get('op4','')
		query6=request.POST.get('ans','')
		question.objects.filter(q_test_id=request.session['testid'],q_number=request.session['q_numberd']).update(q_question=query1,q_op1=query2,q_op2=query3,q_op3=query4,q_op4=query5,q_ans=query6)
		return render(request,'personal/gotequesno.html',{"techid":request.session['techid'],"techname":request.session['techname'],"tid":request.session['testid'],"e":"3"})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def publishtest(request):
	try:
		p=paper_list.objects.filter(pap_tech_id=request.session['techid'],visible=0)
		q=paper_list.objects.filter(pap_tech_id=request.session['techid'],visible=1)
		return render(request,'personal/publishtest.html',{"techid":request.session['techid'],"techname":request.session['techname'],"p":p,"q":q,"messa":"1"})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')


def publishselected(request):
	try:
		query1=request.POST.get('sel1','')
		query2=paper_list.objects.get(test_id=query1)
		if int(query2.max_ques)==int(query2.ques_made):
			paper_list.objects.filter(test_id=query1).update(visible=1)
			p=paper_list.objects.filter(pap_tech_id=request.session['techid'],visible=0)
			q=paper_list.objects.filter(pap_tech_id=request.session['techid'],visible=1)
			return render(request,'personal/publishtest.html',{"techid":request.session['techid'],"techname":request.session['techname'],"p":p,"q":q,"messa":"2"})
		else:
			p=paper_list.objects.filter(pap_tech_id=request.session['techid'],visible=0)
			q=paper_list.objects.filter(pap_tech_id=request.session['techid'],visible=1)
			return render(request,'personal/publishtest.html',{"techid":request.session['techid'],"techname":request.session['techname'],"p":p,"q":q,"messa":"4"})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')


def publishunselected(request):
	try:
		query1=request.POST.get('sel2','')
		paper_list.objects.filter(test_id=query1).update(visible=0)
		p=paper_list.objects.filter(pap_tech_id=request.session['techid'],visible=0)
		q=paper_list.objects.filter(pap_tech_id=request.session['techid'],visible=1)
		return render(request,'personal/publishtest.html',{"techid":request.session['techid'],"techname":request.session['techname'],"p":p,"q":q,"messa":"3"})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def reviewpaper1(request):
	try:
		p=paper_list.objects.filter(pap_tech_id=request.session['techid'])
		return render(request,'personal/reviewpaper1.html',{"techid":request.session['techid'],"techname":request.session['techname'],"p":p})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')


def reviewpaper2(request):
	try:
		query1=request.POST.get('sel1','')
		pp=paper_list.objects.get(test_id=query1)
		qq=question.objects.filter(q_test_id=query1)
		rr=desc.objects.get(de_test_id=query1)
		return render(request,'personal/reviewpaper2.html',{"techid":request.session['techid'],"techname":request.session['techname'],"p":pp,"pp":rr,"q":qq,"testcod":query1})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def result(request):
	try:
		query1=request.session['techid']
		query2=request.session['techname']
		query3=paper_list.objects.filter(pap_tech_id=request.session['techid'])
		query4=stu_solution.objects.filter().values('stu_sol_q_test_id').distinct()
		query5=[]
		for i in query3:
			for j in query4:
				if i.test_id==j["stu_sol_q_test_id"]:
					query5.append(j["stu_sol_q_test_id"])
					break 
		return render(request,'personal/result.html',{"techid":query1,"techname":query2,"p":query5})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def result_gen_option(request):
	try:
		query1=request.session['techid']
		query2=request.session['techname']
		query3=request.POST.get('sel1','')
		request.session['testid']=query3
		return render(request,'personal/result1.html',{"techid":query1,"techname":query2,"id":query3})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def checkstudentresult(request):
	try:
		query1=request.session['techid']
		query2=request.session['techname']
		query3=request.session['testid']
		query4=student.objects.filter(stu_q_test_id=query3)
		return render(request,'personal/result2.html',{"techid":query1,"techname":query2,"roll":query4})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')


def show_ques_wise_result(request):
	try:
		query1=request.session['techid']
		query2=request.session['techname']
		query3=request.session['testid']
		query4=int(request.POST.get('rollno1',''))
		query5=student.objects.get(stu_roll_no=query4,stu_q_test_id=query3)
		
		# marks computation for every student
		marks=0
		query6=stu_solution.objects.filter(stu_sol_roll_no=query4,stu_sol_q_test_id=query3)
		for i in query6:
			query7=question.objects.get(q_test_id=query3,q_number=int(i.stu_sol_q_number))
			if int(i.stu_sol_q_ans)==int(query7.q_ans):
				marks=marks+1
		
		return render(request,'personal/result3.html',{"techid":query1,"techname":query2,"tid":query3,"rollno":query4,"marks":marks,"stuname":query5.stu_name})
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')

def downloadcsv(request):
	try:
		query1=request.session['techid']
		query2=request.session['techname']
		query3=request.session['testid']
		query4=stu_solution.objects.filter(stu_sol_q_test_id=query3).values('stu_sol_roll_no').distinct()
		query6=paper_list.objects.get(test_id=query3)

		response =HttpResponse(content_type='text/csv')
		response['Content-Disposition']='attachment';filename="result.csv"
		writer = csv.writer(response)
		writer.writerow(['Name','Rollno','Max marks','obtained marks'])

		for j in query4:

			query5=student.objects.get(stu_roll_no=int(j["stu_sol_roll_no"]),stu_q_test_id=query3)

			marks=0
			query7=stu_solution.objects.filter(stu_sol_roll_no=int(j["stu_sol_roll_no"]),stu_sol_q_test_id=query3)
			for i in query7:
				query8=question.objects.get(q_test_id=query3,q_number=int(i.stu_sol_q_number))
				if int(i.stu_sol_q_ans)==int(query8.q_ans):
					marks=marks+1

			writer.writerow([query5.stu_name,j["stu_sol_roll_no"],query6.ques_attempt,marks])

		return response
	except:
		return HttpResponse('<h1>ERROR : Please <a href="login">try again</a></h1>')