from vote import app, Config
from collections import namedtuple
from flask import render_template, request, abort, send_file
import boto3

# There's only one place to get the votes, but we will need credentials...
s3 = boto3.client("s3", aws_access_key_id=Config.voting_credentials["id"], aws_secret_access_key=Config.voting_credentials["key"])

@app.route('/')
def index():
    import datetime
    today = datetime.date.today()
    year = today.year

    requested_year = request.args.get('year', year)

    # We want to paginate the s3 objects and put them in an iterator
    s3_paginator = s3.get_paginator('list_objects_v2')
    s3_iterator = s3_paginator.paginate(Bucket=Config.voting_credentials["bucket"], Prefix="Vote_Results/GA/")
    votes = []

    # Then we want to filter them for a last modify date >= the given year or the current year
    # Q: do we want a more specific search?
    filtered_iterator = s3_iterator.search(
        f"Contents[?to_string(LastModified)>='\"{requested_year}-01-01 00:00:00+00:00\"']"
    )

    for key_data in filtered_iterator:
        print(key_data)
        votes.append({"Key": key_data["Key"].split("/")[-1], "LastModified": key_data["LastModified"]})

    # Now sort what we have
    votes.sort(key=lambda x: x["LastModified"], reverse=True)


    return render_template('index.html',votes=votes)

@app.route('/file/<key>', methods=['GET'])
def get_file(key):
    vb_prefix = "Vote_Results/GA/"
    constructed_key = vb_prefix + key
    print(constructed_key)
        
    try:
        s3_file = s3.get_object(Bucket=Config.voting_credentials["bucket"], Key=constructed_key)
    except Exception as e:
        abort(500, str(e))

    return send_file(s3_file['Body'], as_attachment=False, download_name="vote.xml")