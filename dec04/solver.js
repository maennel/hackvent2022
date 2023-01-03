function rtod(radians)
{
  var pi = Math.PI;
  d = radians * 360/(2*pi);
  return d;
}

let rot = [2.5132741228718345, 0.4886921905584123, -1.2566370614359172, 0, 2.548180707911721, -1.9547687622336491, -0.5235987755982988, 1.9547687622336491, -0.3141592653589793, 0.6283185307179586, -0.3141592653589793, -1.8151424220741028, 1.361356816555577, 0.8377580409572781, -2.443460952792061, 2.3387411976724013, -0.41887902047863906, -0.3141592653589793, -0.5235987755982988, -0.24434609527920614, 1.8151424220741028];

let values = [];
for (let r of rot) {
    values.push(Math.round(rtod(r)));
}

let flag = [];
let previous = 0;
for (let v of values) {
    previous = previous + v/2;
  flag.push(String.fromCharCode(previous));
}
console.log(flag.join(""));
// Flag: HV22{C4lcul8_w1th_PI}

