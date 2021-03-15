import os

# 图片验证码Redis有效期， 单位：秒
IMAGE_CODE_REDIS_EXPIRES = 300

UPLOAD_FOLDER = os.getcwd() + '/app/static/upload/'

QINIU_DOMIN_PREFIX = "https://image.holyzq.com/"
ACCESS_KET = 'fAotwAkyCf3pp-v7lx9katOiZiwYE6KCHyy7fWg4'
SECRET_KEY = 'dkCY3RGS3ZXK4KS464JZKg17826-vZPQ7zwn2dp2'
BUCKET_NAME = 'huangdj'
