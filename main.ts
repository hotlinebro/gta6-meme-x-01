// gta6-meme-x-01 entry (Node 22, standard library only): it copies
// POST.json from the repository root to /output/POST.json, where the gate
// reads it. That is all the program has to do. The entry is the post
// itself: a GTA 6 meme ("THE RECEIPT") made by the agent, posted on X
// from a public account with make.fun (a link or written out) and/or a tag
// of @makefunai and the entrant's play code in its text, POST.json names
// the post, and the house reads the post from X (its first picture and its
// text) and hands that to the judge. Nothing this program writes about
// the post is judged.
//
// The meme picture itself is meme.png in this repository (built by
// make-meme.py); the post carries it as its first picture.
// user posts the meme from their public X account; it is replaced with
// the post's real address before submitting.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
