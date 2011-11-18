# -*- coding: utf-8 -*-
#
# Name: face.com Python API client library
# Description: face.com REST API Python client library.
#
# For more information about the API and the return values,
# visit the official documentation at http://developers.face.com/docs/api/.
#
# Rewrite: Chris Piekarski (http://www.cpiekarski.com)
# License: BSD


import urllib
import urllib2
import os
import json
import logging

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
register_openers()

logger = logging.getLogger("face")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

def setLogLevel(level):
    logger.setLevel(level)

class FaceClient(object):
    def __init__(self, apiKey, apiSecret, responseformat='json', ssl=True):
        self._key = apiKey
        self._secret = apiSecret
        self._format = responseformat

        self._credentials = {"facebook": {}, "twitter": {}}
        self._ssl = True
        self._apiurl = "api.face.com"
        
        self._formatInput = lambda m, r :"'{}' received response was '{}'".format(m,r)
        self._formatOutput = lambda m, d : "'{}' sending {}'".format(m,d)
        self._commaOutput = lambda d : unicode(",".join(["{}:{}".format(k,v) for k,v in d.iteritems()]))

    def twitterCredentials(self, user, secret,token):
        """ user - twitter user id
            secret - twitter oauth secret
            token - twitter oauth token
        """
        self._credentials["twitter"].update({'user': user,'secret': secret, 'token': token})

    def facebookCredentials(self, user, token):
        """ user - facebook user id
            token - facebook oauth2 token
        """
        self._credentials["facebook"].update({'user': user,'token': token})

    def facesDetect(self, urls=None, fileName=None, aggressive=False):
        """
        Returns tags for detected faces in one or more photos, with geometric
        information of the tag, eyes, nose and mouth, as well as the gender,
        glasses, and smiling attributes.

        http://developers.face.com/docs/api/faces-detect/
        """
        if fileName:
            # Check if the file exists
            if not os.path.exists(fileName):
                raise IOError('File %s does not exist' % (fileName))

            data = {'file': fileName}
        else:
            data = {'urls': urls}

        if aggressive:
            data['detector'] = 'Aggressive'

        data['attributes'] = 'all'
        self._baseData(data)
        return self._wrapSend('faces/detect', data)

    def facesStatus(self, uids, **kwargs):
        """
        Reports training set status for the specified UIDs.

        http://developers.face.com/docs/api/faces-status/
        """
        data = {'uids': uids}
        self._baseData(data, **kwargs)
        return self._wrapSend('faces/status', data)

    def facesRecognize(self, uids, urls=None, fileName=None, **kwargs):
        """
        Attempts to detect and recognize one or more user IDs' faces, in one
        or more photos.
        For each detected face, the face.com engine will return the most likely
        user IDs, or empty result for unrecognized faces. In addition, each
        tag includes a threshold score - any score below this number is
        considered a low-probability hit.

        http://developers.face.com/docs/api/faces-recognize/
        """
        data = {'uids': uids, 'attributes': 'all'}

        if fileName:
            # Check if the file exists
            if not os.path.exists(fileName):
                raise IOError('File %s does not exist' % (fileName))

            data.update({'file': fileName})
        else:
            data.update({'urls': urls})

        self._baseData(data, **kwargs)
        return self._wrapSend('faces/recognize', data)

    def facesTrain(self, uids, **kwargs):
        """
        Calls the training procedure for the specified UIDs, and reports back
        changes.

        http://developers.face.com/docs/api/faces-train/
        """
        data = {'uids': uids}
        self._baseData(data, callback_url="no-reply", **kwargs)
        return self._wrapSend('faces/train', data)

    ### Methods for managing face tags ###
    def tagsGet(self, uids=None, urls=None, order='recent',limit=5, together=False, **kwargs):
        """
        Returns saved tags in one or more photos, or for the specified
        User ID(s).
        This method also accepts multiple filters for finding tags
        corresponding to a more specific criteria such as front-facing,
        recent, or where two or more users appear together in same photos.
        
        kwargs:
            pids=None,filter=None, namespace=None

        http://developers.face.com/docs/api/tags-get/
        """
        data = {'uids': uids,
                'urls': urls,
                'together': together,
                'limit': limit}

        self._baseData(data, **kwargs)
        return self._wrapSend('tags/get', data)

    def tagsAdd(self, url, x, y, width, uid,tagger_id, **kwargs):
        """
        Add a (manual) face tag to a photo. Use this method to add face tags
        where those were not detected for completeness of your service.

        http://developers.face.com/docs/api/tags-add/
        """
        data = {'url': url,
                'x': x,
                'y': y,
                'width': width,
                'uid': uid,
                'tagger_id': tagger_id}
        self._baseData(data, **kwargs)
        return self._wrapSend('tags/add', data)

    def tagsSave(self, tids, uid, **kwargs):
        """
        Saves a face tag. Use this method to save tags for training the
        face.com index, or for future use of the faces.detect and tags.get
        methods.
        
        tids - one or more tag ids to associate with the passed uid. 
               The tag id is a reference field in the response of faces.detect and faces.recognize methods
        uid  - the user ID of the user being tagged
        kwargs:        
            label - the display name of the user (usually First and Last name)
            tagger_id - the ID of the user who's adding the tag
            password - for use when saving tags is a privileged action in your client-side application

        http://developers.face.com/docs/api/tags-save/
        """
        data = {'tids': tids,
                'uid': uid }
        
        self._baseData(data, **kwargs)
        return self._wrapSend('tags/save', data)

    def tagsRemove(self, tids, **kwargs):
        """
        Remove a previously saved face tag from a photo.

        kwargs:
            password - 
        http://developers.face.com/docs/api/tags-remove/
        """
        data = {'tids': tids}
        self._baseData(data, **kwargs)
        return self._wrapSend('tags/remove', data)

    ### Account management methods ###
    def accountLimits(self):
        """
        Returns current rate limits for the account represented by the passed
        API key and Secret.

        http://developers.face.com/docs/api/account-limits/
        """
        return self._wrapSend('account/limits', {})

    def accountUsers(self, namespaces):
        """
        Returns current rate limits for the account represented by the passed
        API key and Secret.
        
        namespaces - comma separated list of one or more private namespaces

        http://api.face.com/account/users.format
        """
        return self._wrapSend('account/users', {'namespaces': namespaces})

    def _baseData(self, data, **kwargs):
        """ adds standard parameters to data argument like twitter & 
            facebook credentials plus any optional kwargs parameters.
        """
        self._appendCredentials(data, self._hasFacebookCredentials(), self._hasTwitterCredentials())
        self._appendOptionalParams(data, **kwargs)
    
    def _wrapSend(self, method, data):
        logger.debug(self._formatOutput(method,data))
        response = self._sendRequest(method, data)
        logger.debug(self._formatInput(method,response))
        return response
    
    def _hasFacebookCredentials(self):
        return True if len(self._credentials["facebook"]) else False
    
    def _hasTwitterCredentials(self):
        return True if len(self._credentials["twitter"]) else False

    def _getUserIDs(self, uids, domain):
        return [uid for uid in uids.split(',') if uid.find(domain) != -1]

    def _getFacebookUserIDs(self, uids):
        return self._getUserIDs(uids,'@facebook.com')
    
    def _getTwitterUserIDs(self, uids):
        return self._getUserIDs(uids,'@twitter.com')

    def _getFacebookCredentials(self):
        fb = {}
        if self._hasFacebookCredentials():
            fb["fb_user"] = self._credentials["facebook"]["user"]
            fb["fb_oauth_token"] = self._credentials["facebook"]["token"]
        return fb
    
    def _getTwitterCredentials(self):
        tweet = {}
        if self._hasTwitterCredentials():
            tweet["twitter_oauth_user"] = self._credentials["twitter"]["user"]
            tweet["twitter_oauth_secret"] = self._credentials["twitter"]["secret"]
            tweet["twitter_oauth_token"] = self._credentials["twitter"]["token"]
        return tweet
    
    def _addFacebookCredentials(self, data):
        data.update({"user_auth":self._commaOutput(self._getFacebookCredentials())})
              
    def _addTwitterCredentials(self, data):
        data.update({"user_auth":self._commaOutput(self._getTwitterCredentials())})
        
    def _appendCredentials(self, data, facebook=True, twitter=True):
        if facebook:
            self._addFacebookCredentials(data)
        if twitter:
            self._addTwitterCredentials(data)

    def _appendOptionalParams(self, data, **kwargs):
        for key, value in kwargs.iteritems():
            if value:
                data.update({key: value})

    def _sendRequest(self, method=None, parameters=None):
        """ method - api method to call
            parameters - optional data parameters for method call
        """
        if self._ssl:
            protocol = 'https://'
        else:
            protocol = 'http://'

        url = '%s%s/%s.%s' % (protocol, self._apiurl, method,self._format)

        data = {'api_key': self._key,
                'api_secret': self._secret,
                'format': self._format}

        if parameters:
            data.update(parameters)

        # Local file is provided, use multi-part form
        if 'file' in data:
            fileName = data['file']
            data['file'] = open(fileName, "rb")
            datagen, headers = multipart_encode(data)
        else:
            datagen = urllib.urlencode(data)
            headers = {}

        request = urllib2.Request(url, datagen, headers)
        response = urllib2.urlopen(request)
        response = response.read()
        response_data = json.loads(response)

        if 'status' in response_data and \
            response_data['status'] == 'failure':
            raise FaceError(response_data['error_code'],
                            response_data['error_message'])

        return response_data


class FaceError(Exception):
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

    def __str__(self):
        return '%s (%d)' % (self.error_message, self.error_code)
