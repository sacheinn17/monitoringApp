let url = "http://127.0.0.1:8000/"

export class dataBase
{

  async getAppNames(){
    return JSON.parse( await (await fetch(url)).json());
  }

  async getTimeByName(name){
    return (await (await fetch(url+"time/"+name)).json());
  }

  async getAppContext(){
    return JSON.parse( await (await fetch(url)).json());
  }

}