import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { ManagedMediaPersistentStore } from './dist/src/managed_media_persistence.js';
import { execFileSync } from 'node:child_process';
import { ManagedMediaService, parseManagedMediaNativeInput } from './dist/src/managed_media_service.js';
import { MediaBetaGate } from './dist/src/media_beta.js';

const root='/tmp/krc_p2_realpg_20261014/results';
const access='abcdefghijkl', url='https://youtu.be/durable123';
const mode=process.argv[2]||'all';
const input=()=>parseManagedMediaNativeInput({url,language_hint:'auto',beta_access_code:access,credit_consent:{provider:'supadata',mode:'native',max_credits:1}});
class RealPgStore extends ManagedMediaPersistentStore {
  constructor(name) { super(name); }
}

function provider(file,block=false){return {
 async quoteNative(){return {provider:'supadata',mode:'native',plan:'Free',max_credits:100,used_credits:1,remaining_credits:99,estimated_credits:1,remaining_after_estimate:98,consent_required:true,can_continue:true};},
 async getNativeTranscript(){fs.appendFileSync(file,'PROVIDER_CALL\n'); if(block){fs.writeFileSync(root+'/holder_started','yes');await new Promise(()=>{setInterval(()=>{},1000);});}return {status:'completed',language:'en',available_languages:['en'],segments:[{index:0,start_ms:100,end_ms:900,text:'test segment',confidence:null}],transcript_text:'test segment',billable_credits:1};}
};}
function count(file){return fs.existsSync(file)?fs.readFileSync(file,'utf8').trim().split('\n').filter(Boolean).length:0;}
async function startService(dir,file,block=false){const store=new RealPgStore(dir);await store.ready();const svc=new ManagedMediaService(new MediaBetaGate([access]),null,provider(file,block),{store});return {svc,store};}
async function holder(){
 const {svc}=await startService('p2_crash',root+'/crash.count',true);
 await svc.startNative(input());
}
async function recover(){
 const {svc,store}=await startService('p2_crash',root+'/crash.count');
 const recovered=await svc.startNative(input());
 assert.equal(recovered.status,'FAILED');
 assert.equal(recovered.error?.code,'MANAGED_PROVIDER_RESULT_UNCERTAIN_RETRY_BLOCKED');
 assert.equal(recovered.error?.retryable,false);
 assert.equal(recovered.credit_charge_uncertain,true);
 assert.equal(count(root+'/crash.count'),1);
 const stored=await store.get(recovered.job_id);assert.equal(stored.job.status,'FAILED');
 
 console.log('CRASH_RECOVERY_FAIL_CLOSED_PASS provider_calls=1 status=FAILED');
}
async function completeReplay(){
 const dir='p2_completed',file=root+'/completed.count';
 let {svc,store}=await startService(dir,file);
 let first=await svc.startNative(input());
 assert.equal(first.status,'COMPLETED');assert.equal(count(file),1);
 
 ({svc,store}=await startService(dir,file));
 let second=await svc.startNative(input());
 assert.equal(second.job_id,first.job_id);assert.equal(second.reused,true);
 assert.equal(second.status,'COMPLETED');assert.equal(count(file),1);
 const page=await svc.page(first.job_id,0,20);
 assert.equal(page.segments.length,1);
 
 console.log('LOST_REPLY_COMPLETED_REUSE_PASS provider_calls=1 job_same=true');
}
async function concurrent(){
 const dir='p2_concurrent',file=root+'/concurrent.count';
 let entered, release;
 const gate=new Promise(r=>entered=r), finish=new Promise(r=>release=r);
 const fake=provider(file);
 const original=fake.getNativeTranscript;
 fake.getNativeTranscript=async()=>{entered();await finish;return original();};
 const store=new RealPgStore(dir);await store.ready();
 const svc=new ManagedMediaService(new MediaBetaGate([access]),null,fake,{store});
 const firstP=svc.startNative(input());await gate;
 const second=await svc.startNative(input());
 assert.equal(second.status,'PROCESSING');assert.equal(second.reused,true);
 release();let first=await firstP;
 assert.equal(first.status,'COMPLETED');assert.equal(count(file),1);
 
 console.log('CONCURRENT_SINGLE_WINNER_PASS provider_calls=1');
}

