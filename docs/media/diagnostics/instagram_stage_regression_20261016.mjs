import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {randomBytes} from 'node:crypto';
const path='api/src/processing/services/instagram.js';
const baseline=execFileSync('git',['show','HEAD:'+path],{encoding:'utf8'});
const candidate=fs.readFileSync(path,'utf8');
const embedBlock=`            // html embed (no cookie, cookie)
            if (!hasData(data)) data = await requestHTML(id);
            if (!hasData(data) && cookie) data = await requestHTML(id, cookie);

`;
const gqlBlock=`            // web app graphql api (no cookie, cookie)
            if (!hasData(data)) data = await requestGQL(id);
            if (!hasData(data) && cookie) data = await requestGQL(id, cookie);`;
const reordered=baseline.replace(embedBlock+gqlBlock,gqlBlock+'\n\n'+embedBlock.trimEnd());
assert.notEqual(reordered,baseline);
const media={video_versions:[{width:1,height:1,url:'https://fixture.invalid/video.mp4'}]};
const gql={data:{xdt_shortcode_media:{video_url:'https://fixture.invalid/video.mp4'}}};
const embed=(data)=>'"init",[],['+JSON.stringify({contextJSON:JSON.stringify(data)})+']],';
async function run(source,scenario={}) {
 const stages=[];
 const fakeFetch=async(url)=>{
  const u=String(url);
  const stage=u.includes('/oembed/')?'oembed':u.includes('/media/')?'mobile':u.includes('embed/captioned')?'embed':u.includes('graphql/query')?'graphql':u.includes('bulk-route')?'error_context':'web';
  stages.push(stage);
  if(scenario.throwAt?.includes(stage))throw new Error('PRIVATE_ERROR_DETAIL');
  let data=stage==='oembed'?(scenario.mediaId?{media_id:'fixture-id'}:{}):stage==='mobile'?(scenario.mobile?{items:[scenario.mobile]}:{}):stage==='graphql'?(scenario.gql??{}):{};
  const text=stage==='embed'?(scenario.embed??'<html>missing initializer</html>'):'';
  return {json:async()=>data,text:async()=>text,headers:new Headers()};
 };
 const code=source.replace(/^import .*;\n/gm,'').replace('export default function instagram','function instagram');
 const ig=new Function('fetch','getCookie','updateCookie','createStream','genericUserAgent','randomBytes','resolveRedirectingURL',code+';return instagram;')(fakeFetch,()=>undefined,()=>{},()=>'', 'fixture',randomBytes,()=>{});
 const result=await ig({postId:'fixture123'});
 return {stages,result};
}
test('mobile success skips embed and GraphQL',async()=>{
 for(const src of [baseline,candidate]){const x=await run(src,{mediaId:true,mobile:media});assert.equal(x.result.urls,media.video_versions[0].url);assert.deepEqual(x.stages,['oembed','mobile']);}
});
test('no media_id skips mobile and valid embed succeeds',async()=>{
 const x=await run(candidate,{embed:embed(media)});assert.equal(x.result.urls,media.video_versions[0].url);assert.deepEqual(x.stages,['oembed','embed']);
});
test('missing embed initializer reaches GraphQL only after local fix',async()=>{
 const a=await run(baseline,{gql});assert.equal(a.result.error,'fetch.empty');assert.equal(a.stages.includes('graphql'),false);
 const b=await run(candidate,{gql});assert.equal(b.result.urls,media.video_versions[0].url);assert.equal(b.stages.includes('graphql'),true);
});
test('empty context must not win over GraphQL media',async()=>{
 const a=await run(baseline,{embed:embed({}),gql});assert.equal(a.result.error,'fetch.empty');assert.equal(a.stages.includes('graphql'),false);
 const b=await run(candidate,{embed:embed({}),gql});assert.equal(b.result.urls,media.video_versions[0].url);
});
test('mobile fetch failure preserves existing embed recovery',async()=>{
 const a=await run(baseline,{mediaId:true,throwAt:['mobile'],embed:embed(media)});assert.equal(a.result.urls,media.video_versions[0].url);
 const b=await run(candidate,{mediaId:true,throwAt:['mobile'],embed:embed(media)});assert.equal(b.result.urls,media.video_versions[0].url);
});
test('oEmbed exception still permits later independent retrieval',async()=>{
 const x=await run(candidate,{throwAt:['oembed'],gql});assert.equal(x.result.urls,media.video_versions[0].url);assert.equal(x.stages.includes('mobile'),false);
});
test('all stages without media fail closed and do not invent media',async()=>{
 const x=await run(candidate);assert.equal(x.result.error,'fetch.empty');assert.equal(x.result.urls,undefined);assert.equal(x.stages.includes('graphql'),true);
});
test('malformed context does not suppress GraphQL',async()=>{
 const x=await run(candidate,{embed:'"init",[],[{"contextJSON":"invalid JSON"}]],',gql});assert.equal(x.result.urls,media.video_versions[0].url);
});
test('PR order-only approach loses embed recovery when GraphQL throws',async()=>{
 const x=await run(reordered,{throwAt:['graphql'],embed:embed(media)});assert.equal(x.result.error,'fetch.empty');assert.equal(x.stages.includes('embed'),false);
 const b=await run(candidate,{throwAt:['graphql'],embed:embed(media)});assert.equal(b.result.urls,media.video_versions[0].url);
});
test('GraphQL no-data stays fail-closed after empty embed',async()=>{
 const x=await run(candidate,{embed:embed({}),gql:{data:null}});assert.equal(x.result.error,'fetch.empty');assert.equal(JSON.stringify(x.result).includes('PRIVATE_ERROR_DETAIL'),false);
});
