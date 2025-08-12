import fs from 'fs';
import { LngLat, QuadTreeNode } from './quadtree.mjs';


const qtFileName = process.argv[2];
const cimsFileName = process.argv[3];

if (!qtFileName) {
    console.error('Please provide the estuve.bin file name as an argument.');
    process.exit(1);
}

if (!cimsFileName) {
    console.error('Please provide the cims.json name as an argument.');
    process.exit(1);
}

fs.readFile(qtFileName, 'utf8', (err, data) => {
    if (err) {
        console.error(`Error reading file "${fileName}":`, err.message);
        process.exit(1);
    }

    const decoded = Buffer.from(data, 'base64').toString('utf8');

    const obj = JSON.parse(decoded)
    const qt = QuadTreeNode.deserialize(obj.qt)

    const cimsDataRaw = fs.readFileSync(cimsFileName, 'utf-8')
    const cims = JSON.parse(cimsDataRaw)

    const ignored = fs.readFileSync("scripts/not-exact.json", 'utf-8')
    const ignoredCims = JSON.parse(ignored)

    const tolerance = 25

    for (let cim of cims) {

        if (ignoredCims.includes(cim.name)) {
            continue
        }

        if (cim.fet && !qt.locationIsOnTree(cim.lat, cim.lng, tolerance)) {
            console.log(`❌ ${cim.name} marked as done but not present in quadtree. Link: ${cim.link}`)
        }
        if (!cim.fet && qt.locationIsOnTree(cim.lat, cim.lng, tolerance)) {
            console.log(`⚠️ ${cim.name} is on quadtree and marked as not fet. Link: ${cim.link}`)
        }
    }


});