const fbUrl='https://www.facebook.com/reel/1114235920664408/';
const fbInput={url:fbUrl,language_hint:'auto',beta_access_code:access};
function fbProvider(block){
 return {configured:true,async freeRetrieve(){
  fs.appendFileSync(root+'/fb_free.count','FREE_RETRIEVAL_CALL\n');
  if(block){fs.writeFileSync(root+'/fb_holder_started','yes');await new Promise(()=>{setInterval(()=>{},1000);});}
  return {source_url:fbUrl,media_url:'https://video.example.test/fixture.mp4',duration_seconds:22.2,provider:'cobalt',provider_mode:'self_hosted',credits_charged:0,credits_remaining:null,cached:false};
 },async paidRetrieve(){fs.appendFileSync(root+'/fb_paid.count','PAID_CALLED\n');throw new Error('paid fallback forbidden');},async transcribe(_asset,_language,reserve){
  fs.appendFileSync(root+'/fb_stt.count','FAKE_STT_CALL\n');await reserve(22.2);
  return {provider:'assemblyai',provider_model:'universal-2',provider_data_deleted:true,detected_language:'en',language_confidence:0.97,duration_seconds:22.2,transcript_text:'fixture transcript',segments:[{index:0,start_ms:0,end_ms:1000,text:'fixture transcript',confidence:.95}]};
 }};
}
async function facebookHolder(){
 const store=new RealPgStore('p2_facebook');await store.ready();
 const svc=new ManagedMediaService(new MediaBetaGate([access],7200),null,undefined,{store,facebookPipeline:fbProvider(true)});
 await svc.startFacebookFallback(fbInput);
}
async function facebookRecover(){
 const store=new RealPgStore('p2_facebook');await store.ready();
 const svc=new ManagedMediaService(new MediaBetaGate([access],7200),null,undefined,{store,facebookPipeline:fbProvider(false)});
 const job=await svc.startFacebookFallback(fbInput);
 assert.equal(job.status,'COMPLETED');
 assert.equal(job.credits_charged,0);
 assert.equal(count(root+'/fb_free.count'),2);
 assert.equal(count(root+'/fb_stt.count'),1);
 assert.equal(count(root+'/fb_paid.count'),0);
 const raw=execFileSync('psql',['-X','-A','-t','-F','|','-d','p2_facebook','-c','SELECT status,count(*) FROM krc_managed_media_jobs GROUP BY status ORDER BY status'],{encoding:'utf8'});
 assert.match(raw,/FAILED\|1/); assert.match(raw,/COMPLETED\|1/);
 
 console.log('FREE_FACEBOOK_CRASH_CONTROLLED_RETRY_PASS free_retrieval_calls=2 fake_stt_calls=1 paid_calls=0 two_job_states=FAILED_COMPLETED');
}

if(mode==='crossholder'){
 const {svc}=await startService('p2_cross',root+'/cross.count',true);
 await svc.startNative(input());
}
else if(mode==='crossprobe'){
 const {svc}=await startService('p2_cross',root+'/cross.count');
 const job=await svc.startNative(input());
 assert.equal(count(root+'/cross.count'),1);
 console.log('CROSS_PROCESS_PROBE',JSON.stringify({status:job.status,reused:job.reused,error_code:job.error?.code,provider_calls:count(root+'/cross.count')}));
}
else if(mode==='fbholder')await facebookHolder();
else if(mode==='fbrecover')await facebookRecover();
else if(mode==='holder')await holder();
else if(mode==='recover')await recover();
else{
 fs.mkdirSync(root,{recursive:true});
 await completeReplay();await concurrent();
 const child=spawn(process.execPath,[process.argv[1],'holder'],{stdio:'ignore'});
 let ok=false;
 for(let i=0;i<600;i++){if(fs.existsSync(root+'/holder_started')){ok=true;break;}await new Promise(r=>setTimeout(r,100));}
 assert.ok(ok,'holder must reach provider before kill');
 child.kill('SIGKILL');
 await new Promise(resolve=>child.once('exit',resolve));
 assert.equal(count(root+'/crash.count'),1);
 console.log('CRASH_IN_PROCESSING_INJECTED provider_calls_before=1');
 const revived=spawn(process.execPath,[process.argv[1],'recover'],{stdio:'inherit'});
 const rc=await new Promise(resolve=>revived.once('exit',resolve));assert.equal(rc,0);
 console.log('P2_POSTGRES_ENGINE_ALL_PASS');
}