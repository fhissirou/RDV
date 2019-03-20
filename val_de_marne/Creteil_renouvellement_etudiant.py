
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime


class Prefecture:

	def make_body(self):
			return """
			<body>
			<p> Il existe une plage horaire disponible sur le site de la préfecture du val de marne.<p>
			</body>

			"""

	def sendMail(self, SUBJECT, BODY, TO):
			try:

				FROM='your adress mail '
				password = "password"
				MESSAGE = MIMEMultipart()
				MESSAGE['subject'] = SUBJECT
				MESSAGE['To'] = str(TO)
				MESSAGE['From'] = FROM

				HTML_BODY = MIMEText(BODY, 'html')
				MESSAGE.attach(HTML_BODY)

				fp = open("screenshot.png", 'rb')
				img = MIMEImage(fp.read())
				fp.close()
				img.add_header('Content-ID', '<{}>'.format("screenshot.png"))
				MESSAGE.attach(img)


				server = smtplib.SMTP('smtp.gmail.com:587')

				server.starttls()
				server.login(FROM,password)
				server.sendmail(FROM, TO, MESSAGE.as_string())
				server.quit()
				print("Email sent!")
			except:
				print("Email wrong\n")



	def updateSelenium(self, SUBJECT, TO):

		while True:

			try:
				url = "http://www.val-de-marne.gouv.fr/booking/create/5439/0"
				driver = webdriver.PhantomJS()
				driver.get(url)
				print("\n-----\n"+url)
				time.sleep(5)
				driver.find_elements_by_xpath("html[1]/body[1]/div[2]/div[2]/a[2]")[0].click()
				time.sleep(1)
				python_button_demande = driver.find_elements_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[3]/div[1]/div[2]/form[1]/div[5]/input[1]")[0]
			
				checkbox = driver.find_elements_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[3]/div[1]/div[2]/form[1]/div[4]/input[1]")[0]
				checkbox.click()
				time.sleep(1)
				python_button_demande.click()
				time.sleep(5)
			except:
				driver.close()
				continue

			try:

				try:
					try:
						python_button_text = driver.find_elements_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[3]/div[1]/div[2]/form[1]")[0].text
						if python_button_text.find("Il n'existe plus de plage horaire libre pour votre demande de rendez-vous") != -1:
							print("Il n'existe plus de plage horaire libre pour votre demande de rendez-vous.")
						else:
							driver.save_screenshot("screenshot.png")
							time.sleep(5)
							body = self.make_body()
							print(SUBJECT)
							self.sendMail(SUBJECT, body, TO)
							time.sleep(600)


					except:
						driver.save_screenshot("screenshot.png")
						time.sleep(5)
						body = self.make_body()
						print(SUBJECT)
						self.sendMail(SUBJECT, body, TO)
						time.sleep(600)

				except:
					print("Impossible de charger la page")
			except:
				print("error inconnue")
				continue

			print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
			driver.close()
			time.sleep(600)



if __name__ == '__main__':

	prefecture = Prefecture()
	prefecture.updateSelenium("[Prefecture !] Il existe une plage horaire Etudiant", ["emailtosend1@gmail.com","emailtosend2@gmail.com"])