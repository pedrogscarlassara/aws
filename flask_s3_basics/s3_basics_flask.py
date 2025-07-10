from flask import Flask, render_template
import psutil
import boto3

session = boto3.Session(profile_name='default')
s3_client = session.client('s3')

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', value=error)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/api/list_buckets')
def list_buckets():
    counter = 0
    buckets_list = []
    try:
        buckets = s3_client.list_buckets()
        for bucket in buckets['Buckets']:
            counter += 1
            buckets_list.insert(counter, bucket['Name'])
        return buckets_list
    except Exception as error:
        return f'{error}'

@app.route('/api/list_objects/<string:name>')
def list_objects(name):
    try:
        return s3_client.list_objects_v2(Bucket=name)
    except Exception as error:
        return f'{error}'

@app.route('/api/delete_object/<string:bucket>/<string:key>')
def delete_object(bucket, key):
    try:
        return s3_client.delete_object(Bucket=bucket, Key=key)
    except Exception as error:
        return f'{error}'

app.run(debug=True, host='0.0.0.0')