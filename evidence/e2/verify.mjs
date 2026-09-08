// Independent exact determinant verifier in Q(sqrt(17)); Node builtins only.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const assert=(x,m)=>{if(!x)throw new Error(m);};
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let c=a%b;a=b;b=c;}return a;};
const rational=(a,b=1n)=>{assert(b!==0n,'zero denominator');let g=gcd(a,b);if(b<0n)g=-g;return [a/g,b/g];};
const parse=s=>{assert(typeof s==='string'&&/^-?\d+(\/\d+)?$/.test(s),'invalid rational');let a=s.split('/').map(BigInt);return rational(a[0],a[1]??1n);};
const ra=(x,y)=>rational(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const rn=x=>[-x[0],x[1]];
const rm=(x,y)=>rational(x[0]*y[0],x[1]*y[1]);
const zero=[[0n,1n],[0n,1n]];
const add=(x,y)=>[ra(x[0],y[0]),ra(x[1],y[1])];
const neg=x=>[rn(x[0]),rn(x[1])];
const sub=(x,y)=>add(x,neg(y));
const mul=(x,y)=>[ra(rm(x[0],y[0]),rm([17n,1n],rm(x[1],y[1]))),ra(rm(x[0],y[1]),rm(x[1],y[0]))];
const iszero=x=>x[0][0]===0n&&x[1][0]===0n;
const cross=(a,b)=>[sub(mul(a[1],b[2]),mul(a[2],b[1])),sub(mul(a[2],b[0]),mul(a[0],b[2])),sub(mul(a[0],b[1]),mul(a[1],b[0]))];
const dot=(a,b)=>a.reduce((sum,x,i)=>add(sum,mul(x,b[i])),zero);
const determinant=(a,b,c)=>dot(cross(a,b),c);
function verify(d){
  assert(d.n===23&&d.radicand===17,'wrong field or size');
  // 4^2 < 17 < 5^2. Thus 17 is positive and not a rational square, and
  // a+b*sqrt(17)=0 iff a=b=0 at either real embedding.
  assert(4*4<17&&17<5*5,'field check');
  const convert=rows=>{assert(rows.length===23,'wrong count');return rows.map(row=>{assert(row.length===3,'invalid vector');let v=row.map(pair=>{assert(pair.length===2,'invalid field element');return pair.map(parse);});assert(v.some(x=>!iszero(x)),'zero vector');return v;});};
  const points=convert(d.points),lines=convert(d.lines),inc=d.line_incident_points;
  for(const rows of [points,lines])for(let i=0;i<23;i++)for(let j=i+1;j<23;j++)assert(cross(rows[i],rows[j]).some(x=>!iszero(x)),'duplicate object');
  assert(inc.length===23,'invalid block count');const degrees=Array(23).fill(0);let zeros=0;
  for(let j=0;j<23;j++){
    let block=inc[j];assert(block.length===4&&new Set(block).size===4&&block.every(i=>Number.isInteger(i)&&i>=0&&i<23),'invalid block');
    let a=points[block[0]],b=points[block[1]];
    assert(cross(cross(a,b),lines[j]).every(iszero),'wrong point join');
    for(let i=0;i<23;i++){
      let z=iszero(determinant(a,b,points[i]));assert(z===block.includes(i),'wrong collinearity');
      assert(iszero(dot(points[i],lines[j]))===z,'covector discrepancy');
      if(z){zeros++;degrees[i]++;}
    }
  }
  assert(zeros===92&&degrees.every(x=>x===4),'wrong incidence degrees');
  // For the positive embedding w=sqrt(17)>4, the symmetric matrix
  // S=diag(2,(w-1)/4,1) is positive definite.  The permutation below is
  // an involutive point-line duality, and S*p_i is proportional to line
  // perm[i] for every i.  This is an exact self-polarity certificate.
  const two=[[2n,1n],[0n,1n]], one=[[1n,1n],[0n,1n]];
  const alpha=[[-1n,4n],[1n,4n]];
  const polarity=[0,3,4,1,2,5,6,11,12,13,14,7,8,9,10,15,17,18,16,20,22,21,19];
  assert(new Set(polarity).size===23&&polarity.every(j=>j>=0&&j<23),'polarity is not bijective');
  for(let i=0;i<23;i++){
    const image=[mul(two,points[i][0]),mul(alpha,points[i][1]),mul(one,points[i][2])];
    assert(cross(image,lines[polarity[i]]).every(iszero),'polarity image mismatch');
  }
  return {status:'PASS',field:'Q(sqrt(17)), both real embeddings',points:23,lines:23,determinant_checks:529,dot_product_checks:529,incidences:92,nonincidences:437,positive_embedding_polarity:{matrix:'diag(2,(sqrt(17)-1)/4,1)',positive_definite_reason:'sqrt(17)>4, so every diagonal entry is positive',point_to_line_permutation:polarity,exact_images_checked:23,symmetric_nonsingular_matrix:true}};
}
const input=fs.readFileSync(path.join(here,'witness.json')),d=JSON.parse(input),out=verify(d),adversaries={};
function reject(name,change){let bad=structuredClone(d);change(bad);let rejected=false;try{verify(bad);}catch{rejected=true;}assert(rejected,'corruption accepted');adversaries[name]='REJECT';}
reject('moved_point',d=>{d.points[0][1]=['1','0'];});
reject('duplicate_point',d=>{d.points[2]=d.points[1];});
reject('wrong_incidence',d=>{d.line_incident_points[0][0]=Array.from({length:23},(_,i)=>i).find(i=>!d.line_incident_points[0].includes(i));});
reject('wrong_field',d=>{d.radicand=16;});
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
Object.assign(out,{authority:'INDEPENDENT_REPLAY',decides:[],graph_effect:'NONE',node:process.version,adversaries,input_sha256:hash(input),checker_sha256:hash(fs.readFileSync(fileURLToPath(import.meta.url)))});
fs.writeFileSync(path.join(here,'verification.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out));
