
//
//Sabotaged Recaman Sequence to play Fibonacci Sequence 


let seq = [];
let index;

let attackLevel = 1.0;
let releaseLevel = 0;

let attackTime = 0.001
let decayTime = 0.2;
let susPercent = 0.2;
let releaseTime = 0.5

let env;
let osc;

function  setup() {
createCanvas(600,400);
frameRate(5);

seq[0 ] =0;
seq[1] = 1;

env = new p5.Env();
env.setADSR(attackTime, decayTime, susPercent, releaseTime);
env.setRange(attackLevel, releaseLevel);

osc = new p5.Oscillator();

osc.setType("sine");
osc.amp(env);
osc.start();
//-------------------------

}


function step()
{
  //seq.push(counter);
  seq.push(seq[seq.length - 1 ] + seq[seq.length - 2]);
}

function draw() {


    step();


    index = seq[seq.length - 1];
    console.log(index);
    let n = ( index % 25 ) + 48;
    let freq = pow( 2 , (n - 49) / 12 ) * 440;
  //  console.log( index , freq );
    osc.freq(freq);
    env.play();
  //----------------


}

function mousePressed()
{
  osc.start();
}
