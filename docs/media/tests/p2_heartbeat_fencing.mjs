import assert from 'node:assert/strict';
import { ManagedMediaPersistentStore } from './dist/src/managed_media_persistence.js';
import { ManagedMediaService, parseManagedMediaNativeInput } from './dist/src/managed_media_service.js';
import { MediaBetaGate } from './dist/src/media_beta.js';
import { execFileSync } from 'node:child_process';
const code='abcdefghijkl',url='https://youtu.be/krcleaseheartbeat2026';
const q=(db,sql)=>execFileSync('psql',['-X','-At','-F','|','-d',db,'-c',sql],{encoding:'utf8'}).trim();
function input(){return parseManagedMediaNativeInput({url,language_hint:'auto',beta_access_code:code,credit_consent:{provider:'supadata',mode:'native',max_credits:1}})}
function mock(timing){let started;const start=new Promise(resolve=>started=resolve);let release;const wait=new Promise(resolve=>release=resolve);let count=0;const provider={
async quoteNative(){return {provider:'supadata',mode:'native',plan:'Free',max_credits:100,used_credits:1,remaining_credits:99,estimated_credits:1,remaining_after_estimate:98,consent_required:true,can_continue:true}},
async getNativeTranscript(){count++;started();await wait;return {status:'completed',language:'en',available_languages:['en'],segments:[{index:0,start_ms:0,end_ms:1000,text:'lease test segment',confidence:null}],transcript_text:'lease test segment',billable_credits:1}}
};return {provider,start,finish:()=>release(),calls:()=>count};}
function app(store,provider){return new ManagedMediaService(new MediaBetaGate([code]),null,provider,{store});}
function sqlJob(db){return q(db,"SELECT job_id,status,lease_owner,extract(epoch from lease_heartbeat_at)::bigint FROM krc_managed_media_jobs ORDER BY updated_at DESC LIMIT 1").split('|')}
function sleep(ms){return new Promise(r=>setTimeout(r,ms))}
async function heartbeat(){
const db='p2_heartbeat', owner=new ManagedMediaPersistentStore(db), other=new ManagedMediaPersistentStore(db), m=mock();
const svc=app(owner,m.provider), pending=svc.startNative(input());await m.start;
const pre=sqlJob(db);assert.equal(pre[1],'PROCESSING');
console.log('HEARTBEAT_START',new Date().toISOString(),pre[0]);
await sleep(102000);
const post=sqlJob(db);
assert.equal(post[1],'PROCESSING');
assert.equal(post[0],pre[0]);
assert.equal(post[2],pre[2]);
assert.ok(Number(post[3])-Number(pre[3])>=75,'heartbeat must advance substantially');
const otherResult=await app(other,m.provider).startNative(input());
assert.equal(otherResult.status,'PROCESSING');assert.equal(otherResult.reused,true);
assert.equal(m.calls(),1);
m.finish();const done=await pending;
assert.equal(done.status,'COMPLETED');
assert.equal(sqlJob(db)[1],'COMPLETED');
console.log('HEARTBEAT_102S_PASS',JSON.stringify({elapsed_s:102,heartbeat_advance_s:Number(post[3])-Number(pre[3]),other_status:otherResult.status,provider_calls:m.calls(),final:done.status}));
}
async function fencing(){
const db='p2_fencing',owner=new ManagedMediaPersistentStore(db),other=new ManagedMediaPersistentStore(db),m=mock();
const svc=app(owner,m.provider),pending=svc.startNative(input());await m.start;
const [id]=sqlJob(db);assert.ok(id.startsWith('KRCM_'));
q(db,"UPDATE krc_managed_media_jobs SET lease_heartbeat_at=now()-interval '121 seconds' WHERE job_id='"+id+"'");
const otherResult=await app(other,m.provider).startNative(input());
assert.equal(otherResult.status,'FAILED');assert.equal(otherResult.error?.code,'MANAGED_PROVIDER_RESULT_UNCERTAIN_RETRY_BLOCKED');
const before=sqlJob(db);assert.equal(before[1],'FAILED');
m.finish();
let rejected=false;
try{await pending}catch(e){rejected=String(e).includes('fenced write rejected')}
assert.equal(rejected,true,'old owner late-write must reject');
const after=sqlJob(db);assert.equal(after[1],'FAILED');assert.equal(after[2],before[2]);assert.equal(m.calls(),1);
console.log('FENCING_OLD_WORKER_PASS',JSON.stringify({job_id:id,final:after[1],provider_calls:m.calls(),old_write_rejected:rejected}));
}
try {await fencing();await heartbeat();console.log('P2_HEARTBEAT_AND_FENCING_PASS')}catch(e){console.error('P2_HEARTBEAT_AND_FENCING_FAIL',e);process.exitCode=1}