// https://www.npmjs.com/package/hanzi
var hanzi = require("hanzi");
const fs = require('fs')
const { Parser, transforms: { unwind } } = require('json2csv');
//let csvToJson = require('convert-csv-to-json');
//const zhuyin = require('zhuyin')
//var parser = require('csv-parser');
//const ObjectsToCsv = require('objects-to-csv')

hanzi.start();

function readFile(){
    let rawdata = fs.readFileSync('merged.json', {encoding:'utf8', flag:'r'});
    var jsonFile = JSON.parse(rawdata);
    return jsonFile
}

var jsonFile = readFile();

// Add a new column (new item --> key + value in the json dictionary)
function addKeyValue(column, key, data){
    column[key] = data;
  }

/* Merge Arrays */
const merge = (first, second) => {
  for(let i=0; i<second.length; i++) {
    first.push(second[i]);
  }
  return first;
}

// Add missing info to json object
jsonFile.map(function(row) {

    // PINYIN
    pinyin = hanzi.getPinyin(row.hanzi_sc)

    // COMPONENTS
    decomposed = hanzi.decompose(row.hanzi_sc);
    addKeyValue(row, 'pinyin_parsed', pinyin);
    addKeyValue(row, 'decompose1_parsed', decomposed.components1);
    addKeyValue(row, 'decompose2_parsed', decomposed.components2);
    addKeyValue(row, 'decompose3_parsed', decomposed.components3);

    // APPEAR IN
    component_in = hanzi.getCharactersWithComponent(row.hanzi_sc)
    addKeyValue(row, 'component_in_parsed', component_in);

    // GET EXAMPLE WORDS by frequency
    examples = hanzi.getExamples(row.hanzi_sc)
    var words = [];
    examples.forEach(function(item) {
      var get_item = item.map(item => item.simplified);
      merge(words, get_item.slice(0, 5)); // CAN CHANGE FOR MORE WORDS
      
    })
    addKeyValue(row, 'words_parsed', words);


    // TRADITIONAL HANZI
    definitions = hanzi.definitionLookup(row.hanzi_sc);

    try {
      traditional  = definitions.map(item => item.traditional);
      addKeyValue(row, 'traditional_parsed', traditional[0]);
      //console.log(traditional)
    }
    catch(err) {
      err.message;
    }

    
    
    
});

//console.log(jsonFile)
/*let x = jsonFile.map(function(row) {
  pinyin = hanzi.getPinyin(row.hanzi_sc)
  return addKeyValue(row, 'pinyin_parsed', pinyin);
});*/


const fields = [
    'hanzi_sc', 'pinyin_parsed','decompose1_parsed',
    'decompose2_parsed', 'decompose3_parsed',
    'component_in_parsed', 'words_parsed', 
    'traditional_parsed'];
//const transforms = [unwin'd({ paths: ['items', 'items.items'] })];
//const json2csvParser = new Parser({ fields, transforms });
const json2csvParser = new Parser({fields});
const csv = json2csvParser.parse(jsonFile);

// write FILE
fs.writeFileSync('parsed_merged_0.csv', csv);
console.log("DONE !")

/* 'rank_junda',
    'pinyin_x', 'meaning', 'index_gscc',
    'level_hsk', 'index_hsk', 'rank_rsh',
    'key_word', 'pinyin_y', 'index_ccm',
    'hanzi_tc' , 'decomposition', 'pinyin'
*/

