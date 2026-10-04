// Isolated integration fixture: actual VoiceBridge wrapper/handlers/engines,
// with local provider fakes and memory stores. No real media URL is fetched.
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";
const root = process.env.KRC_TEST_VOICEBRIDGE_ROOT;
if (!root) throw new Error("KRC_TEST_VOICEBRIDGE_ROOT is required");
const load = p => import(pathToFileURL(resolve(root, "dist/src", p)));
const { createManagedVoiceBridgeServer } = await load("managed_server.js");
const { MediaBetaGate } = await load("media_beta.js");
const { derivePublicMediaAdmissionCode } = await load("public_media_admission.js");
const { PublicGeminiYoutubeEngine } = await load("public_gemini_youtube.js");
const { PublicCobaltMediaEngine } = await load("public_cobalt_media.js");
const { ManagedMediaService } = await load("managed_media_service.js");
delete process.env.KRC_MEDIA_DATABASE_URL; // Process-local fixture isolation.
const tokens = {
  read: "fixture-media-read-token-20261004",
  youtube: "fixture-media-youtube-token-20261004",
  instagram: "fixture-media-instagram-token-20261004",
  facebook: "fixture-media-facebook-token-20261004",
  telegram: "fixture-media-telegram-token-20261004"
};
const counts = { youtube: 0, instagramRetrieval: 0, instagramStt: 0,
  facebookRetrieval: 0, facebookStt: 0, telegramRetrieval: 0, telegramStt: 0, paid: 0 };
const code = derivePublicMediaAdmissionCode(tokens.read);
function result(platform) {
  const texts = [platform + " first", "Український текст", platform + " last 🙂"];
  return {
    provider: "assemblyai", provider_model: "universal-2", provider_data_deleted: true,
    detected_language: "uk", language_confidence: 1, duration_seconds: 3,
    transcript_text: texts.join("\n"),
    segments: texts.map((text, index) => ({
      index, start_ms: index * 1000, end_ms: (index + 1) * 1000, text, confidence: 1
    }))
  };
}
function asset(url, platform) {
  return { source_url: url, media_url: "https://fixture.invalid/" + platform + ".mp4",
    duration_seconds: 3, provider: platform === "telegram" ? "telegram_public_web" : "cobalt",
    provider_mode: platform === "telegram" ? "telegram_post" : "self_hosted",
    credits_charged: 0, credits_remaining: null, cached: false };
}
const youtube = new PublicGeminiYoutubeEngine(new MediaBetaGate([code]), null, true, "fixture-gemini", {
  provider: { configured: true, model: "fixture-gemini", async transcribe() {
    counts.youtube++;
    return { ...result("youtube"), provider: "gemini", provider_model: "fixture-gemini", provider_data_deleted: null };
  }}
});
const instagram = new PublicCobaltMediaEngine(new MediaBetaGate([code]), null, null, null, {
  retriever: { configured: true, async retrieve(url) { counts.instagramRetrieval++; return asset(url, "instagram"); }},
  stt: { configured: true, async transcribe(_asset, _hint, reserve) {
    counts.instagramStt++; await reserve(3); return result("instagram");
  }}
});
const managed = new ManagedMediaService(new MediaBetaGate([code]), null, undefined, {
  facebookPipeline: { configured: true,
    async freeRetrieve(url) { counts.facebookRetrieval++; return asset(url, "facebook"); },
    async paidRetrieve() { counts.paid++; throw new Error("paid provider forbidden"); },
    async transcribe(_asset, _hint, reserve) { counts.facebookStt++; await reserve(3); return result("facebook"); }
  },
  telegramPipeline: { configured: true,
    async retrieve(url) { counts.telegramRetrieval++; return asset(url, "telegram"); },
    async transcribe(_asset, _hint, reserve) { counts.telegramStt++; await reserve(3); return result("telegram"); }
  }
});
const config = {
  host: "127.0.0.1", port: 0, testAccessToken: "fixture-legacy-token-20261004",
  mediaActionToken: tokens.read, mediaR3e1ActionToken: tokens.youtube,
  mediaR3e2ActionToken: tokens.instagram, mediaR3e3ActionToken: tokens.facebook,
  mediaR3e4ActionToken: tokens.telegram, mediaBetaCodes: [code],
  mediaPublicMode: true, mediaFreeTierOnly: true, mediaDailySttSeconds: 7200,
  assemblyAiApiKey: "fixture-unused-key", geminiApiKey: null,
  cobaltEndpoint: "https://fixture.invalid", cobaltApiKey: "fixture-unused-key",
  geminiTranslationModel: "fixture-model", corsAllowedOrigin: "*",
  maxRequestBodyBytes: 32768, rateLimitRequestsPerMinute: 60
};
let server;
async function listen() {
  server = createManagedVoiceBridgeServer(config, {
    managedService: managed, youtubeEngine: youtube, cobaltEngine: instagram
  });
  await new Promise((resolve, reject) => {
    server.once("error", reject); server.listen(0, "127.0.0.1", resolve);
  });
  return "http://127.0.0.1:" + server.address().port;
}
async function close() {
  server.closeAllConnections();
  await new Promise((resolve, reject) => server.close(e => e ? reject(e) : resolve()));
}
console.log(JSON.stringify({ url: await listen(), tokens }));
// Parent-controlled IPC, never exposed as a public diagnostic endpoint.
process.stdin.setEncoding("utf8");
let pending = "";
process.stdin.on("data", chunk => {
  pending += chunk;
  while (pending.includes("\n")) {
    const index = pending.indexOf("\n");
    const command = pending.slice(0, index); pending = pending.slice(index + 1);
    void (async () => {
      if (command === "counts") console.log(JSON.stringify({ counts }));
      else if (command === "restart") {
        await close(); console.log(JSON.stringify({ url: await listen(), counts }));
      } else if (command === "stop") {
        await close(); process.exit(0);
      }
    })().catch(error => { console.error(error); process.exit(1); });
  }
});
