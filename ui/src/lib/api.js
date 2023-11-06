let url = "http://127.0.0.1:8000/"

async function getResponce(value){
  return (await fetch(url+value)).json()
}

async function getResponceAsJson(value = ''){
  return JSON.parse(await (await fetch(url+value)).json())
}

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
  
  refresh(){
    return getResponce("refreshLabels/");
  }
}
