var initRequest = '{"change":"Add", "interactions":[[1,1], [1,2], [2,0], [2,1], [2,3], [3,1], [3,3]]}';

document.getElementById("initialize").onclick = userItemInitialPrint;

function userItemInitialPrint() {
  document.getElementById("requestInfo").innerHTML = initRequest;
  socket.send(initRequest);

  var userItemMat = JSON.parse(initRequest);
  var userItemInfo = userItemMat["interactions"];
    
  userItemInfo.forEach(element => {
    var row = element[0];
    var col = element[1];
    document.getElementById("interaction_matrix_" + row + "_" + col).innerHTML = 1;    
  });

  document.getElementById("initialize").disabled=true;
}

var socket = new WebSocket("ws://" + window.location.host + "/ws");
socket.onmessage = function (event) {
  var requestInfo = document.getElementById("requestInfo").innerHTML;
  var action = JSON.parse(requestInfo);

  var messages = document.getElementById("messages");
  messages.append(event.data + "\n");

  var change = JSON.parse(event.data);

  if (change['data'] == 'item_interactions_n' && change['change'] == 1) {
    var item = change['item'];
    var count = change['count'];
    document.getElementById("interactions_per_item_" + item).innerHTML = count;
  }

  if (action['change'] == 'Remove' && change['data'] == 'item_interactions_n' && change['change'] == -1 && change['count'] == 1) {
    var item = change['item'];
    document.getElementById("interactions_per_item_" + item).innerHTML = 0;
    for (i = 0; i < 4; i++){
      document.getElementById("cooccurrences_" + item + "_" + i).innerHTML = 0;
      document.getElementById("cooccurrences_" + i + "_" + item).innerHTML = 0;
      document.getElementById("similarities_" + item + "_" + i).innerHTML = 0;
      document.getElementById("similarities_" + i + "_" + item).innerHTML = 0;
    }
    document.getElementById("cooccurrences_" + item + "_" + item).innerHTML = '-';
    document.getElementById("similarities_" + item + "_" + item).innerHTML = '-';
  }


  if (change['data'] == 'cooccurrences_c' && change['change'] == 1) {
    var item_a = change['item_a'];
    var item_b = change['item_b'];
    var count = change['num_cooccurrences'];
    document.getElementById("cooccurrences_" + item_a + "_" + item_b).innerHTML = count;
    document.getElementById("cooccurrences_" + item_b + "_" + item_a).innerHTML = count;
  }

  if (change['data'] == 'similarities_s' && change['change'] == 1) {
    var item_a = change['item_a'];
    var item_b = change['item_b'];
    var similarity = change['similarity'];
    document.getElementById("similarities_" + item_a + "_" + item_b).innerHTML = Number(similarity).toFixed(2);
    document.getElementById("similarities_" + item_b + "_" + item_a).innerHTML = Number(similarity).toFixed(2);
  }

};

var form = document.getElementById("form");
form.addEventListener('submit', function (event) {
  event.preventDefault();
  var input = document.getElementById("msg");
  socket.send(input.value);

  document.getElementById("requestInfo").innerHTML = input.value;

  var inputDict = JSON.parse(input.value);
  var inputInfo = inputDict["interactions"];

  if (inputDict['change'] == 'Remove') {
      var userId = inputInfo[0][0];
      let removeUserElement = document.getElementById('user' + userId);
      removeUserElement.parentElement.removeChild(removeUserElement);
    }

  if (inputDict['change'] == 'Add') {
      var userId = inputInfo[0][0];
      let newUser = document.createElement("tr");
      newUser.id = "user" + userId;
      document.getElementById("user-item-value").appendChild(newUser);

      let newUserTh = document.createElement("th");
      newUserTh.innerHTML = "User" + userId;
      newUserTh.scope = 'row';
      document.getElementById("user" + userId).appendChild(newUserTh);

      for (i = 0; i < 4; i++){
        let newUserItem = document.createElement("td");
        newUserItem.id = "interaction_matrix_" + userId + "_" + i;
        newUserItem.className = "user-item-interactions";
        newUserItem.innerHTML = 0;
        document.getElementById("user" + userId).appendChild(newUserItem);
      }

      inputInfo.forEach(element => {
        var row = element[0];
        var col = element[1];
        document.getElementById("interaction_matrix_" + row + "_" + col).innerHTML = 1;
      });
  }

  input.value = "";

});

var addForm = document.getElementById("addForm");
addForm.addEventListener('submit', function (event) {
  event.preventDefault();
  var newUserId = document.getElementById("addNewUserId").value;
  var newItemId = document.getElementById("addNewItemId").value;
  ItemArray = newItemId.split(',').map(Number);
  var interactionList = [];
  for (i = 0; i < ItemArray.length; i++){
    interactionList.push([Number(newUserId), ItemArray[i]]);
  }

  var addRequest = {"change": "Add"};
  addRequest["interactions"] = interactionList;

  document.getElementById("requestInfo").innerHTML = JSON.stringify(addRequest);

  socket.send(JSON.stringify(addRequest));

  var inputDict = JSON.parse(JSON.stringify(addRequest));
  var inputInfo = inputDict["interactions"];

  var userId = inputInfo[0][0];
  let newUser = document.createElement("tr");
  newUser.id = "user" + userId;
  document.getElementById("user-item-value").appendChild(newUser);

  let newUserTh = document.createElement("th");
  newUserTh.innerHTML = "User" + userId;
  newUserTh.scope = 'row';
  document.getElementById("user" + userId).appendChild(newUserTh);

  for (i = 0; i < 4; i++){
    let newUserItem = document.createElement("td");
    newUserItem.id = "interaction_matrix_" + userId + "_" + i;
    newUserItem.className = "user-item-interactions";
    newUserItem.innerHTML = 0;
    document.getElementById("user" + userId).appendChild(newUserItem);
   }
   
  inputInfo.forEach(element => {
    var row = element[0];
    var col = element[1];
    document.getElementById("interaction_matrix_" + row + "_" + col).innerHTML = 1;
  });
});

var removeForm = document.getElementById("removeForm");
removeForm.addEventListener('submit', function (event) {
  event.preventDefault();
  var removeUserId = document.getElementById("removeUserId").value;
  var interactionList = [];

  for (i = 0; i < 4; i++){
    if (document.getElementById("interaction_matrix_" + removeUserId +"_" + i).innerHTML == '1'){
        interactionList.push([Number(removeUserId), i]);
    }
  }

  var removeRequest = {"change": "Remove"};
  removeRequest["interactions"] = interactionList;
  document.getElementById("requestInfo").innerHTML = JSON.stringify(removeRequest);

  socket.send(JSON.stringify(removeRequest));
  
  let removeUserElement = document.getElementById('user' + removeUserId);
  removeUserElement.parentElement.removeChild(removeUserElement);

});