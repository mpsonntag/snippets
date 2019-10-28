$(document).ready(function () {
    var questionNumber=0;
    var questionBank=new Array();
    var stage="#game1";
    var stage2=new Object;
    var questionLock=false;
    var numberOfQuestions;
    var score=0;

    var data = {
    "quizlist":[
      {
      "question":"Was ist kein Browser",
      "option1":"Windows",
      "option2":"Firefox",
      "option3":"Opera",
      "option4":"Chrome"
      },
      {
      "question":"Was ist kein Datenformat",
      "option1":"RAM",
      "option2":"mp3",
      "option3":"XML",
      "option4":"doc"
      },
      {
      "question":"Wie heisst das Internet-Protokoll zur Übertragung von Dateien?",
      "option1":"HTTP",
      "option2":"FTP",
      "option3":"URL",
      "option4":"XML"
      },
      {
      "question":"Python wird in der Wissenschaft gerne verwendet, weil",
      "option1":"die Sprache einfach zu lernen und gratis ist",
      "option2":"es die häufigste Programmiersprache ist",
      "option3":"alle Wissenschaftler Schlangen mögen",
      "option4":"es die neueste Prgrammiersprache ist"
      },
      {
      "question":"Was ist keine Programmiersprache?",
      "option1":"ClubMate",
      "option2":"Python",
      "option3":"Java",
      "option4":"C++"
      },
      {
      "question":"Der Ausdruck 'Open Source' bezeichnet Software, die",
      "option1":"gratis verfügbar ist und verwendet werden darf",
      "option2":"unter allen herkömmlichen Betriebssystemen läuft",
      "option3":"man testen kann, bevor man kauft",
      "option4":"nicht verändert werden darf"
      },
      {
      "question":"Was ist ein Byte?",
      "option1":"eine Speichereinheit",
      "option2":"ein Internet-Explorer",
      "option3":"ein Computer",
      "option4":"eine Tierart"
      },
      {
      "question":"Wie viele Bits ergeben ein Byte?",
      "option1":"8",
      "option2":"5",
      "option3":"12",
      "option4":"16"
      },
      {
      "question":"Welches ist die kleinste Einheit?",
      "option1":"Bit",
      "option2":"Megabyte",
      "option3":"Kilobyte",
      "option4":"Byte"
      },
      {
      "question":"Was ist kein Eingabegerät am Computer?",
      "option1":"Monitor",
      "option2":"Maus",
      "option3":"Tastatur",
      "option4":"Joystick"
      },
      {
      "question":"Wofür steht die Abkürzung RAM?",
      "option1":"Random Access Memory",
      "option2":"Read Access Memory",
      "option3":"Random Address Memory",
      "option4":"Ralph Anders Mark"
      },
      {
      "question":"Worauf kann man keine Daten speichern?",
      "option1":"WLAN",
      "option2":"Festplatte",
      "option3":"USB-Stick",
      "option4":"CD"
      },
      {
      "question":"Wofür können wissenschaftliche Computermodelle verwendet werden?",
      "option1":"um eine Theorie am Computer zu testen",
      "option2":"um den Computer warm zu halten",
      "option3":"um online Geld z.B. Bitcoins zu erzeugen",
      "option4":"um berühmt zu werden"
      }
      ]
    }

    for(i=0; i<data.quizlist.length; i++){
          questionBank[i]=new Array;
          questionBank[i][0] = data.quizlist[i].question;
          questionBank[i][1] = data.quizlist[i].option1;
          questionBank[i][2] = data.quizlist[i].option2;
          questionBank[i][3] = data.quizlist[i].option3;
          questionBank[i][4] = data.quizlist[i].option4;
      }
      numberOfQuestions = questionBank.length;

      displayQuestion();

function displayQuestion(){
      var rnd=Math.random()*4;
      rnd=Math.ceil(rnd);
      var q1;
      var q2;
      var q3;
      var q4;
      var curr = questionBank[questionNumber];

      if(rnd==1){q1=curr[1]; q2=curr[2]; q3=curr[3]; q4=curr[4]}
      if(rnd==2){q2=curr[1]; q3=curr[2]; q4=curr[3]; q1=curr[4];}
      if(rnd==3){q3=curr[1]; q4=curr[2]; q1=curr[3]; q2=curr[4];}
      if(rnd==4){q4=curr[1]; q1=curr[2]; q2=curr[3]; q3=curr[4];}

    $(stage).append('<div class = "questionText">'+curr[0]+'</div>');
    $(stage).append('<div id="1" class="option">'+q1+'</div>')
    $(stage).append('<div id="2" class="option">'+q2+'</div>')
    $(stage).append('<div id="3" class="option">'+q3+'</div>')
    $(stage).append('<div id="4" class="option">'+q4+'</div>')

    $('.option').click(function(){
      if(questionLock==false){questionLock=true;
      //correct answer
      if(this.id==rnd){
      $(stage).append('<div class="feedback1">RICHTIG</div>');
      score++;
      }
      //wrong answer
      if(this.id!=rnd){
      $(stage).append('<div class="feedback2">LEIDER NEIN</div>');
      }
      setTimeout(function(){changeQuestion()},1000);
      }})
      }//display question

function changeQuestion(){

    questionNumber++;

    if(stage=="#game1"){
        stage2="#game1";stage="#game2";
    }
    else{
        stage2="#game2"; stage="#game1";
    }

    if(questionNumber < numberOfQuestions){displayQuestion();}
    else{displayFinalSlide();}

    $(stage2).animate({"right": "+=800px"}, "slow", function() { $(stage2).css('right' , '-1800px'); $(stage2).empty(); });
    $(stage).animate({"right": "+=800px"}, "slow", function() {questionLock=false; $(stage).css('right' , '0px');});
}//change question

function displayFinalSlide(){

    $(stage).append(" <div class='questionText'>Gratuliere, du hast das Quiz geschafft!<br><br>Anzahl Fragen: "+numberOfQuestions+"<br>Richtige Antworten: "+score+"</div>");

}//display final slide
});

