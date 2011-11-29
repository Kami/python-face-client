EXAMPLE
=======

Here is a short example demonstrating how you can use this client.

Lets say that we want to create our own private namespace and train it to recognize Guido Van Rossum.

Here are the images which we will use for training our namespace index:

| http://savasplace.com/wp-content/uploads/2009/04/guido-van-rossum.jpg
| http://farm1.static.flickr.com/43/104506247_c748f20b83.jpg
| http://farm1.static.flickr.com/67/200126290_2798330e61.jpg

And here is the image which hopefully, after training our index will be recognized as "Guido Van Rossum":

http://farm1.static.flickr.com/41/104498903_bad315cee0.jpg

#. First we create our private namespace named **testns** (this can be done on the `face.com page`_)

#. Now we import the module and instantiate the class with our face.com **api_key** and **api_secret** (you can get them by registering your application on `face.com page`_)::

    >> import face_client
    >> client = face.FaceClient('API_KEY', 'API_SECRET')

#. Before training our namespace index I just want to show you that the image is not already recognized::

    >> client.faces_recognize('guido', 'http://farm1.static.flickr.com/41/104498903_bad315cee0.jpg', namespace = 'testns')

    {u'no_training_set': [u'guido@testns'],
    u'photos': [{u'height': 375,
                         ...omitted for clarity...
                         u'tid': u'TEMP_F@51b67ae268617da2c99c69091ab8f3b0_cf224a584e806722a7fa15a936ed1367_48.00_41.82_0',
                         u'uids': [],
                         u'width': 47,
                         u'yaw': 31.649999999999999}],
                  u'url': u'http://farm1.static.flickr.com/41/104498903_bad315cee0.jpg',
                  u'width': 500}],
                         ...omitted for clarity...

   As you can see, the "uids" list is empty, meaning that Guido Van Rossum is not yet recognized in our **testns** namespace.

#. Saving the tags and training our index

   For saving the tags, we need to provide the **tags_save** method with the tag ids, which we can obtain by using the **faces_detect** or **faces_recognize** method.

   In this example, I will use faces_detect::

    >> response = client.facesDetect('http://savasplace.com/wp-content/uploads/2009/04/guido-van-rossum.jpg,http://farm1.static.flickr.com/43/104506247_c748f20b83.jpg,http://farm1.static.flickr.com/67/200126290_2798330e61.jpg')
    >> tids = [photo['tags'][0]['tid'] for photo in response['photos']]

    >> tids

    [u'TEMP_F@cc96b0429a7946711de5693c5ff67c46_cf224a584e80672ea7fa15a936ed1367_47.00_27.83_0',
    u'TEMP_F@e2ee88f20076bc1a60c3629281f34197_cf224a584e80672ea7fa15a936ed1367_48.00_34.93_0',
    u'TEMP_F@33c91a546bbba775628e7d7ca969f7ce_cf224a584e80672ea7fa15a936ed1367_48.35_26.40_0']

   We can also check that the tags were saved by using the **tags_get** method::

    >> client.tags_get('guido@testns')

    {u'message': u'Tags saved with uid: guido@testns ,label: Guido Van Rossum',
     u'saved_tags': [{u'detected_tid': u'TEMP_F@cc96b0429a7946711de5693c5ff67c46_cf224a584e80672ea7fa15a936ed1367_47.00_27.83_0',
                  u'tid': u'21319_cf224a584e80672ea7fa15a936ed1367'},
                 {u'detected_tid': u'TEMP_F@e2ee88f20076bc1a60c3629281f34197_cf224a584e80672ea7fa15a936ed1367_48.00_34.93_0',
                  u'tid': u'21321_cf224a584e80672ea7fa15a936ed1367'},
                 {u'detected_tid': u'TEMP_F@33c91a546bbba775628e7d7ca969f7ce_cf224a584e80672ea7fa15a936ed1367_48.35_26.40_0',
                 u'tid': u'21323_cf224a584e80672ea7fa15a936ed1367'}],
     u'status': u'success'}

#. Now when we have the temporary tag ids, we can use them save to save the tags and train our namespace index::

    >> client.tags_save(tids = ',' . join(tids), uid = 'guido@testns', label = 'Guido Van Rossum')
    >> client.faces_train('guido@testns')

    {u'status': u'success',
    u'unchanged': [{u'last_trained': 1274462404,
                 u'training_in_progress': False,
                 u'training_set_size': 3,
                 u'uid': u'guido@testns'}]}

#. Now after we have trained our index, lets check if Guido is recognized::

    >> client.faces_recognize('all', 'http://farm1.static.flickr.com/41/104498903_bad315cee0.jpg', namespace = 'testns')

    {u'photos': [{u'height': 375,
              u'pid': u'F@2981c22e78cc0f12276825aa0b05df86_cf224a584e80672ea7fa15a936ed1367',
                         ...omitted for clarity...
                         u'roll': -1.3400000000000001,
                         u'tagger_id': None,
                         u'threshold': 60,
                         u'tid': u'TEMP_F@2981c22e78cc0f12276825aa0b05df86_cf224a584e80672ea7fa15a936ed1367_51.00_35.20_2',
                         u'uids': [{u'confidence': 20,
                                    u'uid': u'guido@testns'}],
                         u'width': 18.600000000000001,
                         u'yaw': 36}],
              u'url': u'http://farm1.static.flickr.com/41/104498903_bad315cee0.jpg',
              u'width': 500}],
    u'status': u'success',
                         ...omitted for clarity...

   As you can see by looking at the uids key, Guido was now recognized with a 20% confidence!

For more information about the face.com API and how to use it with Facebook and Twitter, visit the `official documentation`_.

.. _face.com page: http://developers.face.com/account/
.. _official documentation: http://developers.face.com/docs/recognition-howto/
