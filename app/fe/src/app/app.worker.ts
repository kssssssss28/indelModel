/// <reference lib="webworker" />
import * as SparkMD5 from 'spark-md5';
/**
 *
 *
 * 签名 filereader blob webworker hash
 */

addEventListener('message', (files:any) => {
 let file = files.data
 //设置每个chunk的大小
 const size = 1*1024*1024
 // 兼容 符合h5的 firefox chrome&safari（webkit内核）
 let blobSliceFunc = File.prototype.slice
 // 计算总的chunk多少个 向上取整
 let chunkNumber = Math.ceil(file.size / size)
 // 当前chunk index
 let  currentChunk = 0
 // hash
 // 读文件
 let fileReader = new FileReader()
  const chunkList:any = []
 const loadNext = ()=>{
   // 起始位置 当前chunk的index * 每个chunk大小
   let startPosition = currentChunk * size
   // 判断是不是最后一个chunk -》 如果超过大小就读到文件尾就OK
   let end = ((startPosition + size) >=
    file.size ? file.size : startPosition + size)
   // 分块
   let chunk = blobSliceFunc.call(file, startPosition, end)
   // 读chunk
   fileReader.readAsArrayBuffer(chunk);
 }

 fileReader.onload = (e:any)=>{
   // 获取文件
   const spark = new SparkMD5.ArrayBuffer()
   const chunk = e.target.result;
   // 计算文件hash
   spark.append(chunk);
   let hash = spark.end()
   chunkList.push({chunk,hash})
   // index + 1
   currentChunk++;

   // 如果没有到最后一个chunk
   if (currentChunk < chunkNumber) {
     //调用next
     loadNext();
   }else{
     // 如果是最后一个chunk 获取spark里的最后个hash
     console.info('finished computed hash');
     // 返回hash
     postMessage(chunkList)
   }
 }


// start
 loadNext();
});
