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
    speechTimeout: 0.5,
    enhanced: "true",
    speechModel: "phone_call",
    timeout: 8

});

  gather.say(voiceConfig, "Hi! This is Ella. How can I help?");

//   supportedLanguages.forEach((language, index) => {
//     gather.say(voiceConfig, `Select ${index + 1} to translate to ${language}`);
//   });

  callback(null, twiml);
};