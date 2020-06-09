// Basil Labib
// 4th Jan 2019
// updated and made a bit workable : 13th Jan , 2019
// Recaman Sequence visualisation
// This might take some time to figure out
// add some sound
// Courtesy : Dan Shiffman
//
// Sequence Definition
// a(0) = 0
// a(n) = a(n-1) - n if a(n) > 0 and a(n) is not in the sequence already
// a(n) = a(n-1) + n otherwise



let attackLevel = 1.0;
let releaseLevel = 0;

let attackTime = 0.001
let decayTime = 0.2;
let susPercent = 0.2;
let releaseTime = 0.5

// the imp arrays
let numbers = [];
let seq = [];
let arcs = [];

let counter;
let index;
let next;
let biggest;

let osc;
let env;

let bgColor = [ 0 ];
let colors = [
  [255, 0, 255], // this is pinkish
  [120 , 0 ,255] // this is purple-indigo
]

function setup()
{

  createCanvas( windowWidth , windowHeight );
  background(bgColor);
  noFill();
  frameRate(5);
  textSize(34);
  textAlign(CENTER);

  // seeding the array
  seq[0] = 0;
  numbers[0] = true;
  counter = 1;
  biggest = seq[0];
  index = seq[0];
  next = 0;

//-------------------SOUND CODE-----------------------------------
  env = new p5.Env();
  env.setADSR(attackTime, decayTime, susPercent, releaseTime);
  env.setRange(attackLevel, releaseLevel);

  osc = new p5.Oscillator();

  osc.setType("sine");
  osc.amp(env);
  osc.start();
//----------------------------------------------------------------
}

class Arc
{
  // encapsulating the x y etc of an arc in its object
  constructor( x , y , diameter ,dir , col = [ 120 , 0, 255])
  {
    this.x = x;
    this.y = y;
    this.diameter = diameter;
    this.dir = dir;
    this.col = col;
  }


  // and them simply drawing it at those pos upside or not depending on the dir
  render()
  {
    stroke(this.col);
    if ( this.dir == 0){
      arc( this.x , this.y , this.diameter , this.diameter , 0 , PI);
    }
    else{
      arc( this.x , this.y , this.diameter , this.diameter , PI , 0);

    }
  }
}



// this one is mine ( Basil )
// function nextRec()
// {
//   // this code generates the next Integer in the recaman Sequence
//   prev = seq[seq.length-1]; // prev <- last term in seq i.e. a(n-1)
//   term = prev - counter;   // term <- a(n-1) - n
//   // this adds the array to the seq of numbers if term is not in array
//   if ( term > 0 && seq.includes(term) == false ){ // condition
//     seq.push(term);       // if condition is true, add it to the last pos in seq
//   }
//   else{
//     seq.push(term + 2*counter);   // otherwise add a(n-1) + n
//   }
//   counter++;                     // increment n each time !
//   // this code above generates the next Integer in the recaman sequence
//   return seq[seq.length-1];
// }

function step()
{
  // attempting to go back
  next = index - counter;

  // this is the very condition for a number to be a part of the sequence
  // if negative or already in sequence then go ahead
  if ( next < 0 || numbers[next] == true){
    next = index + counter;
  }

  // --------------------SOUND CODE--------------------------------------
    let n = ( index % 25 ) + 48;
    let freq = pow( 2 , (n - 49) / 12 ) * 440;
  //  console.log( index , freq );
    osc.freq(freq);
    env.play();
  //---------------------------------------------------------------------

  // this checks and stores the biggest number in sequence for perfect scaling purposes
  if ( index > biggest){
    biggest = index;
  }


  // x is the center of the arc that represents this number i.e next and index
  let x = (next + index) / 2;
  // diameter is well.. i think you can picture what im trying to do
  let diameter = (next - index);

  // let color = random(colors);
  // creating a new Arc and pushing it into the collection of arrays
  let a = new Arc( x , 0 , diameter , counter % 2 , [255]);
  arcs.push(a);


  // if ( counter % 2 == 0){
  //   arc( x , height / 2, diameter , diameter , 0 , PI);
  // }
  // else{
  //   arc( x , height / 2, diameter , diameter , PI , 0);
  // }

  // pushing the number into the seq array
  seq.push(next);
  // the index now is the last number added to the sequence
  index = next;
  // and that place is set to true since it cannot be taken now
  numbers[next] = true;
  // incrementing the counter is the most imp of all
  counter++;
}



function draw()
{
    background(bgColor);
    step();
    // drawing from the middle of the screen
    translate( 0 , height / 2);
    // scaling each frame to fit the biggest number found already in the sequence
    scale( width / biggest );
    // looping through all the arcs and drawing them
    for ( a of arcs){
      a.render();
    }


    // if ( counter >= 250 ){
    //   noLoop();
    // }

}

function mousePressed()
{
    osc.start();
}
