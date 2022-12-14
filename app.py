from flask import Flask,render_template,request,jsonify
import numpy as np
import pickle
import requests
import os
import logging

model=pickle.load(open('Healthcare.pkl','rb'))


app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    

@app.route('/',methods=['POST','GET'])
def home():
    page='cardiac-arrest-smarthealth-herokuapp'
    url="https://smarthealthmonitoring.com/contactus/predictiondata"
    header=request.headers
    agent=request.headers.get('User-Agent')
    referr=request.referrer
    
    current_count = read_click_db()
    if current_count is not None:
        new_count = int(current_count) + 1
        current_count=write_click_db(new_count)
    else:
        write_click_db(1)
     
    app.logger.debug('current_count :'+ current_count)
    app.logger.debug('new_count after :'+ str(new_count))
	
    def get_my_ip():
        return jsonify({'ip': request.remote_addr}), 200

    ip=get_my_ip()
    return render_template('home.html',counter=new_count)

@app.route('/predict', methods=['POST','GET'] )
def predict():
    data1=float(request.form['a'])
    data2=float(request.form['b'])
    data3=float(request.form['c'])
    data4=float(request.form['d'])
    data5=float(request.form['e'])
    data6=float(request.form['f'])
    data7=float(request.form['g'])
    data8=float(request.form['h'])
    data9=float(request.form['i'])
    data10=float(request.form['j'])
    features=np.array([data1,data2,data3,data4,data5,data6,data7,data8,data9,data10])
    pred = model.predict([features])
    
    def result():
        if pred == 0:
            return 'There is NO evidence of possible Cardiac arrest'
        elif pred == 1:
            return 'There is evidence of possible Cardiac arrest'

    def resultcolor():
        if pred == 0:
            return "green"
        elif pred == 1:
            return "red"
    
    return render_template('home.html',statement=result(),resultcolor=resultcolor())


@app.route('/test')
def test():
    current_count = read_click_db()
    if current_count is not None:
        new_count = int(current_count) + 1
        current_count=write_click_db(new_count)
    else:
        write_click_db(1)
     
    app.logger.debug('current_count :'+ current_count)
    app.logger.debug('new_count after :'+ str(new_count))
    page='cardiac-arrest-smarthealth-herokuapp'
    url="https://smarthealthmonitoring.com/contactus/predictiondata"
    header=request.headers
    agent=request.headers.get('User-Agent')
    referr=request.referrer
	
    def get_my_ip():
        return request.remote_addr

    ip=get_my_ip()
    app.logger.debug('IP :'+ ip)
    params = {"ip": ip,"headers":header,"user_agent":agent,"referr_url_sess ":referr,"page":page}
    print (requests.get(url, params).text)

    return render_template('test.html',counter=new_count)

def read_click_db() -> str:
    if not os.path.isfile("visitors.txt"):
        print("File doesn't exist")
        return
    with open("visitors.txt", "rt") as f:
        click_counter = f.readline()
        f.close()
    return click_counter


def write_click_db(counter: int):
    with open("visitors.txt", "wt") as f:
        f.write(str(counter))
        f.close()
        return str(counter)


@app.route('/predict_test', methods=['POST','GET'] )
def predict_test():
    data1=float(request.form['a'])
    data2=float(request.form['b'])
    data3=float(request.form['c'])
    data4=float(request.form['d'])
    data5=float(request.form['e'])
    data6=float(request.form['f'])
    data7=float(request.form['g'])
    data8=float(request.form['h'])
    data9=float(request.form['i'])
    data10=float(request.form['j'])
    features=np.array([data1,data2,data3,data4,data5,data6,data7,data8,data9,data10])
    pred = model.predict([features])

    #save data in smart health
    form_data = ';'.join(map(str, features)) 
    url="https://smarthealthmonitoring.com/contactus/predictiondata"
	
    def get_my_ip():
        return request.remote_addr

    ip=get_my_ip()
    app.logger.debug('IP :'+ ip)
    app.logger.debug('form data :'+ form_data)

    params = {"ip": ip,"form_data":form_data}
    print (requests.get(url, params).text)

    def result():
        if pred == 0:
            return 'There is NO evidence of possible Cardiac arrest'
        elif pred == 1:
            return 'There is evidence of possible Cardiac arrest'

    def resultcolor():
        if pred == 0:
            return "green"
        elif pred == 1:
            return "red"
    
    return render_template('test.html',statement=result(),resultcolor=resultcolor())


