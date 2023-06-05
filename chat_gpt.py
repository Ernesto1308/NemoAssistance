import openai

from mqtt_provider import *
from utils import time

openai.organization = "org-cGnbTKlS8VbEwWTAIQzkw0xi"
openai.api_key = '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'


def on_message(client, userdata, message):
    text_input = message.payload.decode('utf-8')
    print('Solicitud enviada', time())
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text_input,
        max_tokens=2048,
        temperature=0
    )
    print('Respuesta recibida', time())
    response_split = response['choices'][0]['text'].strip()
    answer = ''.join(response_split)
    mqtt_publish = MqttPublisher('localhost', 'GPT Module Output', 'audio/chat_gpt_output')
    mqtt_publish.publish(answer)


mqtt_subscribe = MqttSubscriber('localhost', 'GPT Module Input', 'audio/chat_gpt_input')
mqtt_subscribe.client.on_message = on_message
mqtt_subscribe.subscribe()
