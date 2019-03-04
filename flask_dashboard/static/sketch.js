// Daniel Shiffman
// http://codingtra.in
// http://patreon.com/codingtrain
// Code for: https://youtu.be/NcewaPfFR6Y

var canvas;
var score;
var button;
var initialInput;
var submitButton;
var database;

function setup() {
  canvas = createCanvas(100, 100);
  canvas.parent('game');
  score = 0;
  createP('Click the button to get points.').parent('game');
  button = createButton('click');
  button.mousePressed(increaseScore);
  button.parent('game');
  initialInput = createInput('initials');
  initialInput.parent('game');
  submitButton = createButton('submit');
  submitButton.parent('game');
  submitButton.mousePressed(submitScore);

  var config = {
    apiKey: "AIzaSyCYAqcsSlHPGJoK9zoIndRnMAr6CEm6A6w",
    authDomain: "haha-4cf04.firebaseapp.com",
    databaseURL: "https://haha-4cf04.firebaseio.com",
    projectId: "haha-4cf04",
    storageBucket: "haha-4cf04.appspot.com",
    messagingSenderId: "978160165048"
  };
  firebase.initializeApp(config);
  database = firebase.database();

  var ref = database.ref('scores');
  ref.on('value', gotData, errData);
}

function gotData(data) {

  var scorelistings = selectAll('.scorelisting');
  for (var i = 0; i < scorelistings.length; i++) {
    scorelistings[i].remove();
  }

  //console.log(data.val());
  var scores = data.val();
  var keys = Object.keys(scores);
  //console.log(keys);
  for (var i = 0; i < keys.length; i++) {
    var k = keys[i];
    var initials = scores[k].date;
    var score = scores[k].time;
    var s = scores[k].co;
    //console.log(initials, score);
    var li = createElement('li', initials);
    li.class('scorelisting');
    li.parent('scorelist');
  }
}

function errData(err) {
  console.log('Error!');
  console.log(err);
}


function submitScore() {
  var data = {
    initials: initialInput.value(),
    score: score
  }
  console.log(data);
  var ref = database.ref('scores');
  var result = ref.push(data);
  console.log(result.key);
}

function increaseScore() {
  score++;
}

function draw() {
  background(0);
  textAlign(CENTER);
  textSize(32);
  fill(255);
  text(score, width / 2, height / 2);
}