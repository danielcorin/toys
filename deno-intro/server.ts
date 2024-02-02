import { logger } from "https://deno.land/x/hono@v3.11.11/middleware.ts";
import { Context, Hono } from "https://deno.land/x/hono@v3.11.11/mod.ts";
import OpenAI from "https://deno.land/x/openai@v4.25.0/mod.ts";
import { Transcription } from "https://deno.land/x/openai@v4.25.0/resources/audio/transcriptions.ts";

const app = new Hono();
const client = new OpenAI();

const helloAudioUploadable = new File(
  // file omitted from source control
  [await Deno.readFile("hello.mp3")], "hello.mp3", { type: 'audio/mpeg' }
);

app.use("*", logger());
app.get("/", async (c: Context) => {

  const transcription: Transcription = await client.audio.transcriptions.create({
    file: helloAudioUploadable,
    model: "whisper-1",
  })
  return c.text(transcription.text);
});

Deno.serve(app.fetch);
