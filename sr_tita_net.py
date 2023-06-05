import nemo.collections.asr as nemo_asr
from mqtt_provider import *
from utils import write_audio, time


def on_message(client, userdata, message):
    print('Solicitud recibida', time())
    payload_decoded = eval(message.payload.decode('utf-8'))
    known_speakers_list = payload_decoded['known_speakers']
    unknown_speaker_data = payload_decoded['unknown_speaker']
    unknown_speaker = bytes(unknown_speaker_data)
    write_audio(unknown_speaker, 'unknown_speaker.wav')
    answer = False

    for speaker in known_speakers_list:
        audio = speaker['audio']['data']
        known_speaker = bytes(audio)
        write_audio(known_speaker, 'known_speaker.wav')
        answer = speaker_model.verify_speakers('known_speaker.wav', 'unknown_speaker.wav')

        if answer:
            break

    mqtt_publish = MqttPublisher('localhost', 'Verification Module Output', 'audio/verification_output')
    mqtt_publish.publish(str(answer))


speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained(model_name='titanet_large')
mqtt_subscribe = MqttSubscriber('localhost', 'Verification Module Input', 'audio/verification_input')
mqtt_subscribe.client.on_message = on_message
mqtt_subscribe.subscribe()