@app.route("/save_email", methods=['POST'])
def save_email():
    email = request.form.get('email')
	#base_url = "https://smarthealthmonitoring.com/contactus/save/?email="
	#url = base_url + email
    if request.method == 'POST':
        url = "https://smarthealthmonitoring.com/contactus/save"
        params = {"email": email}
        print (requests.get(url, params).text)
        confirm_msg = "Your email have been saved. Thank you!"
    else:
	    confirm_msg = "Try contacting info@smarthealthmonitoring.com"
    return render_template("home.html", confirm_msg=confirm_msg)

@app.route("/diabetes",methods=["GET","POST"])
def diabetes():
	if request.method=='GET':
		return render_template("form.html")
	else:
		ds=pd.read_csv('diabetes1.csv')
		X=ds.iloc[:,[0,1,2,5,6]]
		y=ds.iloc[::,-1]
		X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.10,random_state=0)
		model=LogisticRegression()
		model.fit(X_train,y_train)
		Pregnancies=int(request.form['Pregnancies'])
		Glucose=int(request.form['Glucose'])
		BloodPressure=int(request.form['BloodPressure'])
		BMI=float(request.form['BMI'])
		DiabetesPedigreeFunction=float(request.form['DiabetesPedigreeFunction'])
		new=np.array([[Pregnancies,Glucose,BloodPressure,BMI,DiabetesPedigreeFunction]])
		y_pred=model.predict(new)
		return render_template("result.html",y_pred=y_pred)



@app.route("/heart",methods=["GET","POST"])
def heart():
	if request.method=='GET':
		return render_template('form1.html')
	else:
		ds=pd.read_csv('heart.csv')
		X=ds.drop('target',axis=1)
		y=ds.iloc[:,-1]
		X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.10,random_state=0)
		reg=LogisticRegression(max_iter=1200000)
		reg.fit(X_train,y_train)
		Age=int(request.form['Age'])
		gender=int(request.form['gender'])
		cp=int(request.form['cp'])
		trestbps=int(request.form['trestbps'])
		chol=int(request.form['chol'])
		fbs=int(request.form['fbs'])
		restecg=int(request.form['restecg'])
		thalach=int(request.form['thalach'])
		new=np.array([[Age,gender,cp,trestbps,chol,fbs,restecg,thalach,ds['exang'].mean(),ds['oldpeak'].mean(),ds['slope'].mean(),ds['ca'].mean(),ds['thal'].mean()]])
		y_pred=reg.predict(new)
		return render_template("result1.html",y_pred=y_pred)




@app.route("/liverprediction",methods=["GET","POST"])
def liver():
	if request.method=='GET':
		return render_template('form2.html')
	else:
		df=pd.read_csv('indian_liver_patient.csv')
		dummies=pd.get_dummies(df['Gender'])
		df['Albumin_and_Globulin_Ratio'].fillna(df['Albumin_and_Globulin_Ratio'].mean(),inplace=True)
		df1=pd.concat([df,dummies],axis='columns')
		X=df1.drop(['Gender','Female','Dataset'],axis=1)
		y=df1.iloc[:,-3]
		X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.10,random_state=0)
		model = LogisticRegression(max_iter=12000000)
		model.fit(X_train,y_train)
		Age=int(request.form['Age'])
		gender=int(request.form['gender'])
		Total_Bilirubin=int(request.form['Total_Bilirubin'])
		Alkaline_Phosphotase=int(request.form['Alkaline_Phosphotase'])
		Alamine_Aminotransferase=int(request.form['Alamine_Aminotransferase'])
		Aspartate_Aminotransferase=int(request.form['Aspartate_Aminotransferase'])
		Total_Protiens=int(request.form['Total_Protiens'])		
		Albumin=int(request.form['Albumin'])
		new=np.array([[Age,Total_Bilirubin,df1['Direct_Bilirubin'].mean(),Alkaline_Phosphotase,Alamine_Aminotransferase,Aspartate_Aminotransferase,Total_Protiens,Albumin,df1['Albumin_and_Globulin_Ratio'].mean(),gender]])
		y_pred=model.predict(new)
		return render_template('result2.html',y_pred=y_pred)
		


