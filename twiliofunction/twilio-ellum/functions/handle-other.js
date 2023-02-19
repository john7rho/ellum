const VoiceResponse = require('twilio').twiml.VoiceResponse;

const voiceConfig = {
  voice: "Polly.Amy-Neural"
}

const supportedLanguages = ['german', 'french', 'japanese'];

exports.handler = function(context, event, callback) {
  const twiml = new VoiceResponse();
  
  const gather = twiml.gather({
    input: 'speech',
    action: '/handle-language',
    speechTimeout: 1
});

  callback(null, twiml);
};