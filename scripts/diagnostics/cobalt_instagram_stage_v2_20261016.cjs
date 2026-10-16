const fs = require("node:fs");
const crypto = require("node:crypto");

const SHORTCODE = "Dcea3BiPTBm";
const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/155 Safari/537.36";
const commonHeaders = {
  "user-agent": UA,
  "sec-gpc": "1",
  "sec-fetch-site": "same-origin",
  "x-ig-app-id": "936619743392459"
};
const mobileHeaders = {
  "x-ig-app-locale": "en_US",
  "x-ig-device-locale": "en_US",
  "x-ig-mapped-locale": "en_US",
  "user-agent": "Instagram 275.0.0.27.98 Android (33/13; 280dpi; 720x1423; Xiaomi; Redmi 7; onclite; qcom; en_US; 458229237)",
  "accept-language": "en-US",
  "x-fb-http-engine": "Liger",
  "x-fb-client-ip": "True",
  "x-fb-server-cluster": "True",
  "content-length": "0"
};
const embedHeaders = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
  "accept-language": "en-GB,en;q=0.9",
  "cache-control": "max-age=0",
  "dnt": "1",
  "sec-fetch-dest": "document",
  "sec-fetch-mode": "navigate",
  "sec-fetch-site": "none",
  "upgrade-insecure-requests": "1",
  "user-agent": UA
};

const sc = s => Number.isInteger(s) ? s : null;
const result = {
  status: "instagram_stage_diagnostic",
  target: "known_public_reel",
  secrets_exposed: false,
  stages: {}
};

const probeDeadline = Date.now() + 24000;
async function fetchBounded(url, opts={}) {
  const remaining = probeDeadline - Date.now();
  if (remaining <= 0) throw new Error("diagnostic_budget_exhausted");
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), Math.min(4000, remaining));
  let reader;
  try {
    const response = await fetch(url, {...opts, signal: controller.signal, redirect: "follow"});
    reader = response.body?.getReader();
    const chunks = [];
    let bytes = 0;
    if (reader) for (;;) {
      const {done,value} = await reader.read();
      if (done) break;
      bytes += value.byteLength;
      if (bytes > 2097152) throw new Error("diagnostic_body_limit");
      chunks.push(Buffer.from(value));
    }
    return new Response([204,205,304].includes(response.status) ? null : Buffer.concat(chunks), {
      status:response.status, headers:response.headers
    });
  } finally {
    try { await reader?.cancel(); } catch {}
    clearTimeout(timer);
  }
}
function objEntry(name, data) {
  const m = data?.match(new RegExp('\\["' + name + '",.*?,({.*?}),\\d+\\]'));
  if (!m) return null;
  try { return JSON.parse(m[1]); } catch { return null; }
}
function numQuery(name, data) {
  const m = data?.match(new RegExp(name + '=(\\d+)'));
  return m && +m[1] ? +m[1] : undefined;
}
async function jsonOrNull(r) {
  try { return await r.json(); } catch { return null; }
}

async function getApiKey() {
  const u = (process.env.API_KEY_URL || "").trim();
  if (!u) return null;
  let raw;
  try {
    if (u.startsWith("file://")) raw = fs.readFileSync(new URL(u), "utf8");
    else if (/^https?:\/\//i.test(u)) {
      const r = await fetchBounded(u);
      if (!r.ok) return null;
      raw = await r.text();
    } else return null;
    const parsed = JSON.parse(raw);
    const keys = parsed && typeof parsed === "object" && !Array.isArray(parsed) ? Object.keys(parsed) : [];
    return keys.find(k => /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(k)) || null;
  } catch { return null; }
}

