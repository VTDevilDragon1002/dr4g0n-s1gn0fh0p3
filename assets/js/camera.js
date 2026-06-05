let handCameraStarted=false,lastSpoken='',stableText='',stableCount=0;
const SIGN_SENTENCES={
  fist:'Stop / No / Need attention',
  one:'One finger detected',
  two:'Peace / Two / Victory',
  three:'Three fingers detected',
  four:'Four fingers detected',
  five:'Hello / Open palm / Help',
  thumbsup:'Thumbs up / Yes / Good',
  thumbsdown:'Thumbs down / No / Bad',
  ok:'Okay sign detected',
  ily:'I love you / Care sign',
  call:'Call me / Phone sign'
};
function dist(a,b){return Math.hypot(a.x-b.x,a.y-b.y)}
function isUp(lm,tip,pip,mcp){return lm[tip].y < lm[pip].y && lm[pip].y < lm[mcp].y + .045}
function fingerStates(lm){
  const handedness = (lm[17].x < lm[5].x) ? 'right' : 'left';
  const thumbSide = handedness==='right' ? lm[4].x < lm[3].x-.015 : lm[4].x > lm[3].x+.015;
  return {
    thumb: thumbSide || dist(lm[4],lm[17]) > dist(lm[3],lm[17])*1.05,
    index: isUp(lm,8,6,5), middle: isUp(lm,12,10,9), ring: isUp(lm,16,14,13), pinky: isUp(lm,20,18,17),
    handedness
  };
}
function classifySign(lm){
  const f=fingerStates(lm); const arr=[f.thumb,f.index,f.middle,f.ring,f.pinky]; const count=arr.filter(Boolean).length;
  const pinch=dist(lm[4],lm[8]); const palm=dist(lm[0],lm[9]);
  const thumbVerticalUp = lm[4].y < lm[3].y && lm[3].y < lm[2].y && !f.index && !f.middle && !f.ring && !f.pinky;
  const thumbVerticalDown = lm[4].y > lm[3].y && lm[3].y > lm[2].y && !f.index && !f.middle && !f.ring && !f.pinky;
  if(thumbVerticalUp) return {key:'thumbsup',emoji:'👍',label:SIGN_SENTENCES.thumbsup,confidence:92};
  if(thumbVerticalDown) return {key:'thumbsdown',emoji:'👎',label:SIGN_SENTENCES.thumbsdown,confidence:88};
  if(pinch < palm*.23 && f.middle && f.ring && f.pinky) return {key:'ok',emoji:'👌',label:SIGN_SENTENCES.ok,confidence:90};
  if(f.thumb && f.index && !f.middle && !f.ring && f.pinky) return {key:'ily',emoji:'🤟',label:SIGN_SENTENCES.ily,confidence:89};
  if(f.thumb && !f.index && !f.middle && !f.ring && f.pinky) return {key:'call',emoji:'🤙',label:SIGN_SENTENCES.call,confidence:87};
  const names=['fist','one','two','three','four','five']; const emojis=['✊','☝️','✌️','🖖','🖐️','🖐️'];
  const key=names[count]||'five'; return {key,emoji:emojis[count]||'🖐️',label:SIGN_SENTENCES[key]||`${count} fingers`,confidence:Math.min(96,70+count*4)};
}
function setResult(result,manual=false){
  const emoji=document.getElementById('emoji'), label=document.getElementById('label'), meaning=document.getElementById('meaning'), meter=document.getElementById('confidenceBar'), sentence=document.getElementById('sentence');
  if(!emoji)return; emoji.textContent=result.emoji; label.textContent=manual?'Manual test: '+result.label:result.label; if(meaning)meaning.textContent=result.label; if(meter)meter.style.width=(result.confidence||80)+'%'; if(sentence)sentence.textContent=`Sign result: ${result.label}`;
  if(!manual){ if(stableText===result.label)stableCount++; else {stableText=result.label; stableCount=0;} if(stableCount===10 && lastSpoken!==result.label){lastSpoken=result.label; speak(result.label);} }
}
function manualSign(key){ const data={fist:['✊',92],one:['☝️',90],two:['✌️',90],three:['🖖',85],four:['🖐️',84],five:['🖐️',94],thumbsup:['👍',94],thumbsdown:['👎',91],ok:['👌',92],ily:['🤟',90],call:['🤙',89]}[key]||['✋',80]; const r={key,emoji:data[0],label:SIGN_SENTENCES[key]||key,confidence:data[1]}; setResult(r,true); speak(r.label); }
function cameraSafe(){ return location.protocol==='https:' || location.hostname==='localhost' || location.hostname==='127.0.0.1'; }
async function startHandCamera(){
  const video=document.getElementById('video'),canvas=document.getElementById('canvas'),ctx=canvas.getContext('2d'),label=document.getElementById('label');
  const warn=document.getElementById('cameraWarning'); if(warn) warn.textContent='';
  if(!cameraSafe() && warn){warn.textContent='Camera may be blocked when opened as a file. Run start-server.bat or use localhost for perfect working camera.';}
  if(handCameraStarted){label.textContent='Camera already running. Show your hand clearly.';return;}
  if(!window.Hands || !window.Camera || !window.drawConnectors){label.textContent='MediaPipe library not loaded. Connect internet and refresh, or use manual sign test below.';return;}
  try{
    const hands=new Hands({locateFile:f=>`https://cdn.jsdelivr.net/npm/@mediapipe/hands/${f}`});
    hands.setOptions({maxNumHands:1,modelComplexity:1,minDetectionConfidence:.65,minTrackingConfidence:.65});
    hands.onResults(r=>{
      canvas.width=video.videoWidth||640; canvas.height=video.videoHeight||480; ctx.clearRect(0,0,canvas.width,canvas.height);
      if(r.multiHandLandmarks&&r.multiHandLandmarks.length){const lm=r.multiHandLandmarks[0];drawConnectors(ctx,lm,HAND_CONNECTIONS,{color:'#32e6ff',lineWidth:4});drawLandmarks(ctx,lm,{color:'#ff4d6d',lineWidth:2});setResult(classifySign(lm));}
      else{label.textContent='Show one hand fully inside the box'; const m=document.getElementById('confidenceBar'); if(m)m.style.width='0%';}
    });
    const cam=new Camera(video,{onFrame:async()=>{await hands.send({image:video})},width:640,height:480}); await cam.start(); handCameraStarted=true; label.textContent='Camera started — show your hand sign';
  }catch(err){label.textContent='Camera error: '+(err.message||err); if(warn)warn.textContent='Allow camera permission. On PC, open using start-server.bat, not direct file mode.';}
}
