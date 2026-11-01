import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "..");
const distDir = path.resolve(rootDir, "dist");
const outputDir = path.resolve(rootDir, ".output/public");

if (fs.existsSync(distDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
  fs.cpSync(distDir, outputDir, { recursive: true });
  console.log(`[copy-dist] Synced dist/ to .output/public/`);
}
