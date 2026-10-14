import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { PGlite } from '@electric-sql/pglite';
import { ManagedMediaService, parseManagedMediaNativeInput } from './dist/src/managed_media_service.js';
import { MediaBetaGate } from './dist/src/media_beta.js';

const root='/tmp/krc_p2_pg_crash_20261014';
const access='abcdefghijkl', url='https://youtu.be/durable123';
const mode=process.argv[2]||'all';
const input=()=>parseManagedMediaNativeInput({url,language_hint:'auto',beta_access_code:access,credit_consent:{provider:'supadata',mode:'native',max_credits:1}});
class PgStore {
  durable=true;kind='postgres';db;
  constructor(dir){this.db=new PGlite(dir);}
  async ready(){await this.db.exec('CREATE TABLE IF NOT EXISTS jobs (job_id text PRIMARY KEY, request_key text UNIQUE NOT NULL, document jsonb NOT NULL, expires_at timestamptz NOT NULL);');}
  async purgeExpired(){await this.db.exec('DELETE FROM jobs WHERE expires_at<=now()');}
  async findByRequestKey(key){let r=await this.db.query('SELECT document FROM jobs WHERE request_key=$1 AND expires_at>now()', [key]); return r.rows[0]?.document??null;}
  async reserve(rec){await this.db.query('INSERT INTO jobs(job_id,request_key,document,expires_at) VALUES ($1,$2,$3,$4) ON CONFLICT(request_key) DO NOTHING',[rec.job.job_id,rec.requestKey,JSON.stringify(rec),rec.expiresAt]);let r=await this.findByRequestKey(rec.requestKey);assert.ok(r);return {created:r.job.job_id===rec.job.job_id,record:r};}
  async put(rec){await this.db.query('INSERT INTO jobs(job_id,request_key,document,expires_at) VALUES ($1,$2,$3,$4) ON CONFLICT(job_id) DO UPDATE SET document=excluded.document,expires_at=excluded.expires_at',[rec.job.job_id,rec.requestKey,JSON.stringify(rec),rec.expiresAt]);}
  async get(id){let r=await this.db.query('SELECT document FROM jobs WHERE job_id=$1 AND expires_at>now()', [id]);return r.rows[0]?.document??null;}
  async reserveSttSeconds(jobId,dayUtc,requestedSeconds,limitSeconds){await this.db.exec('CREATE TABLE IF NOT EXISTS quota(job_id text PRIMARY KEY,seconds integer NOT NULL)');await this.db.query('INSERT INTO quota(job_id,seconds) VALUES($1,$2) ON CONFLICT(job_id) DO NOTHING',[jobId,Math.ceil(requestedSeconds)]);const q=await this.db.query('SELECT COALESCE(sum(seconds),0)::integer AS total FROM quota');return {allowed:q.rows[0].total<=limitSeconds,used_seconds:q.rows[0].total,remaining_seconds:limitSeconds-q.rows[0].total};}
  async close(){await this.db.close();}
}
function provider(file,block=false){return {
 async quoteNative(){return {provider:'supadata',mode:'native',plan:'Free',max_credits:100,used_credits:1,remaining_credits:99,estimated_credits:1,remaining_after_estimate:98,consent_required:true,can_continue:true};},
 async getNativeTranscript(){fs.appendFileSync(file,'PROVIDER_CALL\n'); if(block){fs.writeFileSync(root+'/holder_started','yes');await new Promise(()=>{setInterval(()=>{},1000);});}return {status:'completed',language:'en',available_languages:['en'],segments:[{index:0,start_ms:100,end_ms:900,text:'test segment',confidence:null}],transcript_text:'test segment',billable_credits:1};}
};}
function count(file){return fs.existsSync(file)?fs.readFileSync(file,'utf8').trim().split('\n').filter(Boolean).length:0;}
async function startService(dir,file,block=false){const store=new PgStore(dir);await store.ready();const svc=new ManagedMediaService(new MediaBetaGate([access]),null,provider(file,block),{store});return {svc,store};}
async function holder(){
 const {svc}=await startService(root+'/crash',root+'/crash.count',true);
 await svc.startNative(input());
}
async function recover(){
 const {svc,store}=await startService(root+'/crash',root+'/crash.count');
 const recovered=await svc.startNative(input());
 assert.equal(recovered.status,'FAILED');
 assert.equal(recovered.error?.code,'MANAGED_PROVIDER_RESULT_UNCERTAIN_RETRY_BLOCKED');
 assert.equal(recovered.error?.retryable,false);
 assert.equal(recovered.credit_charge_uncertain,true);
 assert.equal(count(root+'/crash.count'),1);
 const stored=await store.get(recovered.job_id);assert.equal(stored.job.status,'FAILED');
 await store.close();
 console.log('CRASH_RECOVERY_FAIL_CLOSED_PASS provider_calls=1 status=FAILED');
}
async function completeReplay(){
 const dir=root+'/completed',file=root+'/completed.count';
 let {svc,store}=await startService(dir,file);
 let first=await svc.startNative(input());
 assert.equal(first.status,'COMPLETED');assert.equal(count(file),1);
 await store.close();
 ({svc,store}=await startService(dir,file));
 let second=await svc.startNative(input());
 assert.equal(second.job_id,first.job_id);assert.equal(second.reused,true);
 assert.equal(second.status,'COMPLETED');assert.equal(count(file),1);
 const page=await svc.page(first.job_id,0,20);
 assert.equal(page.segments.length,1);
 await store.close();
 console.log('LOST_REPLY_COMPLETED_REUSE_PASS provider_calls=1 job_same=true');
}
async function concurrent(){
 const dir=root+'/concurrent',file=root+'/concurrent.count';
 let entered, release;
 const gate=new Promise(r=>entered=r), finish=new Promise(r=>release=r);
 const fake=provider(file);
 const original=fake.getNativeTranscript;
 fake.getNativeTranscript=async()=>{entered();await finish;return original();};
 const store=new PgStore(dir);await store.ready();
 const svc=new ManagedMediaService(new MediaBetaGate([access]),null,fake,{store});
 const firstP=svc.startNative(input());await gate;
 const second=await svc.startNative(input());
 assert.equal(second.status,'PROCESSING');assert.equal(second.reused,true);
 release();let first=await firstP;
 assert.equal(first.status,'COMPLETED');assert.equal(count(file),1);
 await store.close();
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
 const store=new PgStore(root+'/facebook');await store.ready();
 const svc=new ManagedMediaService(new MediaBetaGate([access],7200),null,undefined,{store,facebookPipeline:fbProvider(true)});
 await svc.startFacebookFallback(fbInput);
}
async function facebookRecover(){
 const store=new PgStore(root+'/facebook');await store.ready();
 const svc=new ManagedMediaService(new MediaBetaGate([access],7200),null,undefined,{store,facebookPipeline:fbProvider(false)});
 const job=await svc.startFacebookFallback(fbInput);
 assert.equal(job.status,'COMPLETED');
 assert.equal(job.credits_charged,0);
 assert.equal(count(root+'/fb_free.count'),2);
 assert.equal(count(root+'/fb_stt.count'),1);
 assert.equal(count(root+'/fb_paid.count'),0);
 const q=await store.db.query("SELECT document->'job'->>'status' AS status, COUNT(*)::integer AS n FROM jobs GROUP BY 1");
 assert.equal(q.rows.find(x=>x.status==='FAILED')?.n,1);
 assert.equal(q.rows.find(x=>x.status==='COMPLETED')?.n,1);
 await store.close();
 console.log('FREE_FACEBOOK_CRASH_CONTROLLED_RETRY_PASS free_retrieval_calls=2 fake_stt_calls=1 paid_calls=0 two_job_states=FAILED_COMPLETED');
}

if(mode==='fbholder')await facebookHolder();
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