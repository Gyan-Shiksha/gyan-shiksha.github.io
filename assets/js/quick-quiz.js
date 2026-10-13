(() => {
"use strict";
const QUESTIONS = {
"10":[
["x² − 5x + 6 = 0 ના બંને મૂળ કયાં છે?",["2 અને 3","−2 અને −3","1 અને 6","−1 અને −6"],0,"(x−2)(x−3)=0, તેથી x=2 અથવા x=3."],
["x² − 9 = 0 ના મૂળ શોધો.",["3 અને 0","9 અને −9","3 અને −3","−3 અને 0"],2,"(x−3)(x+3)=0, તેથી બંને મૂળ +3 અને −3."],
["24 અને 36 નો HCF કેટલો?",["6","12","18","24"],1,"24 અને 36 બંનેને ભાગતી સૌથી મોટી સંખ્યા 12 છે."],
["2x + 7 = 19 હોય, તો xનું મૂલ્ય શોધો.",["4","5","7","6"],3,"2x=19−7=12; x=6."],
["3, 7, 11, ... આ સમાંતર શ્રેણીનું ચોથું પદ કયું?",["13","15","17","19"],1,"દરેક પદમાં 4 ઉમેરાય છે. 11+4=15."],
["ત્રિજ્યા 7 cm હોય તેવા વર્તુળનું ક્ષેત્રફળ કેટલું? (π=22/7)",["44 cm²","77 cm²","154 cm²","308 cm²"],2,"ક્ષેત્રફળ = πr² = (22/7)×7×7 = 154 cm²."],
["(0,1) અને (2,5)માંથી પસાર થતી રેખાનો ઢાળ કેટલો?",["2","3","4","1"],0,"ઢાળ = (5−1)/(2−0)=2."],
["x² − 4x + 4 = 0 નો વિવેચક (Discriminant) કેટલો?",["4","8","−4","0"],3,"D=(−4)²−4×1×4=0."],
["(0,0) અને (3,4) વચ્ચેનું અંતર કેટલું?",["4","5","6","7"],1,"અંતર = √(3²+4²)=√25=5."],
["sin 30° નું મૂલ્ય કેટલું?",["1","√3/2","1/2","0"],2,"sin 30° = 1/2."],
["2³ × 2² કેટલું?",["32","16","64","8"],0,"2⁵ = 32."],
["4, 6 અને 8 નો સરેરાશ કેટલો?",["5","7","8","6"],3,"(4+6+8)/3 = 6."]
],
"12":[
["f(x)=x² હોય તો x=3 પર f'(x) કેટલો?",["3","6","9","12"],1,"f'(x)=2x; x=3 માટે 6."],
["f(x)=3x²−4x+5 નો x=2 પર ઢાળ કેટલો?",["4","6","8","12"],2,"f'(x)=6x−4; f'(2)=8."],
["∫2x dx નું અનિશ્ચિત સમાકલન શું?",["2x²+C","x+C","x³+C","x²+C"],3,"x² નો અવકલજ 2x છે, તેથી x²+C."],
["sin x નો x પ્રમાણે અવકલજ કયો?",["cos x","−cos x","sin x","−sin x"],0,"d(sin x)/dx = cos x."],
["અચળ સંખ્યા 7 નો અવકલજ કેટલો?",["7","1","0","x"],2,"અચળ સંખ્યાનો અવકલજ 0 છે."],
["∫1 dx નું અનિશ્ચિત સમાકલન કયું?",["1+C","x+C","x²+C","0+C"],1,"x નો અવકલજ 1 છે, તેથી x+C."],
["સંતુલિત સિક્કો એક વાર ઉછાળીએ ત્યારે Head આવવાની સંભાવના કેટલી?",["1/4","1","0","1/2"],3,"બે સરખી સંભાવનાવાળા પરિણામમાંથી Head એક છે: 1/2."],
["f(x)=x³ હોય તો x=2 પર f'(x) શોધો.",["12","8","6","4"],0,"f'(x)=3x², તેથી 3×2²=12."],
["આવ્યુહ [[1,2],[3,4]] નો Determinant કેટલો?",["2","−1","−2","10"],2,"1×4−2×3=−2."],
["tan 45° નું મૂલ્ય કેટલું?",["0","1","√3","1/√3"],1,"tan 45° = 1."],
["x⁴ નો x પ્રમાણે અવકલજ કયો?",["x³","3x³","4x⁴","4x³"],3,"Power ruleથી 4x³."],
["2, 5, 8, ... સમાંતર શ્રેણીનું પાંચમું પદ કેટલું?",["14","11","17","20"],0,"a=2, d=3. પાંચમું પદ = 2+4×3=14."]
]
};
if (typeof module !== "undefined" && module.exports) module.exports = QUESTIONS;
const root=document.getElementById("quick-quiz-app");
if(!root)return;
const grade=document.getElementById("quick-grade");
const start=document.getElementById("quick-start");
const heading=document.getElementById("quick-question");
const choices=document.getElementById("quick-options");
const status=document.getElementById("quick-progress");
const feedback=document.getElementById("quick-feedback");
const next=document.getElementById("quick-next");
const retry=document.getElementById("quick-retry");
const setup=document.getElementById("quick-setup");
const play=document.getElementById("quick-play");
const finish=document.getElementById("quick-finish");
const scoreText=document.getElementById("quick-score");
let current=[],index=0,score=0,answered=false;
function show(e){e.hidden=false}
function hide(e){e.hidden=true}
function question(){
const q=current[index];answered=false;heading.textContent=q[0];
status.textContent="પ્રશ્ન "+(index+1)+" / "+current.length+" · સાચા જવાબ: "+score;
choices.replaceChildren();
q[1].forEach((value,pos)=>{
 const b=document.createElement("button");b.type="button";b.className="quick-choice";
 b.textContent=["A","B","C","D"][pos]+". "+value;
 b.addEventListener("click",()=>answer(pos));choices.append(b);
});
feedback.textContent="";feedback.className="quick-feedback";hide(next);
}
function answer(pos){
if(answered)return;answered=true;
const q=current[index],correct=pos===q[2];if(correct)score++;
[...choices.children].forEach((b,i)=>{
 b.disabled=true;
 if(i===q[2])b.classList.add("is-correct");
 else if(i===pos)b.classList.add("is-incorrect");
});
feedback.textContent=(correct?"✓ સાચો જવાબ! ":"✕ આ જવાબ સાચો નથી. ")+q[3];
feedback.className="quick-feedback "+(correct?"is-correct":"is-incorrect");
status.textContent="પ્રશ્ન "+(index+1)+" / "+current.length+" · સાચા જવાબ: "+score;
next.textContent=index===current.length-1?"પરિણામ જુઓ →":"આગળનો પ્રશ્ન →";
show(next);
}
start.addEventListener("click",()=>{
 if(!QUESTIONS[grade.value])return;
 current=QUESTIONS[grade.value].slice(0,10);index=0;score=0;
 hide(setup);hide(finish);show(play);question();heading.focus();
});
next.addEventListener("click",()=>{
 if(!answered)return;
 index++;if(index<current.length)question();else{
 hide(play);show(finish);
 scoreText.textContent=current.length+"માંથી "+score+" સાચા જવાબ ("+Math.round(score*100/current.length)+"%).";
 retry.focus();
 }
});
retry.addEventListener("click",()=>{hide(finish);show(setup);start.focus()});
})();