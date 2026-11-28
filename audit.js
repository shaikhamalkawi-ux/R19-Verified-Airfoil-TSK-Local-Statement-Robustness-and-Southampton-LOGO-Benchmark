/* Browser companion, v0.1.0-web. Finite-input float64 numerical checks. */
(function(root){'use strict';
const G=1e-8;
const dot=(a,b)=>{let s=0;for(let i=0;i<a.length;i++)s+=a[i]*b[i];return s};
const norm=a=>Math.sqrt(dot(a,a));
const vec=a=>Float64Array.from(a);
const finite=a=>Array.from(a).every(Number.isFinite);
function model(m){
 if(!Array.isArray(m.P)||!m.P.length||!Array.isArray(m.beta)||!m.beta.length||!Array.isArray(m.ytrain))throw Error('Missing P, beta or ytrain arrays');
 const P=m.P.map(vec), b=vec(m.beta), y=vec(m.ytrain), n=P.length,q=b.length,lam=Number(m.lam),offset=Number(m.offset??0), Pt=m.Pt==null?null:m.Pt.map(vec);
 if(n>20000||q>200||y.length!==n||P.some(r=>r.length!==q||!finite(r))||!finite(b)||!finite(y)||!(lam>0)||!Number.isFinite(lam)||!Number.isFinite(offset)||Pt&&(Pt.length===0||Pt.some(r=>r.length!==q||!finite(r))))throw Error('Invalid dimensions or nonfinite values. Limits: 20,000 rows, 200 coefficients; lambda > 0.');
 for(let i=0;i<n;i++)y[i]-=offset;
 const H=Array.from({length:q},()=>new Float64Array(q)),g=new Float64Array(q);let J=lam*dot(b,b);
 for(let j=0;j<q;j++){H[j][j]=lam;g[j]=lam*b[j]}
 for(let i=0;i<n;i++){const p=P[i],r=dot(p,b)-y[i];J+=r*r/n;for(let j=0;j<q;j++){g[j]+=p[j]*r/n;for(let k=0;k<=j;k++)H[j][k]+=p[j]*p[k]/n}}
 for(let j=0;j<q;j++)for(let k=0;k<j;k++)H[k][j]=H[j][k];
 if(!(J>0)||!Number.isFinite(J))throw Error('Reference ridge objective must be positive and finite');
 const L=Array.from({length:q},()=>new Float64Array(q));
 for(let i=0;i<q;i++)for(let j=0;j<=i;j++){let v=H[i][j];for(let k=0;k<j;k++)v-=L[i][k]*L[j][k];if(i===j){if(!(v>0))throw Error('Cholesky failed; check design or ridge penalty');L[i][j]=Math.sqrt(v)}else L[i][j]=v/L[j][j]}
 function lower(a){const x=new Float64Array(q);for(let i=0;i<q;i++){let s=a[i];for(let j=0;j<i;j++)s-=L[i][j]*x[j];x[i]=s/L[i][i]}return x}
 function upper(a){const x=new Float64Array(q);for(let i=q-1;i>=0;i--){let s=a[i];for(let j=i+1;j<q;j++)s-=L[j][i]*x[j];x[i]=s/L[i][i]}return x}
 const center=upper(lower(g));for(let i=0;i<q;i++)center[i]*=-1;
 const gHg=-dot(g,center), W=P.map(lower), pc=P.map(p=>dot(p,center));
 if(!finite(center)||!Number.isFinite(gHg))throw Error('Invalid objective geometry');
 return {P,Pt,b,y,n,q,lam,H,g,J,center,gHg,W,pc,lower,upper,R:m.R,labels:m.labels};
}
function check(m,j,d,eps,eta,gamma){
 if(!finite(d))return null;const b=m.b[j],base=Math.abs(b),move=-Math.sign(b)*d[j],alt=vec(m.b);for(let k=0;k<m.q;k++)alt[k]+=d[k];
 const train=Math.max(...m.P.map(p=>Math.abs(dot(p,d))));let J2=m.lam*dot(alt,alt);for(let i=0;i<m.n;i++){let r=dot(m.P[i],alt)-m.y[i];J2+=r*r/m.n}
 const direct=(J2-m.J)/m.J,quad=(dot(d,m.H.map(h=>dot(h,d)))+2*dot(m.g,d))/m.J,t=G*(1+base);
 if(![train,direct,quad,move].every(Number.isFinite)||Math.abs(direct-quad)>G*(1+Math.abs(quad))||train>eps||Math.max(direct,quad)>eta||move<=base+t||move<(1+gamma)*base-t)return null;
 const held=m.Pt?Math.max(...m.Pt.map(p=>Math.abs(dot(p,d)))):null;
 return {max_training_change:train,relative_objective_increase:direct,quadratic_objective_increase:quad,heldout_max_change:held,heldout_budget_retained:held===null?null:held<=eps,alternative_beta:Array.from(alt),delta:Array.from(d)};
}
function audit(m,j,eps,eta,gamma=.001,options={}){
 if(!Number.isInteger(j)||j<0||j>=m.q||![eps,eta,gamma].every(v=>Number.isFinite(v)&&v>0))throw Error('Invalid coefficient index or budget');
 const b=m.b[j],base=Math.abs(b),sign=-Math.sign(b),r={index:j,original_coefficient:b,status:'UNRESOLVED',epsilon:eps,eta,gamma,method:'none'};
 if(base<=G)return r;const c=new Float64Array(m.q);c[j]=sign;const w=m.lower(c),cc=dot(c,m.center),rad2=eta*m.J+Math.max(0,m.gHg),rad=Math.sqrt(rad2),wn=norm(w),margin=G*(1+base+norm(m.b));
 const ellipse=cc+rad*wn+margin;r.movement_upper_bound=ellipse;
 if(ellipse<base)return {...r,status:'PROTECTED',method:'ellipsoid',zero_margin:base-ellipse};
 const zt=(target)=>{const z=vec(w),s=(target-cc)/dot(w,w);for(let k=0;k<z.length;k++)z[k]*=s;return z};
 const delta=z=>{const d=m.upper(z);for(let k=0;k<d.length;k++)d[k]+=m.center[k];return d};
 const target=(1+gamma)*base+2*margin;
 let wit=check(m,j,delta(zt(target)),eps,eta,gamma);if(wit)return {...r,status:'REVERSIBLE',method:'direct_witness',...wit};
 // Projection dual in whitened coordinates: every nonnegative multiplier gives a valid lower bound.
 // Use original eps and zero target for protection; tightened eps for strict witness.
 function project(t,cap,proof){
  const q=m.q,n=m.n,active=[],lookup=new Set(),z=new Float64Array(q);let best=-Infinity;
  function add(idx,side){const key=idx+':'+side;if(lookup.has(key))return;lookup.add(key);
   let a=idx===-1?vec(w):vec(m.W[idx]);let rhs=idx===-1?cc-t:cap-side*m.pc[idx];
   const s=idx===-1?-1:side;for(let k=0;k<q;k++)a[k]*=s;const len=norm(a);if(len<1e-30)return;for(let k=0;k<q;k++)a[k]/=len;active.push({idx,side,a,rhs:rhs/len,len,mu:0});
  }
  add(-1,-1);
  for(let round=0;round<(options.rounds??60);round++){
   for(let sweep=0;sweep<(options.sweeps??250);sweep++){
    let change=0;
    for(let h of active){const nm=Math.max(0,h.mu+dot(h.a,z)-h.rhs),d=nm-h.mu;h.mu=nm;change=Math.max(change,Math.abs(d));for(let k=0;k<q;k++)z[k]-=d*h.a[k]}
    if((sweep%10===0||change<1e-10)&&proof){
     // Recompute dual residual from multipliers, not accumulated iterates.
     const s=new Float64Array(q);let rhs=0;for(let h of active){rhs+=h.mu*h.rhs;for(let k=0;k<q;k++)s[k]+=h.mu*h.a[k]}
     const lower=-.5*dot(s,s)-rhs;best=Math.max(best,lower);
     const guard=G*(1+Math.abs(rhs)+dot(s,s)+rad2);
     if(Number.isFinite(lower)&&lower-guard>.5*rad2)return {protected:true,objective_norm_sq_lower:2*(lower-guard),radius_sq:rad2,dual:active.filter(h=>h.mu>0).map(h=>({row:h.idx,side:h.side,multiplier:h.mu/h.len}))};
    }
    if(!finite(z))return {};
    if(change<1e-10)break;
   }
   if(!proof){const wv=check(m,j,delta(z),eps,eta,gamma);if(wv)return {witness:wv}}
   const violations=[];for(let i=0;i<n;i++){const a=dot(m.W[i],z)+m.pc[i],v=Math.abs(a)-cap;if(v>G*Math.max(1,cap)&&!lookup.has(i+':'+Math.sign(a)))violations.push([v,i,Math.sign(a)])}
   violations.sort((a,b)=>b[0]-a[0]);for(const a of violations.slice(0,12))add(a[1],a[2]);
   if(!violations.length){if(proof&&norm(z)<=rad*(1+1e-8)&&dot(w,z)+cc>=t-margin&&m.P.every((p,i)=>Math.abs(dot(m.W[i],z)+m.pc[i])<=cap+G))return {};if(round>8)break}
  }
  return {best};
 }
 const p=project(base,eps,true);if(p.protected)return {...r,status:'PROTECTED',method:'projection_dual',...p};
 const v=project(target,eps*(1-1e-6),false);if(v.witness)return {...r,status:'REVERSIBLE',method:'projection_witness',...v.witness};return r;
}
function demo(){// a valid two-rule, one-input TSK consequent design, synthetic not experimental
 const x=[-1,-.7,-.4,-.1,.1,.4,.7,1],P=x.map(v=>{const w=1/(1+Math.exp(-2*v));return [w,w*v,1-w,(1-w)*v]});const b=[.3,1,-.4,.06],lam=.025;
 // Construct y so beta is a ridge stationary fit (minimum-norm solution to P^T r=-n*lambda*beta).
 // For a transparent demo use ridge fit of prescribed synthetic y instead.
 const y=x.map(v=>.25+.6*v+.05*v*v),q=4;
 const H=Array.from({length:q},(_,j)=>Array.from({length:q},(_,k)=>P.reduce((s,p)=>s+p[j]*p[k]/P.length,0)+(j===k?lam:0)));
 const rhs=Array.from({length:q},(_,j)=>P.reduce((s,p,i)=>s+p[j]*y[i]/P.length,0));
 for(let i=0;i<q;i++){const d=H[i][i];for(let k=i;k<q;k++)H[i][k]/=d;rhs[i]/=d;for(let j=0;j<q;j++)if(i!==j){const f=H[j][i];for(let k=i;k<q;k++)H[j][k]-=f*H[i][k];rhs[j]-=f*rhs[i]}}
 return {P,beta:rhs,ytrain:y,offset:0,lam,R:2,Pt:[-1.4,1.4].map(v=>{const w=1/(1+Math.exp(-2*v));return [w,w*v,1-w,(1-w)*v]}),labels:['Rule 1 intercept','Rule 1 slope','Rule 2 intercept','Rule 2 slope']};}
root.FRG={model,audit,check,demo};if(typeof module!=='undefined')module.exports=root.FRG;
})(typeof self!=='undefined'?self:globalThis);
