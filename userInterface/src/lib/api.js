let url = "http://127.0.0.1:8000/"

async function getResponce(value){
  return (await (await fetch(url+value)).json())
}

async function getResponceAsJson(value = ''){
  return JSON.parse(await (await fetch(url+value)).json())
}

// export async let totalTime = await (await fetch(url+"time/total")).json();
export class dataBase
{
  async getTotalTime(){
    return getResponce("time/total");
  }

  /**
   * @param {string} name
   */
  async getTimeByName(name){
    return getResponce("time/"+name);
  }

  async getTimeByCatogary(day){
    return await getResponceAsJson("catogariesAndTime/?day="+day);
  }

  async getNamesAndContext()
  {
    return getResponceAsJson("namesAndContext");
  }
  
  async refresh(){
    return getResponce("refreshLabels/");
  }
}