(async () => {
  let mediaId = null;

  // Stage 1: exact anonymous oEmbed lookup used by cobalt.
  try {
    const u = new URL("https://i.instagram.com/api/v1/oembed/");
    u.searchParams.set("url", `https://www.instagram.com/p/${SHORTCODE}/`);
    const r = await fetchBounded(u, {headers: mobileHeaders});
    const j = await jsonOrNull(r);
    mediaId = j && typeof j.media_id === "string" ? j.media_id : null;
    result.stages.oembed = {http: sc(r.status), json: !!j, media_id_present: !!mediaId};
  } catch {
    result.stages.oembed = {http: "network_error", json: false, media_id_present: false};
  }

  // Stage 2: exact anonymous mobile media-info lookup.
  if (mediaId) {
    try {
      const r = await fetchBounded(`https://i.instagram.com/api/v1/media/${encodeURIComponent(mediaId)}/info/`, {headers: mobileHeaders});
      const j = await jsonOrNull(r);
      result.stages.mobile = {
        http: sc(r.status),
        json: !!j,
        item_present: !!(j && Array.isArray(j.items) && j.items[0])
      };
    } catch {
      result.stages.mobile = {http: "network_error", json: false, item_present: false};
    }
  } else {
    result.stages.mobile = {http: "not_attempted", json: false, item_present: false};
  }

  // Stage 3: exact anonymous embed fallback shape check.
  try {
    const r = await fetchBounded(`https://www.instagram.com/p/${SHORTCODE}/embed/captioned/`, {headers: embedHeaders});
    const html = await r.text().catch(() => "");
    const m = html.match(/"init",\[\],\[(.*?)\]\],/);
    let context = false;
    if (m) {
      try {
        const x = JSON.parse(m[1]);
        context = !!x?.contextJSON;
      } catch {}
    }
    result.stages.embed = {
      http: sc(r.status),
      legacy_init_marker: !!m,
      context_json_present: context
    };
  } catch {
    result.stages.embed = {http: "network_error", legacy_init_marker: false, context_json_present: false};
  }

  // Stage 4: anonymous web page prerequisites + GraphQL fallback.
  let gqlHeaders = null, gqlBody = null;
  try {
    const page = await fetchBounded(`https://www.instagram.com/p/${SHORTCODE}/`, {headers: embedHeaders});
    const html = await page.text();
    const siteData = objEntry("SiteData", html);
    const polaris = objEntry("PolarisSiteData", html);
    const webConfig = objEntry("DGWWebConfig", html);
    const pushInfo = objEntry("InstagramWebPushInfo", html);
    const extractedLsd = objEntry("LSD", html)?.token;
    const lsd = extractedLsd || crypto.randomBytes(8).toString("base64url");
    const csrf = objEntry("InstagramSecurityConfig", html)?.csrf_token;
    const anonCookie = [
      csrf && "csrftoken=" + csrf,
      polaris?.device_id && "ig_did=" + polaris.device_id,
      "wd=1280x720","dpr=2",
      polaris?.machine_id && "mid=" + polaris.machine_id,
      "ig_nrcb=1"
    ].filter(Boolean).join("; ");
    result.stages.web_prereq = {
      http: sc(page.status),
      site_data: !!siteData,
      polaris_site_data: !!polaris,
      web_config: !!webConfig,
      lsd_present: !!lsd,
      lsd_extracted: !!extractedLsd,
      lsd_synthetic: !extractedLsd,
      csrf_present: !!csrf
    };
    gqlHeaders = {
      ...embedHeaders,
      "x-ig-app-id": webConfig?.appId || "936619743392459",
      "x-fb-lsd": lsd,
      "x-csrftoken": csrf || "",
      "x-asbd-id": "129477",
      "cookie": anonCookie,
      "content-type": "application/x-www-form-urlencoded",
      "x-fb-friendly-name": "PolarisPostActionLoadPostQueryQuery"
    };
    gqlBody = new URLSearchParams({
      "__d":"www","__a":"1","__s":"::diag",
      "__hs":siteData?.haste_session || "20126.HYP:instagram_web_pkg.2.1...0",
      "__req":"b","__ccg":"EXCELLENT",
      "__rev":pushInfo?.rollout_hash || "1019933358",
      "__hsi":siteData?.hsi || "7436540909012459023",
      "__dyn":crypto.randomBytes(154).toString("base64url"),
      "__csr":crypto.randomBytes(154).toString("base64url"),
      "__user":"0","__comet_req":String(numQuery("__comet_req", html) || 7),
      "av":"0","dpr":"2","lsd":lsd,
      "jazoest":String(numQuery("jazoest", html) || Math.floor(Math.random()*10000)),
      "__spin_r":siteData?.__spin_r || "1019933358",
      "__spin_b":siteData?.__spin_b || "trunk",
      "__spin_t":String(siteData?.__spin_t || Math.floor(Date.now()/1000)),
      "fb_api_caller_class":"RelayModern",
      "fb_api_req_friendly_name":"PolarisPostActionLoadPostQueryQuery",
      "variables":JSON.stringify({shortcode:SHORTCODE,fetch_tagged_user_count:null,hoisted_comment_id:null,hoisted_reply_id:null}),
      "server_timestamps":"true",
      "doc_id":"8845758582119845"
    }).toString();
  } catch {
    result.stages.web_prereq = {http:"network_error",site_data:false,polaris_site_data:false,web_config:false,lsd_present:false,csrf_present:false};
  }

  if (gqlHeaders && gqlBody) {
    try {
      const r = await fetchBounded("https://www.instagram.com/graphql/query", {method:"POST",headers:gqlHeaders,body:gqlBody});
      const j = await jsonOrNull(r);
      const data = j?.data || null;
      result.stages.graphql = {
        http: sc(r.status),
        json: !!j,
        data_present: !!data,
        media_present: !!(data?.xdt_shortcode_media || data?.shortcode_media)
      };
    } catch {
      result.stages.graphql = {http:"network_error",json:false,data_present:false,media_present:false};
    }
  } else {
    result.stages.graphql = {http:"not_attempted",json:false,data_present:false,media_present:false};
  }

  // Stage 5: real local cobalt retrieval request, authenticated internally.
  try {
    const apiKey = await getApiKey();
    const headers = {"accept":"application/json","content-type":"application/json"};
    if (apiKey) headers["authorization"] = "Api-Key " + apiKey;
    const r = await fetchBounded("http://127.0.0.1:9000/", {
      method:"POST", headers,
      body:JSON.stringify({
        url:`https://www.instagram.com/reel/${SHORTCODE}/`,
        downloadMode:"audio",
        audioFormat:"mp3",
        disableMetadata:true
      })
    });
    const j = await jsonOrNull(r);
    const rawCode = j?.error && typeof j.error === "object" ? j.error.code : null;
    const allowCode = [
      "error.api.auth.key.missing","error.api.auth.key.invalid",
      "error.api.auth.key.rate_limit","error.api.rate_limit",
      "error.api.fetch.empty","error.api.fetch.fail"
    ].includes(rawCode) ? rawCode : null;
    result.stages.cobalt_retrieval = {
      http: sc(r.status),
      api_key_loaded_internal: !!apiKey,
      response_status: typeof j?.status === "string" && ["redirect","tunnel","picker","local-processing","error"].includes(j.status) ? j.status : "other_or_none",
      allowlisted_error: allowCode
    };
  } catch {
    result.stages.cobalt_retrieval = {http:"network_error",api_key_loaded_internal:false,response_status:"other_or_none",allowlisted_error:null};
  }

  console.log(JSON.stringify(result));
})().catch(() => {
  console.log(JSON.stringify({status:"diagnostic_unavailable",raw_error_suppressed:true}));
  process.exitCode=1;
});
