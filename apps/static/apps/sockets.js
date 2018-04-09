var ws = new WebSocket("ws://" + window.location.host + "/");

ws.onmessage = function(e){
    console.log(e.data)
};

var msg = {
  stream: "questions",
  payload: {
    action: "create",
    data: {
      question_text: "What is your favorite python package?"
    },
    request_id: "some-guid"
  }
};
ws.send(JSON.stringify(msg));
// response
{
  stream: "questions",
  payload: {
    action: "create",
    data: {
      id: "1",
      question_text: "What is your favorite python package"
    }
    errors: [],
    response_status: 200
    request_id: "some-guid"
  }
}

