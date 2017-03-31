import cv2
import cognitive_face as CF
import MySQLdb
 
# Camera 0 is the integrated web cam on my netbook
camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 1
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.

 
# Captures a single image from the camera and returns it in PIL format

 
# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
db1 = MySQLdb.connect("localhost","root","","MyDB")
cursor = db1.cursor()
sql = 'CREATE DATABASE MyDB'
#cursor.execute(sql)
table = 'CREATE TABLE MyTable5 (gender VARCHAR(10),age INTEGER,moustache VARCHAR(20), beard VARCHAR(20), sideburns VARCHAR(20),smile VARCHAR(20))'
#cursor.execute(table)

PersonTable = 'CREATE TABLE Person(id INTEGER,avg_smile DOUBLE,age INTEGER,gender VARCHAR(20))'
#cursor.execute(PersonTable)
person=0
uninterested_person=0
c=0
x=0
avg_smile=0
sum=0
result1=""
flag=0
while(1):

	camera = cv2.VideoCapture(camera_port)
	
	def get_image():
	# read is the easiest way to get a full image out of a VideoCapture object.
		retval, im = camera.read()
		return im
	
	for i in xrange(ramp_frames):
	 temp = get_image()
	#print("Taking image...")
	# Take the actual image we want to kee

	camera_capture = get_image()
	file = "test_image.png"
	# A nice feature of the imwrite method is that it will automatically choose the
	# correct format based on the file extension you provide. Convenient!
	cv2.imwrite(file, camera_capture)
	 
	# You'll want to release the camera, otherwise you won't be able to create a new
	# capture object until your script exits
	del(camera)

	KEY = 'ce99e4de092c491bbf473609d6538e89'  # Replace with a valid Subscription Key here.
	CF.Key.set(KEY)

	img_url = 'test_image.png'
	result = CF.face.detect(img_url,True,False,'age,gender,smile,facialHair')
	if (c==0):
		result1 = result
	print result
	if not result:
		break;
	no_of_ppl=len(result)
	
	for j in range(0,no_of_ppl):
		age = result[j]['faceAttributes']['age']
		gender = result[j]['faceAttributes']['gender']
		moustache = result[j]['faceAttributes']['facialHair']['moustache']
		beard = result[j]['faceAttributes']['facialHair']['beard']
		sideburns = result[j]['faceAttributes']['facialHair']['sideburns']
		smile = result[j]['faceAttributes']['smile']
		cursor.execute('''INSERT into MyTable5 (gender, age, moustache, beard, sideburns, smile)
				  values (%s, %s, %s, %s, %s, %s)''',
					(gender, age,moustache,beard,sideburns,smile))
		if(c>0):
			for i in range(0,len(result1)):
				age = result1[i]['faceAttributes']['age']
				gender = result1[i]['faceAttributes']['gender']
				moustache = result1[i]['faceAttributes']['facialHair']['moustache']
				beard = result1[i]['faceAttributes']['facialHair']['beard']
				sideburns = result1[i]['faceAttributes']['facialHair']['sideburns']
				smile = result1[i]['faceAttributes']['smile']
			
				diff_age=abs(age-result[j]['faceAttributes']['age'])
				print diff_age
				if ( gender == result[j]['faceAttributes']['gender'] ):
					diff_gender=0
				else:
					diff_gender=3

				diff_facial=abs(result[j]['faceAttributes']['facialHair']['moustache']-moustache)+abs(result[j]['faceAttributes']['facialHair']['beard']-beard)+abs(result[j]['faceAttributes']['facialHair']['sideburns']-sideburns)
				if ( diff_age+diff_gender+diff_facial <= 2.6 ):
					print "Same person"
					sum = sum + result[j]['faceAttributes']['smile']
					x=x+1
					if( x==3 ):
						person = person + 1
						sum = sum + smile
						avg_smile = sum / 3
						sum = 0
						x=0
						if(flag==0):
							print 'jsadgakj'
							cursor.execute('''INSERT into Person (id,avg_smile,age,gender)
							values (%s, %s, %s, %s)''',
							(person,avg_smile,age,gender))
							flag=1;
					
						if (avg_smile>0.5) :
							print 'Interested'
						else:
							print 'NotInterested'
				else:	
					print "Not the same person"
					flag=0
					uninterested_person=uninterested_person+1
					x=0
				result1 = result
				#print result1
	c=c+1
	#print (c)
	 

db1.commit()
#select = 'SELECT COUNT(age) as count FROM MyTable5'
#cursor.execute(select)

#row = cursor.fetchone()

#while row is not None:
#			print(row)
#			row = cursor.fetchone()

persondisplay = 'SELECT * FROM Person WHERE age BETWEEN 25 and 30'
cursor.execute(persondisplay)
row = cursor.fetchone()

while row is not None:
			print(row)
			row = cursor.fetchone()
print 'Number Of Uninterested People are : ' 
print uninterested_person