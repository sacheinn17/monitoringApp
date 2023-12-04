import { fetch,ResponseType } from "@tauri-apps/api/http";

let url = "http://127.0.0.1:1421/"



async function getResponce(value){
  return (await fetch(url+value,{
    method:"GET",
    timeout:30,
    responseType:ResponseType.JSON,
  })).data
}

async function getResponceAsJson(value = ''){
  return JSON.parse((await fetch(url+value,{
    method:"GET",
    timeout:30,
    responseType:ResponseType.JSON,
  })).data)}

// export async let totalTime = await (await fetch(url+"time/total")).json();
export class dataBase
{
  getTotalTime(day){
    return getResponce("time/total?day="+day);
  }

  refreshDataBase(){
    return getResponce("refreshLabels/");
  }

  /**
   * @param {string} name
   */
   getTimeByName(name){
    return getResponce("time/"+name);
  }

  getAppUsage(day){
    return getResponceAsJson("getAppUsageTime/?day="+day);
  }
  getCatogariesAndTime(day){
    return getResponceAsJson("catogariesAndTime/?day="+day);
  }

  getNamesAndContext()
  {
    return getResponceAsJson("namesAndContext");
  }
  
  getCatNames()
  {
    return getResponceAsJson("getCatNames");
  }

  refresh(){
    return getResponce("refreshLabels/");
  }

  getNameByCat(name,date){
    return getResponceAsJson("nameByCat/?cat="+name+"&date="+date)
  }


}
