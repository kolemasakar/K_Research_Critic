import fs from 'node:fs';
import assert from 'node:assert/strict';
const file=process.argv[2];
const source=fs.readFileSync(file,'utf8').replace(/^import .*;\n/gm,'').replace('export default function instagram','function instagram');
const run = async (embed) => {
  const calls=[];
  const fetch=async(url)=>{
    calls.push(String(url));
    if(String(url).includes('/oembed/'))return {json:async()=>({})};
    if(String(url).includes('/embed/captioned/'))return {text:async()=>embed};
    if(String(url).includes('/graphql/query'))return {json:async()=>({data:{xdt_shortcode_media:{video_url:'https://fixture.invalid/video.mp4'}}})};
    return {text:async()=>'',json:async()=>({})};
  };
  const instagram=new Function('fetch','getCookie','updateCookie','createStream','genericUserAgent','randomBytes','resolveRedirectingURL',source+'; return instagram;')(fetch,()=>undefined,()=>{},()=>'', 'fixture',()=>({toString:()=> 'fixture'}),()=>{});
  const result=await instagram({postId:'fixture123'});
  return {error:result?.error,hasVideo:Boolean(result?.urls),graphqlAttempted:calls.some(u=>u.includes('/graphql/query'))};
};
for (const embed of ['<html>no legacy embed initializer</html>', '\"init\",[],[{\"contextJSON\":\"{}\"}]],']) {
 const result=await run(embed);
 if(process.argv.includes('--patched')) {
  assert.equal(result.graphqlAttempted,true);
  assert.equal(result.hasVideo,true);
 } else {
  assert.equal(result.error,'fetch.empty');
  assert.equal(result.graphqlAttempted,false);
 }
}
console.log('PASS: two independent fallback scenarios; mode='+ (process.argv.includes('--patched')?'patched':'baseline'));
