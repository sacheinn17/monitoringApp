import {dataBase} from "./api.js"
import { weeks } from "./stores/lists.js";
const db = new dataBase;

export function sortByKeyDesc(array, key) {
    return array.sort(function(a, b) {
      var x = a[key];
      var y = b[key];
      return ((x > y) ? -1 : ((x < y) ? 1 : 0));
    });
  }

export async function getTop5Apps(query){
    const value = await(query);
    return sortByKeyDesc(value,"time").slice(0,5);
}

export function getDate(today = new Date){
    return today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');}

export function getDates(date)
{
    let curr = new Date(date);
    console.log(date)
    let firstDayofWeek = curr.getDate() - curr.getDay();
    console.log(curr)
    let days = [];
    console.log(curr.getMonth())
    for (const x of Array(7).keys()){
        curr = new Date(date);
            days.push(getDate(new Date(curr.setDate(firstDayofWeek+x)))) 
            days = [...days]
        }
    
    weeks.set(days);
    return days;
}

export async function getCatTimeWithDate(database,dates)
{
    let dayWithCatogary = [];
    for (const x of Array(7).keys()){
        let t2 = await database.getCatogariesAndTime(dates[x]);
        if (t2[0] != null){
            dayWithCatogary.push(t2)
        }
        else{
            t2 = [{"time":0}]
            dayWithCatogary.push(t2[0])
        }
    }
    return dayWithCatogary
}

export async function getTimeByCat(date,catogary){
    let t = await db.getCatogariesAndTime(date);
    // console.log(date,t)
    if(t[0] !=null){
        for (const x of t){
            // console.log(x)
            if (x.name === catogary){
                return x.time;
            }
        }
    }
    else{
        return 0;
    }
}

export function getTimeCat(date,catogary)
{
    return db.getCatogariesAndTime(date).then(
        t =>{
            if(t[0] !=null){
                for (const x of t){
                    // console.log(x)
                    if (x.name === catogary){
                        // console.log(x);
                        return x.time/60;
                    }
                }
            }
            else{
                return 0;
                
            }
        }
    )
}

function getNoOfDays(month,leapYear = false){
    if (month in [1,3,5,7,8,10,12]){
        return 31;
    }
    else if(month in [4,6,9,11]){
        return 30;
    }
    else if (leapYear === true){
        return 29;
    }
    else{
        return 28;
    }
}