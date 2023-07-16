const http = require('http');
const path = require('path');
const tf = require('@tensorflow/tfjs-node');
const url = require('url');
const modelPath = path.resolve(__dirname, 'model.json');

const fs = require('fs');


function parseToOneHot(dna) {
  const dna_dict = {
    'A': [1, 0, 0, 0],
    'C': [0, 1, 0, 0],
    'G': [0, 0, 1, 0],
    'T': [0, 0, 0, 1],
    'N': [0, 0, 0, 0]
  };
  const encoded_sequence = [];

  for (let i = 0; i < dna.length; i++) {
    const base = dna[i];
    const encoded_base = dna_dict[base];
    encoded_sequence.push(encoded_base);
  }

  const flatEncodedSequence = encoded_sequence.flat();
  const e = tf.tensor(flatEncodedSequence, [1, encoded_sequence.length, 4, 1]);
  
  return e;
}

function predict(model, dna) {
  const dnaEncoded = parseToOneHot(dna);
  const res = model.predict(dnaEncoded).arraySync();
  const result = {
    "dele": res[0][0],
    "oneIns": res[0][1],
    "oneDele": res[0][2]
  };

  for (const [key, value] of Object.entries(result)) {
    console.log(`${key}: ${value.toFixed(2)}`);
  }

  return result;
}


function parseModelDetails(jsonData) {
  const modelDetails = {};
  
  const modelTopology = jsonData.modelTopology;
  const layers = modelTopology.model_config.config.layers;
  
  modelDetails.layers = [];
  
  for (const layer of layers) {
    const layerDetails = {};
    
    layerDetails.name = layer.config.name;
    layerDetails.type = layer.class_name;
    
    if (layer.config.units) {
      layerDetails.units = layer.config.units;
    }
    
    modelDetails.layers.push(layerDetails);
  }
  
  const optimizerConfig = modelTopology.training_config.optimizer_config;
  modelDetails.optimizer = optimizerConfig.class_name;
  modelDetails.learningRate = optimizerConfig.config.learning_rate;
  
  return modelDetails;
}



const server = http.createServer((req, res) => {
  // 允许跨域请求的域名，可以根据需要进行更改
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    // OPTIONS 请求不需要实际的请求处理逻辑，只需返回响应头部即可
    res.writeHead(200);
    res.end();
  }
  if (req.method === 'POST') {
    req.on('data', (seq) => {
      let p = new Promise((resolve, reject)=>{
        fs.readFile('./model.json', 'utf8', (err, data) => {
          if (err) {
            console.error('读取文件时出错:', err);
            return;
          }   
          try {
            // 解析 JSON 数据
            const jsonData = JSON.parse(data);
            const modelDetails = parseModelDetails(jsonData);
            resolve(modelDetails.layers)
          } catch (error) {
            console.error('error:', error);
          }
        });
      })
        p.then(v=>{
          const resultString = JSON.stringify(v); // 将 result 对象转换为字符串
          res.statusCode = 200;
          res.setHeader('Content-Type', 'application/json');
          res.end(resultString);
        })
    });
  }


  if (req.method === 'GET') {
    const urlObj = url.parse(req.url, true);
    const query = urlObj.query;
    let dna = query.dna
    tf.loadLayersModel('file://' + modelPath).then(model => {
      const s = Array.from(dna)
      const result = predict(model,s);
      const resultString = JSON.stringify(result); // 将 result 对象转换为字符串
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(resultString);
    });
  }
});

server.listen(3000, 'localhost', () => {
  console.log('Server running at http://localhost:3000/');
});