@app.route('/kidneydisease',methods=['GET','POST'])
def kidney():
	if request.method=='GET':
		return render_template('kidneyform.html')
	else:
		with open('kidney_predict','rb') as f:
			model=pickle.load(f)
		Age=int(request.form['Age'])
		Blood_Pressure=int(request.form['Blood_Pressure'])
		Specific_Gravity=float(request.form['Specific_Gravity'])
		Albumin=int(request.form['Albumin'])
		Sugar=int(request.form['Sugar'])
		Red_Blood_Cells=int(request.form['Red_Blood_Cells'])
		new=np.array([[Age,Blood_Pressure,Specific_Gravity,Albumin,Sugar,Red_Blood_Cells]])
		y_pred=model.predict(new)
		return render_template('result3.html',y_pred=y_pred)



@app.route("/backpain",methods=["GET","POST"])
def backpain():
	if request.method=="GET":
		return render_template("backpainform.html")
	else:
		pelvic_incidence=float(request.form['pelvic_incidence'])
		pelvic_tilt=float(request.form['pelvic_tilt'])
		lumbar_lordosis_angle=float(request.form['lumbar_lordosis_angle'])
		sacral_slope=float(request.form['sacral_slope'])
		pelvic_radius=float(request.form['pelvic_radius'])
		restecgdegree_spondylolisthesis=float(request.form['restecgdegree_spondylolisthesis'])
		pelvic_slope=float(request.form['pelvic_slope'])
		Direct_tilt=float(request.form['Direct_tilt'])
		thoracic_slope=float(request.form['thoracic_slope'])
		cervical_tilt=float(request.form['cervical_tilt'])
		sacrum_angle=float(request.form['sacrum_angle'])
		scoliosis_slope=float(request.form['scoliosis_slope'])
		df=pd.read_csv('Dataset_spine.csv')
		df.columns=['pelvic_incidence','pelvic_tilt','lumbar_lordosis_angle','sacral_slope','pelvic_radius','degree_spondylolisthesis','pelvic_slope','Direct_tilt','thoracic_slope','cervical_tilt','sacrum_angle','scoliosis_slope','Class']
		X=df.drop('Class',axis=1)
		y=df['Class']
		model=LogisticRegression(max_iter=120000000)
		model.fit(X,y)
		new=np.array([[pelvic_incidence,pelvic_tilt,lumbar_lordosis_angle,sacral_slope,pelvic_radius,restecgdegree_spondylolisthesis,pelvic_slope,Direct_tilt,thoracic_slope,cervical_tilt,sacrum_angle,scoliosis_slope]])
		y_pred=model.predict(new)
		return render_template("backpainresult.html",y_pred=y_pred)



@app.route("/Tuberculosis",methods=["GET","POST"])
def tb():
	if request.method=="GET":
		return render_template('tbform.html')
	else:
		df=pd.read_csv("tb.csv")
		X=df.drop(['prognosis','Tuberculosis','id'],axis=1)
		y=df['Tuberculosis']
		model=LogisticRegression()
		model.fit(X,y)
		fatigue=int(request.form['fatigue'])
		weight_loss=int(request.form['weight_loss'])
		loss_of_appetite=int(request.form['loss_of_appetite'])
		mild_fever=int(request.form['mild_fever'])
		chills=int(request.form['chills'])
		sweating=int(request.form['sweating'])
		mucoid_sputum=int(request.form['mucoid_sputum'])
		cough=int(request.form['cough'])
		chest_pain=int(request.form['chest_pain'])
		new=np.array([[fatigue,weight_loss,loss_of_appetite,mild_fever,chills,sweating,mucoid_sputum,cough,chest_pain]])
		y_pred=model.predict(new)
		return f'{y_pred}'



@app.route('/about')
def about():
	return render_template('about.html')

if __name__=='__main__':
    app.run()
