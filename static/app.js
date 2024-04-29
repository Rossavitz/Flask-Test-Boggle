const $btn = $("#submit");
const $restart = $("#restart");
const $word = $(".word");
const $form = $("form");
const $ul = $(".words");
const $li = $("li");
const $timesPlayed = $(".timesPlayed");
let wordList = [];
let score = 0;

//show messages function, generic to be re-usable
function showMessage(msg, cls) {
  $(".msg").text(msg).removeClass().addClass(`msg ${cls}`);
}

//scoring based on length of word
function showScore(x) {
  let wordScore = x.length;
  score += wordScore;
  $(".score").text(`Your score: ${score}`);
}

//timer functionality, at 0 runs endGame function
function timer() {
  let sec = 60;
  let timer = setInterval(function () {
    $(".timer").text(`Timer: ${sec}`);
    sec -= 1;
    if (sec < 0) {
      clearInterval(timer);
      endGame();
    }
  }, 1000);
}

//event handler for button click, prevent refresh, check validity of word, reset input
$btn.click(async function (e) {
  e.preventDefault();
  check_word();
  $($form)[0].reset();
});

//Putting word values into list. If the list contains the word value, return, if it doesn't continue forward.
//Then logic to see if word is a valid word, if its a valid word but not on the board and then eventually if it is a valid word, on the board we create and append an LI
async function check_word() {
  let word = $word.val();

  if (!word) return;

  if (!wordList.includes(word)) {
    wordList.push(word);
  } else {
    showMessage("You already submitted that word");
    return;
  }

  const response = await axios.get("/result", { params: { word: word } });
  console.log(response);
  if (response.data.result === "not-word") {
    showMessage(`${word} is not a valid word`);
  } else if (response.data.result === "not-on-board") {
    showMessage(`${word} is not on this board`);
  } else {
    showMessage(`Added: ${word}`);
    function showWord($word) {
      $(".words").append($("<li>", { text: $word }));
    }
  }
  showWord(word);
  showScore(word);
}

// Hide words/functionality when game ends, display score, show restart button
async function endGame() {
  $(".words").hide();
  $(".timer").hide();
  $(".score").hide();
  $(".form").hide();
  const response = await axios.post("/end-game", { total: score });
  if (response.data.newHighScore) {
    showMessage(`New High Score: ${score}`, "ok");
  } else {
    showMessage(`Total Score: ${score}`, "ok");
  }
  $restart.show();
}

// on document load hide restart button, start timer
$(document).ready(function () {
  $restart.hide();
  timer();
});

// reload page on restart button click
$restart.click(function () {
  window.location.reload();
});
