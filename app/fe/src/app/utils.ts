import { async } from "@angular/core/testing";

export const checkFormatName = async (file:File)=>{
  const reader = new FileReader()
  const fileType = file.name.split(".")[1] || ''
  const buffer:any = await readFile2Buffer(file)
  // dataview用来操作二进制流
  var dataView = new DataView(buffer);
  // 获取16位无符号整数 并转为 16进制 为什么16 idk 不然直接判断也可以
  // 16比2短 2/3
  // magic number我这只准接收 压缩文件 因为情况复杂
  // 举例有些文件没有magic number 例如cvs 有些的共享 例如xlxs和压缩包 因为xlxs 本质就是压缩包
  //
  var magicNumber = dataView.getUint16(0, false).toString(16); // 读取文件的前两个字节
  if(magicNumber == "504B" || "504b")
    return true

  return false

}

const readFile2Buffer = async (file:File, start=0, end=8)=>{
  return new Promise((resolve, reject)=>{
    const reader = new FileReader()
    reader.readAsArrayBuffer(file.slice(start, end))
    reader.onload = ()=>{
      resolve(reader.result)
    }
  })
}

export const spliceFile = async (file:File)=>{
  //const worker  = new Worker("file-worker.worker.ts")
  const worker = new Worker(new URL('./app.worker', import.meta.url));
  worker.postMessage(file)
  const chunkList = await new Promise((resolve, reject)=>{
    worker.onmessage = (event) => {
      const result = event.data;
      resolve(result);
    };
  })
  console.log(chunkList)

}


console.log(1)
const async1 =async () => {
  await async2()
  console.log(2)
  await async3()
  console.log(3)
}

const async2 = async () =>{
  console.log(4)
}

const async3 = ()=>{
  console.log(5)
}

async1()

setTimeout(() => {
  console.log(6)
}, 0);

new Promise((resolve,r)=>{
  console.log(7)
  resolve(1)
}).then(v=>{
  console.log(8)
}).then(v=>{
  console.log(9)
})
