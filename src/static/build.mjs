import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import crypto from 'crypto';
import * as sass from 'sass';

// Get __dirname in an ES module
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Constants with absolute paths
const PATHS = {
    build: path.resolve(__dirname, './build.json'),
    input: path.resolve(__dirname, './scss/main.scss'),
    output: path.resolve(__dirname, '../public/assets/style.css')
};

// Generate a hash of the compiled CSS
function generateHash(content) {
    return crypto.createHash('md5')
    .update(content)
    .digest('hex')
    .slice(0, 8); // Use first 8 chars for brevity
}

// Update build version in build.json to a content hash
async function updateBuildHash(cssContent) {
    try {
        const hash = generateHash(cssContent);
        const buildData = { version: hash };

        await fs.writeFile(PATHS.build, JSON.stringify(buildData, null, 2));
        console.log(`✅ Build hash ${hash} complete`);
        return hash;
    } catch (err) {
        console.error('❌ Error writing build.json:', err.message);
        throw err;
    }
}

// Compile SCSS to CSS
async function compileSass() {
    try {
        const result = sass.compile(PATHS.input, {
            style: 'compressed',
            sourceMap: false,
        });

        // Ensure output directory exists
        await fs.mkdir(path.dirname(PATHS.output), { recursive: true });
        await fs.writeFile(PATHS.output, result.css);
        console.log('🎨 SCSS successfully compiled to CSS');

        return result.css;
    } catch (err) {
        console.error('❌ SCSS compilation error:', err.message);
        throw err;
    }
}

// Main script execution
async function main() {
    try {
        // Compile first to get CSS content
        const cssContent = await compileSass();
        // Then update build.json with hash of CSS
        await updateBuildHash(cssContent);
    } catch {
        process.exit(1);
    }
}

main();