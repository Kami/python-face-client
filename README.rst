SkyBiometry Face Detection and Recognition API client library
=============================================================

SkyBiometry Face Detection and Recognition REST API client library.

For more information about the API and the return values, visit the `official documentation`_.

Example
-------

Here is a short example demonstrating how you can use this client.

Lets say that we want to create our own private namespace and train it to recognize Guido Van Rossum.

Here are the images which we will use for training our namespace index:

| http://savasplace.com/wp-content/uploads/2009/04/guido-van-rossum.jpg
| http://farm1.static.flickr.com/43/104506247_c748f20b83.jpg
| http://farm1.static.flickr.com/67/200126290_2798330e61.jpg

And here is the image which hopefully, after training our index will be recognized as "Guido Van Rossum":

http://farm1.static.flickr.com/41/104498903_bad315cee0.jpg

#. First we create our private namespace named **testns** (this can be done on the `SkyBiometry page`_).

#. Now we import the module and instantiate the class with our SkyBiometry **API_KEY** and **API_SECRET** (you can get them by registering your application on `SkyBiometry page`_)::

    >> from face_client import FaceClient
    >> client = FaceClient('API_KEY', 'API_SECRET')

#. Before training our namespace index I just want to show you that the image is not already recognized::

    >> client.faces_recognize('guido', 'http://farm1.static.flickr.com/41/104498903_bad315cee0.jpg', namespace = 'testns')

    {
        u'status': u'success',
        u'photos': [{
            u'url': u'http://farm1.static.flickr.com/41/104498903_bad315cee0.jpg',
            u'width': 500,
            u'tags': [{
                u'eye_left': {u'y': 31.2, u'x': 55.6},
                u'confirmed': False,
                u'uids': [],
                u'yaw': -45,
                u'manual': False,
                u'height': 18.13,
                u'width': 13.6,
                u'mouth_center': {u'y': 43.47, u'x': 52.6},
                u'nose': {u'y': 36.53, u'x': 53.4},
                u'eye_right': {u'y': 30.93, u'x': 48.0},
                u'pitch': 0,
                u'tid': u'TEMP_F@08e31221350a43d267be01d500f10086_1d12ece6a6ea2_48.20_35.73_0_1',
                u'attributes': {
                    u'gender': {u'confidence': 47, u'value': u'male'},
                    u'smiling': {u'confidence': 85, u'value': u'false'},
                    u'glasses': {u'confidence': 27, u'value': u'false'},
                    u'dark_glasses': {u'confidence': 89, u'value': u'false'},
                    u'face': {u'confidence': 71, u'value': u'true'}
                },
                u'recognizable': True,
                u'roll': 3,
                u'center': {u'y': 35.73, u'x': 48.2}
            }],
            u'pid': u'F@08e31221350a43d267be01d572dc824b_1d12ece6a6ea2',
            u'height': 375
        }],
        u'usage': {...omitted for clarity...}
    }

   As you can see, the "uids" list is empty, meaning that Guido Van Rossum is not yet recognized in our **testns** namespace.

#. Saving the tags and training our index. For saving the tags, we need to provide the **tags_save** method with the tag ids, which we are obtained by using the **faces_detect** or **faces_recognize** method. In this example, I will use **faces_detect**::

    >> response = client.faces_detect('http://savasplace.com/wp-content/uploads/2009/04/guido-van-rossum.jpg,http://farm1.static.flickr.com/43/104506247_c748f20b83.jpg,http://farm1.static.flickr.com/67/200126290_2798330e61.jpg')
    >> tids = [photo['tags'][0]['tid'] for photo in response['photos']]
    >> tids

    [
        u'TEMP_F@0bf0294f6c43162105c9bdfa00bc00ab_15e78870a332a_47.00_28.50_0_1',
        u'TEMP_F@008f7f3d4f93956f2fd24b1e01000084_e29f2ba8f58c6_51.20_35.20_0_1',
        u'TEMP_F@0d38a4e97c5c63042b5da6da00a10088_73a8fb3908097_48.35_27.20_0_1'
    ]

