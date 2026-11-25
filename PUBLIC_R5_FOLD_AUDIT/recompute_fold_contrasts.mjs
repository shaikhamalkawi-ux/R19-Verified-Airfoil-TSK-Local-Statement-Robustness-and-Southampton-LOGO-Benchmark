#!/usr/bin/env node
// Recompute descriptive fold contrasts from two already-public, immutable R5 files.
// Node.js >= 18. No external libraries, no new fits, no reviewer-only files.
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
function compute(raw, comparison) {
  function check(ok,msg){if(!ok)throw new Error(msg);}
  function csv(s,header) {
    const [h,...lines]=s.trimEnd().split(/\r?\n/);
    check(h===header,"Unexpected CSV header");
    return lines.map(l=>{const row=l.split(",");check(row.length===header.split(",").length,"Malformed CSV row");return row;});
  }
  const rows=csv(raw,"feature_set,mode,representation,outer_fold,model,row_id,group_id,y,pred");
  const contrasts=csv(comparison,"contrast,A,B,difference_equal_config_RMSE_dB,conditional_low_2p5,conditional_high_97p5,resamples,independent_retraining,p_value");
  check(rows.length===30060&&contrasts.length===13,"Unexpected source dimensions");
  const keys=[...new Set(contrasts.flatMap(r=>[r[1],r[2]]))];
  check(keys.length===14,"Unexpected model-feature families");
  const losses=new Map(keys.map(k=>[k,new Map()]));
  const identity=new Map(), groupFold=new Map();
  for(const [f,mode,rep,fold,m,id,g,y,p] of rows){
    const key=f+":"+m;
    if(!losses.has(key))continue;
    const t=Number(y),pred=Number(p),k=Number(fold);
    check(mode==="group"&&rep==="log"&&Number.isInteger(k)&&k>=0&&k<10&&Number.isFinite(t)&&Number.isFinite(pred),"Invalid evaluation record");
    const signature=JSON.stringify([g,k,t]);
    if(identity.has(id))check(identity.get(id)===signature,"Row alignment failed");
    else identity.set(id,signature);
    if(groupFold.has(g))check(groupFold.get(g)===k,"Group split across folds");
    else groupFold.set(g,k);
    const groups=losses.get(key);
    if(!groups.has(g))groups.set(g,{fold:k,ids:new Set(),sse:0});
    const b=groups.get(g);
    check(b.fold===k&&!b.ids.has(id),"Duplicate row or invalid group");
    b.ids.add(id);b.sse+=(pred-t)**2;
  }
  check(identity.size===1503&&groupFold.size===106,"Unexpected sample scope");
  const groups=[...groupFold.keys()].sort(),base=losses.get(keys[0]);
  for(const key of keys){
    const m=losses.get(key);check(m.size===106,"Incomplete model coverage");
    for(const g of groups){
      const a=base.get(g),b=m.get(g);
      check(a&&b&&a.ids.size===b.ids.size&&[...a.ids].every(id=>b.ids.has(id)),"Model row alignment failed");
    }
  }
  function rmse(key,gs){return Math.sqrt(gs.reduce((s,g)=>{const b=losses.get(key).get(g);return s+b.sse/b.ids.size;},0)/gs.length);}
  const summary=[],foldDifferences=[];
  let maximumDifference=0;
  for(const [label,a,b,original] of contrasts){
    const overall=rmse(a,groups)-rmse(b,groups);
    const x=Array.from({length:10},(_,fold)=>{
      const gs=groups.filter(g=>groupFold.get(g)===fold);
      check(gs.length>0,"Empty fold");
      const d=rmse(a,gs)-rmse(b,gs);
      foldDifferences.push({contrast:label,fold,groups:gs.length,difference_dB:d});
      return d;
    });
    const mean=x.reduce((s,v)=>s+v,0)/10;
    const sd=Math.sqrt(x.reduce((s,v)=>s+(v-mean)**2,0)/9);
    const diff=Math.abs(overall-Number(original));check(diff<=1e-10,"Original overall contrast mismatch");
    maximumDifference=Math.max(maximumDifference,diff);
    summary.push({contrast:label,A:a,B:b,overall_difference_dB:overall,fold_mean_dB:mean,fold_sample_sd_dB:sd});
  }
  return {status:"PASS",source_rows:rows.length,selected_model_feature_families:keys.length,observations:identity.size,groups:groupFold.size,folds:10,overall_contrasts:summary.length,paired_fold_differences:foldDifferences.length,max_abs_overall_difference_from_public_table_dB:maximumDifference,summary,fold_differences:foldDifferences};
}
async function load(path,url,expectedSha){
  let bytes;
  if(path){bytes=await readFile(path);}else{const response=await fetch(url);if(!response.ok)throw Error("HTTP "+response.status+" "+url);bytes=Buffer.from(await response.arrayBuffer());}
  const actual=createHash("sha1").update("blob "+bytes.length+"\0").update(bytes).digest("hex");
  if(actual!==expectedSha)throw Error("Git blob identity mismatch: "+url);
  return bytes.toString("utf8");
}
if(process.argv.length!==2&&process.argv.length!==4)throw Error("Usage: node recompute_fold_contrasts.mjs [ALL_PRIMARY_OOF.csv TABLE_PAIRED_CONDITIONAL_RANGES.csv]");
const [raw,table]=await Promise.all([
  load(process.argv[2],"https://raw.githubusercontent.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility/6c537312da0388a0c9a2784ee175be95f8657747/results/r5/ALL_PRIMARY_OOF.csv","13969778bd29858f4117912e9dbf99ca16e6929a"),
  load(process.argv[3],"https://raw.githubusercontent.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility/6c537312da0388a0c9a2784ee175be95f8657747/results/r5/TABLE_PAIRED_CONDITIONAL_RANGES.csv","1938e156d2a4d0da41bee5a964cfb8a98553c8cb")
]);
console.log(JSON.stringify(compute(raw,table),null,2));
