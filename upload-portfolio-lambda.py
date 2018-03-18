import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    portfolio_bucket = s3.Bucket('about.eqbalmurad.com')
    build_bucket = s3.Bucket('portfolio-build.eqbalmurad.com')

    portfolip_zip = StringIO.StringIO()
    build_bucket.download_fileobj('portfoliobuild.zip', portfolip_zip)

    with zipfile.ZipFile(portfolip_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        # TODO implement
    return 'Porfolio deployed by Lambda'
