from gtts import gTTS
from mqtt_provider import *
from utils import read_audio, time


def on_message(client, userdata, message):
    payload_decoded = message.payload.decode('utf-8')
    mqtt_publish = MqttPublisher('localhost', 'TextToSpeech Module Output', 'audio/text_to_speech_output')
    print('Solicitud enviada', time())
    tts = gTTS(payload_decoded, lang='es')
    tts.save('text_to_speech.wav')
    print('Respuesta recibida', time())
    mqtt_publish.publish(read_audio('text_to_speech.wav'))


mqtt_subscribe = MqttSubscriber('localhost', 'TextToSpeech Module Input', 'audio/text_to_speech_input')
mqtt_subscribe.client.on_message = on_message
mqtt_subscribe.subscribe()
