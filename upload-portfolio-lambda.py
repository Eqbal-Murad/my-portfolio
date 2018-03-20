import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')

    location = {
        "bucketName":"portfolio-build.eqbalmurad.com",
        "objectKey" : "portfoliobuild.zip"

    }

    topic = sns.Topic('arn:aws:sns:us-east-1:084610447019:deployPortfolioTopic')
    portfolio_bucket = s3.Bucket('about.eqbalmurad.com')
    build_bucket = s3.Bucket(location["bucketName"])



    try:
        job = event.get("CodePipeline.job")
        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]
        print "Building portfolio from" + str(location)

        portfolip_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], portfolip_zip)

        with zipfile.ZipFile(portfolip_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
            # TODO implement
        topic.publish(Subject="Portfolio deployed",Message="Portfolio deployed sucessfully")

        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Portfolio deploy failed",Message="Portfolio deployment failed")
        raise
    return 'Porfolio deployed by Lambda'
