const VoiceResponse = require('twilio').twiml.VoiceResponse;
const axios = require('axios');



exports.handler = async function(context, event, callback) {
  const twiml = new VoiceResponse();
  const speech = event.SpeechResult;
  console.log(speech);
  
  const newSpeech = (s) => {
    let res = "";
    for (let i = 0; i < s.length; i++) {
        if (s.charAt(i).toLowerCase().match(/[a-z]/i)) {
            res += s.charAt(i).toLowerCase()
        }
        else if (s.charAt(i) == " " && res[res.length - 1] != "+") {
            res += "+"
        }
    }
    res.replace(" ", "+")
    return res;
  };
try {
    
    let output = await axios.get('https://adityarai10101--vectordbqaadi-queryreal.modal.run/?x=' + newSpeech(speech));
    if(output == " I don't know.") {
        twiml.say("I don't quite know the answer to that. Let me put in a support ticket for you.")
    }
    else {
        twiml.say(output.data);
    }
    
}
catch {
    twiml.say("I didnt quite get that. Could you please repeat it?")
}

    twiml.redirect('/handle-other');

  callback(null, twiml);
};