#. Now when we have the temporary tag ids, we can use them to save the tags and train our namespace index::

    >> client.tags_save(tids = ',' . join(tids), uid = 'guido@testns', label = 'Guido Van Rossum')

    {
        u'status': u'success',
        u'message': u'Tags saved with uid: guido@testns, label: Guido Van Rossum',
        u'saved_tags': [
            {u'tid': u'00bc00ab_15e78870a332a', u'detected_tid': u'TEMP_F@0bf0294f6c43162105c9bdfa00bc00ab_15e78870a332a_47.00_28.50_0_1'},
            {u'tid': u'01000084_e29f2ba8f58c6', u'detected_tid': u'TEMP_F@008f7f3d4f93956f2fd24b1e01000084_e29f2ba8f58c6_51.20_35.20_0_1'},
            {u'tid': u'00a10088_73a8fb3908097', u'detected_tid': u'TEMP_F@0d38a4e97c5c63042b5da6da00a10088_73a8fb3908097_48.35_27.20_0_1'}
        ]
    }

    >> client.faces_train('guido@testns')

    {
        u'status': u'success',
        u'created': [{
            u'training_set_size': 3,
            u'last_trained': 1361651583,
            u'uid': u'guido@testns',
            u'training_in_progress': False}
        ]
    }

#. We can also check that the tags were saved by using the **tags_get** method::

    >> client.tags_get('guido@testns')

    {
        u'status': u'success',
        u'photos': [
            {u'url': u'http://farm1.static.flickr.com/67/200126290_2798330e61.jpg', ...omitted for clarity...},
            {u'url': u'http://farm1.static.flickr.com/43/104506247_c748f20b83.jpg', ...omitted for clarity...},
            {u'url': u'http://savasplace.com/wp-content/uploads/2009/04/guido-van-rossum.jpg', ...omitted for clarity...}
        ],
        u'usage': {...omitted for clarity...}
    }

#. Now after we have trained our index, lets check if Guido is recognized::

    >> client.faces_recognize('all', 'http://farm1.static.flickr.com/41/104498903_bad315cee0.jpg', namespace = 'testns')

    {
        u'status': u'success',
        u'photos': [{
            u'url': u'http://farm1.static.flickr.com/41/104498903_bad315cee0.jpg',
            u'width': 500,
            u'tags': [{
                u'eye_left': {u'y': 31.2, u'x': 55.6},
                u'confirmed': False,
                u'uids': [{u'confidence': 34, u'uid': u'guido@testns'}],
                u'width': 13.6,
                u'yaw': -45,
                u'manual': False,
                u'height': 18.13,
                u'threshold': 30,
                u'mouth_center': {u'y': 43.47, u'x': 52.6},
                u'nose': {u'y': 36.53, u'x': 53.4},
                u'eye_right': {u'y': 30.93, u'x': 48.0},
                u'pitch': 0,
                u'tid': u'TEMP_F@08e31221350a43d267be01d500f10086_1d12ece6a6ea2_48.20_35.73_0_1',
                u'attributes': {
                    u'gender': {u'confidence': 47, u'value': u'male'},
                    u'smiling': {u'confidence': 85, u'value': u'false'},
                    u'glasses': {u'confidence': 27, u'value': u'false'},
                    u'dark_glasses': {u'confidence': 89, u'value': u'false'},
                    u'face': {u'confidence': 71, u'value': u'true'}
                },
                u'recognizable': True,
                u'roll': 3,
                u'center': {u'y': 35.73, u'x': 48.2}
            }],
            u'pid': u'F@08e31221350a43d267be01d572dc824b_1d12ece6a6ea2',
            u'height': 375
        }],
        u'usage': {...omitted for clarity...}
    }

   As you can see by looking at the "uids" list, Guido was now recognized with a 34% confidence!

For more information about the SkyBiometry Face Detection and Recognition API and how to use it, visit the `official documentation`_.

.. _SkyBiometry page: http://www.skybiometry.com/Account
.. _official documentation: http://www.skybiometry.com/Documentation
