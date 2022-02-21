from aioauth_client import HmacSha1Signature


def test_hmac_sha1_signature():
    signer = HmacSha1Signature()

    signature = signer.sign(
        consumer_secret='consumer_secret',
        method='GET',
        url='https://site.com/endpoint.json',
        oauth_token_secret='oauth_token_secret',
        escape=False,
        oauth_consumer_key='blablabla',
        oauth_nonce='blublublu',
        oauth_signature_method='HMAC-SHA1',
        oauth_timestamp='1644067741',
        oauth_version='1.0',
        tweet_mode='extended',
        oauth_token='bliblibli',
    )
    assert signature == "eqgTuU6+8g4Op1Cyu0QWk+watto="
