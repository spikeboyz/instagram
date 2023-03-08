from instagram import Instagram, Params, GrantTypes

class AccessToken(Instagram):
    ENDPOINT_DEBUG = 'debug_token'
    ENDPOINT_PERMISSIONS = 'permissions'
    ENDPOINT_TOKEN = 'oauth/access_token'

    def __init__(self, config={}):
        super().__init__(config)
        self.appId = config['app_id'] if 'app_id' in config else ''
        self.appSecret = config['app_secret'] if 'app_secret' in config else ''
        self.value = config['value'] if 'value' in config else ''
        self.expiresAt = config['expires_at'] if 'expires_at' in config else 0
        self.userId = config['user_id'] if 'user_id' in config else ''

    def debug(self):
        getParams = {
            'endpoint': '/' + self.ENDPOINT_DEBUG,
            'params': {
                Params.INPUT_TOKEN: self.value
            }
        }
        response = self.get(getParams)
        return response

    def getAccessTokenFromCode(self, code, redirectUri):
        getParams = {
            'endpoint': '/' + self.ENDPOINT_TOKEN,
            'params': {
                Params.CLIENT_ID: self.appId,
                Params.CLIENT_SECRET: self.appSecret,
                Params.REDIRECT_URI: redirectUri,
                Params.CODE: code
            }
        }
        response = self.get(getParams)
        self.setDataFromResponse(response)
