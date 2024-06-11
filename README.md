# Development

Requirements

Backend

1. python3.11 +
2. See requirements.txt

Frontend

1. Javascript/ES6
2. Vuejs

Development

1. Create virtualenv inside project folder

   ```
   python3 -m venv .
   ```

2. Install requirements

   ```
   pip install -r requirements.txt
   ```

3. Run the app
   ```
   flask --app llmtool.app run --port 5002 --debug
   ```
   Should be visible in http://localhost:5002

Restarting Services for AWS Ec2 Instance

1. `sudo supervisorctl restart llm ` or ` sudo supervisorctl restart all`

This test app is hosted in AWS ec2 instance https://llm.ianrusseladem.com/

But this will not run properly as the free tier resources is not enough to run this app.

# llmtest
