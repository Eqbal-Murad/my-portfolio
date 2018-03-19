import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')

    topic = sns.Topic('arn:aws:sns:us-east-1:084610447019:deployPortfolioTopic')
    portfolio_bucket = s3.Bucket('about.eqbalmurad.com')
    build_bucket = s3.Bucket('portfolio-build.eqbalmurad.com')
    try:
        portfolip_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolip_zip)

        with zipfile.ZipFile(portfolip_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
            # TODO implement
        topic.publish(Subject="Portfolio deployed",Message="Portfolio deployed sucessfully")
    except:
        topic.publish(Subject="Portfolio deploy failed",Message="Portfolio deployment failed")
        raise
    return 'Porfolio deployed by Lambda'
