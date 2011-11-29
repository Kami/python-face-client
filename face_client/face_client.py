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
""" Module for interfacing with face.com rest API """

import urllib
import urllib2
import os
import json
import logging

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
register_openers()

LOGGER_FACE = logging.getLogger("face_client")
LOGGER_FACE.setLevel(logging.WARNING)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

COMMA_OUTPUT = (lambda d : 
					  unicode(",".join(
					  ["{}:{}".format(k, v) for k,v in d.iteritems()])))

GET_USER_IDS = (lambda uids, domain:
				[uid for uid in uids.split(',') if uid.find(domain) != -1])

GET_FACEBOOK_USER_IDS = (lambda uids:
						 GET_USER_IDS(uids,'@facebook.com'))

GET_TWITTER_USER_IDS = (lambda uids:
						 GET_USER_IDS(uids,'@twitter.com'))

def set_log_level(level):
	""" sets the module logging level """
	LOGGER_FACE.setLevel(level)

class FaceClient(object):
	""" This is the main interface class. Its methods represent the 
		current face.com API and the encapsulated data is the facebook
		and twitter credentials information
	"""
	def __init__(self, api_key, api_secret, response_format='json', ssl=True):
		""" api_key: face.com provided api key
			api_secret: face.com provided api secret
			response_format: json | xml
			ssl: True | False
		"""
		self._key = api_key
		self._secret = api_secret
		self._format = response_format

		self._credentials = {"facebook": {}, "twitter": {}}
		self._ssl = ssl
		self._apiurl = "api.face.com"

	def set_twitter_oauth_credentials(self, user, secret, token):
		""" user - twitter user id
			secret - twitter oauth secret
			token - twitter oauth token
		"""
		self._credentials["twitter"].update({'user': user,
											 'secret': secret, 
											 'token': token})

	def set_facebook_oauth_credentials(self, user, token):
		""" user - facebook user id
			token - facebook oauth2 token
		"""
		self._credentials["facebook"].update({'user': user, 'token': token})

	def faces_detect(self, urls=None, file_name=None, aggressive=False):
		"""
		Returns tags for detected faces in one or more photos, with geometric
		information of the tag, eyes, nose and mouth, as well as the gender,
		glasses, and smiling attributes.

		http://developers.face.com/docs/api/faces-detect/
		"""
		if file_name:
			# Check if the file exists
			if not os.path.exists(file_name):
				raise IOError('File %s does not exist' % (file_name))

			data = {'file': file_name}
		else:
			data = {'urls': urls}

		if aggressive:
			data['detector'] = 'Aggressive'

		data['attributes'] = 'all'
		self._base_data(data)
		return self._wrap_send('faces/detect', data)

	def faces_status(self, uids, **kwargs):
		"""
		Reports training set status for the specified UIDs.

		http://developers.face.com/docs/api/faces-status/
		"""
		data = {'uids': uids}
		self._base_data(data, **kwargs)
		return self._wrap_send('faces/status', data)

	def faces_recognize(self, uids, urls=None, file_name=None, **kwargs):
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

		if file_name:
			# Check if the file exists
			if not os.path.exists(file_name):
				raise IOError('File %s does not exist' % (file_name))

			data.update({'file': file_name})
		else:
			data.update({'urls': urls})

		self._base_data(data, **kwargs)
		return self._wrap_send('faces/recognize', data)

	def faces_train(self, uids, **kwargs):
		"""
		Calls the training procedure for the specified UIDs, and reports back
		changes.

		http://developers.face.com/docs/api/faces-train/
		"""
		data = {'uids': uids}
		self._base_data(data, callback_url="no-reply", **kwargs)
		return self._wrap_send('faces/train', data)

	### Methods for managing face tags ###
	def tags_get(self, uids=None, urls=None, 
				 limit=5, together=False, **kwargs):
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

		self._base_data(data, **kwargs)
		return self._wrap_send('tags/get', data)

	def tags_add(self, url, face_x, face_y, width, uid, tagger_id, **kwargs):
		"""
		Add a (manual) face tag to a photo. Use this method to add face tags
		where those were not detected for completeness of your service.

		http://developers.face.com/docs/api/tags-add/
		"""
		data = {'url': url,
				'x': face_x,
				'y': face_y,
				'width': width,
				'uid': uid,
				'tagger_id': tagger_id}
		self._base_data(data, **kwargs)
		return self._wrap_send('tags/add', data)

	def tags_save(self, tids, uid, **kwargs):
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
		
		self._base_data(data, **kwargs)
		return self._wrap_send('tags/save', data)

	def tags_remove(self, tids, **kwargs):
		"""
		Remove a previously saved face tag from a photo.

		kwargs:
			password - 
		http://developers.face.com/docs/api/tags-remove/
		"""
		data = {'tids': tids}
		self._base_data(data, **kwargs)
		return self._wrap_send('tags/remove', data)

	### Account management methods ###
	def account_limits(self):
		"""
		Returns current rate limits for the account represented by the passed
		API key and Secret.

		http://developers.face.com/docs/api/account-limits/
		"""
		return self._wrap_send('account/limits', {})

	def account_users(self, namespaces):
		"""
		Returns current rate limits for the account represented by the passed
		API key and Secret.
		
		namespaces - comma separated list of one or more private namespaces

		http://api.face.com/account/users.format
		"""
		return self._wrap_send('account/users', {'namespaces': namespaces})

	def _base_data(self, data, **kwargs):
		""" adds standard parameters to data argument like twitter & 
			facebook credentials plus any optional kwargs parameters.
		"""
		self._append_credentials(data, self._has_facebook_credentials(), 
								 self._has_twitter_credentials())
		self._append_optional_params(data, **kwargs)
	
	def _wrap_send(self, method, data):
		""" logs request and response data from face.com API """
		LOGGER_FACE.debug("'{}' sending {}'".format(method, data))
		response = self._send_request(method, data)
		LOGGER_FACE.debug("'{}' received response was '{}'".format(method, 
																   response))
		return response
	
	def _has_facebook_credentials(self):
		""" returns True if client has facebook oauth creds """
		return True if len(self._credentials["facebook"]) else False
	
	def _has_twitter_credentials(self):
		""" returns True if client has twitter oauth creds """
		return True if len(self._credentials["twitter"]) else False

	def _get_facebook_credentials(self):
		""" returns encapsulated facebook oauth creds if present """
		f_b = {}
		if self._has_facebook_credentials():
			f_b["fb_user"] = self._credentials["facebook"]["user"]
			f_b["fb_oauth_token"] = self._credentials["facebook"]["token"]
		return f_b
	
	def _get_twitter_credentials(self):
		""" returns encapsulated twitter oauth creds if present """
		t_w = {}
		if self._has_twitter_credentials():
			t_w["twitter_oauth_user"] = self._credentials["twitter"]["user"]
			t_w["twitter_oauth_secret"] = self._credentials["twitter"]["secret"]
			t_w["twitter_oauth_token"] = self._credentials["twitter"]["token"]
		return t_w
	
	def _add_facebook_credentials(self, data):
		""" appends facebook creds to the data dictionary """
		data.update({"user_auth":
					 COMMA_OUTPUT(self._get_facebook_credentials())})
			  
	def _add_twitter_credentials(self, data):
		""" appends twitter creds to the data dictionary """
		data.update({"user_auth":
					 COMMA_OUTPUT(self._get_twitter_credentials())})
		
	def _append_credentials(self, data, facebook=True, twitter=True):
		""" adds either facebook or twitter oauth creds to the data package """
		if facebook:
			self._add_facebook_credentials(data)
		if twitter:
			self._add_twitter_credentials(data)

	def _append_optional_params(self, data, **kwargs):
		""" adds optional kwargs to data paramater """ 
		for key, value in kwargs.iteritems():
			if value:
				data.update({key: value})

	def _send_request(self, method=None, parameters=None):
		""" method - api method to call
			parameters - optional data parameters for method call
		"""
		if self._ssl:
			protocol = 'https://'
		else:
			protocol = 'http://'

		url = '%s%s/%s.%s' % (protocol, self._apiurl, method, self._format)

		data = {'api_key': self._key,
				'api_secret': self._secret,
				'format': self._format}

		if parameters:
			data.update(parameters)

		# Local file is provided, use multi-part form
		if 'file' in data:
			file_name = data['file']
			data['file'] = open(file_name, "rb")
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
	""" Basic exception wrapper class """
	def __init__(self, error_code, error_message, **kwargs):
		""" code & message """
		super(FaceError, self).__init__(**kwargs)
		self.error_code = error_code
		self.error_message = error_message

	def __str__(self):
		return '%s (%d)' % (self.error_message, self.error_code)
