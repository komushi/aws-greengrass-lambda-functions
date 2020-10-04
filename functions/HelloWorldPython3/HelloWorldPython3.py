#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# HelloWorldPython3.py
# Demonstrates a simple publish to a topic using Greengrass core sdk
# This lambda function will retrieve underlying platform information and send
# a hello world message along with the platform information to the topic 'python3/hello/world'
# The function will sleep for five seconds, then repeat.  Since the function is
# long-lived it will run forever when deployed to a Greengrass core.  The handler
# will NOT be invoked in our example since the we are executing an infinite loop.
import uuid

import json
import logging
import os
import platform
from threading import Timer

# from DeepStreamDevice import device_subscribe

import greengrasssdk

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')

# Retrieving platform information to send from Greengrass Core
my_platform = platform.platform()
python_version = platform.python_version()

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# When deployed to a Greengrass core, this code will be executed immediately
# as a long-lived lambda function.  The code will enter the infinite while loop
# below.
# If you execute a 'test' on the Lambda Console, this test will fail by hitting the
# execution timeout of three seconds.  This is expected as this function never returns
# a result.

GROUP_ID = os.environ['GROUP_ID']
THING_NAME = os.environ['AWS_IOT_THING_NAME']
THING_ARN = os.environ['AWS_IOT_THING_ARN']

payload = {}
payload['group_id'] = GROUP_ID
payload['thing_name'] = THING_NAME
payload['thing_arn'] = THING_ARN

def greengrass_hello_world_run(my_topic):
    if not my_platform:
        payload['message'] = 'Hello world! Sent from Greengrass Core from Python {} {} {} {}'.format(
                python_version, GROUP_ID, THING_NAME, THING_ARN)
    else:
        payload['message'] = 'Hello world! Sent from Greengrass Core from Python {} running on platform {} {} {} {}'.format(
            python_version, my_platform, GROUP_ID, THING_NAME, THING_ARN)
    client.publish(topic=THING_NAME + '/python3/hello/world',
                   payload=json.dumps(payload))

    # logger.warning(json.dumps(payload))

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(5, greengrass_hello_world_run, kwargs={'my_topic': my_topic }).start()


# # Start executing the function above
topic=THING_NAME + '/python3/hello/world'
greengrass_hello_world_run(topic)
# device_subscribe(topic)

my_uuid = uuid.uuid4()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    logger.warning(event)
    logger.warning("my_uuid:" + str(my_uuid))
    return
